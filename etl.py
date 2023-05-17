import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime
from io import StringIO
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read_file(open('dmp.cfg'))

USER = config.get('POSTGRES','USER')
PASSWORD = config.get('POSTGRES','PASSWORD')

def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values
    song_data = song_data[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values
    artist_data = artist_data[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df1 = df.loc[ df['page'] == 'NextSong' ].copy()

    # convert timestamp column to datetime
    df1['date_time'] = [x.strftime("%Y-%m-%d %H:%M:%S") for x in map(lambda x: datetime.datetime.fromtimestamp(int(x)/1000), df1['ts'])]
    df1['date_time'] = pd.to_datetime(df1['date_time'])
    df1['month'] = [x for x in map(lambda x: x.month, pd.Series(df1['date_time']))]
    df1['week'] = [x for x in map(lambda x: x.week, pd.Series(df1['date_time']))]
    df1['weekday'] = [x for x in map(lambda x: x.dayofweek, pd.Series(df1['date_time']))]
    df1['hour'] = [x for x in map(lambda x: x.hour, pd.Series(df1['date_time']))]
    df1['year'] = [x for x in map(lambda x: x.year, pd.Series(df1['date_time']))]
    df1['day'] = [x for x in map(lambda x: x.day, pd.Series(df1['date_time']))]
    
    # insert time data records
    time_df = df1[['date_time','hour','day','week','month','year','weekday']].copy()

    output = StringIO()
    time_df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    cur.copy_from(output, 'time', null="")

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']].copy()
    
    # drop rows with blank/null userid
    user_df['userId'].replace('', np.nan, inplace=True) # replaces blank '' with nan/null
    user_df.dropna(subset=['userId'], inplace=True) # drops all nan/null values

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df1.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.date_time, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(f"host=127.0.0.1 dbname=sparkifydb user={USER} password={PASSWORD}")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()
    

if __name__ == "__main__":
    main()