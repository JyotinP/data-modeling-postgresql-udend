# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = " DROP TABLE IF EXISTS users "
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLE IF NOT EXISTSS

songplay_table_create = (""" 
                        CREATE TABLE IF NOT EXISTS songplay 
                        (
                        songplay_id SERIAL PRIMARY KEY, 
                        start_time TIMESTAMP NOT NULL, 
                        user_id int NOT NULL, 
                        level varchar, 
                        song_id varchar, 
                        artist_id varchar, 
                        session_id int, 
                        location varchar, 
                        user_agent varchar
                        )
                        """)

user_table_create = ("""
                    CREATE TABLE IF NOT EXISTS users
                    (
                    user_id int PRIMARY KEY, 
                    first_name varchar, 
                    last_name varchar, 
                    gender char(1), 
                    level varchar
                    )
                    """)

song_table_create = (""" 
                    CREATE TABLE IF NOT EXISTS song 
                    (
                    song_id varchar PRIMARY KEY, 
                    title varchar NOT NULL, 
                    artist_id varchar, 
                    year smallint, 
                    duration numeric NOT NULL
                    )
                    """)

artist_table_create = (""" 
                      CREATE TABLE IF NOT EXISTS artist 
                      (
                      artist_id varchar PRIMARY KEY, 
                      name varchar NOT NULL, 
                      location varchar, 
                      latitude decimal, 
                      longitude decimal
                      )
                      """)

time_table_create = (""" 
                    CREATE TABLE IF NOT EXISTS time 
                    (
                    start_time TIMESTAMP PRIMARY KEY, 
                    hour smallint, 
                    day smallint, 
                    week smallint, 
                    month smallint, 
                    year smallint, 
                    weekday varchar
                    )
                    """)

# INSERT RECORDS

songplay_table_insert = (""" 
INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT(user_id) DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
INSERT INTO song (song_id, title, artist_id, year, duration)
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artist (artist_id, name, location, latitude, longitude)
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES(%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = (""" 
select s.song_id, a.artist_id from song s 
inner join artist a 
on s.artist_id = a.artist_id
where s.title = %s
and a.name = %s
and s.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]