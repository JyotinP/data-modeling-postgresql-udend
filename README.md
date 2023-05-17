# Project Description

As a startup in the music streaming industry, we want want to analyze the data which we've been collecting on songs and user activity. The   analytics team is particularly interested in understanding what songs users are listening to. We want to provide data in a format which makes it easier for them to do so.

First we'll define and create new fact and dimension tables according to the star schema, which makes it easy and efficient to execute analytical join queries.

Then we'll build an ETL pipeline which will transfer data from the log and song json files of our music streaming app to these star schema based tables in Postgres.

# Project Datasets
There are two datasets residing in Local Directory:

- **Song data:** > data/song_data
- **Log data:** > data/log_data

## Song dataset
- Subset of [Million Song Dataset](http://millionsongdataset.com)
- JSON files
- Sample:
```json
{"num_songs": 1, "artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null, "artist_longitude": null, "artist_location": "California - LA", "artist_name": "Casual", "song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```

## Log dataset
- Generated by [Event Simulator](https://github.com/Interana/eventsim)
- JSON files
- Sample:
```json
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
```

# Files

First we should define all the table create queries and insert statements in the 'sql_queries.py' file.

'create_tables.py' has all the functions which executes the create table queries from the 'sql_queries.py'. Executing this will establish connection with the Postgres, create database and the defined tables.

'etl.ipynb' is where we develop ETL processes for each table and insert data from one file to test whether our pipeline is working as per expectations.

'etl.py' is where we process data from all the log and song json files with the ETL pipeline developed in 'etl.ipynb' file.

'test.ipynb' is where we confirm your records were successfully inserted into each table and run sanity tests.

# Database schema design and ETL pipeline

'songplays' is our Fact Table. This contains records in log data associated with song plays. Primary key values from other tables are included  
to make it easier to join with other tables and do various analytical tasks. Data is filtered to contain only information associated with 'NextSong' page. We've implemented auto incremental primary key value for 'songplay_id'.

'users' is our Dimension Table. This contains records of all the users in the app. It contans name of the user, gender and level of subscription of the app.

'songs' is our Dimension Table. This contains records of all songs in the music database. It contains song title, year of release and duration.

'artists' is our Dimension Table. This contains records of all artists in music database. It countain name of the artist and location.

'time' is our Dimension Table. This contains records of all timestamps of records in songplays broken down into specific units.  
Date/time data is broken down into hour, day, week, month, year, weekday columns.
