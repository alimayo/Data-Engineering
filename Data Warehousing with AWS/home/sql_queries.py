import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE staging_events
                                (
                                artist          VARCHAR,
                                auth            VARCHAR, 
                                first_name      VARCHAR,
                                gender          VARCHAR,   
                                item_in_session INTEGER,
                                last_name       VARCHAR,
                                length          FLOAT,
                                level           VARCHAR, 
                                location        VARCHAR,
                                method          VARCHAR,
                                page            VARCHAR,
                                registration    BIGINT,
                                session_id      INTEGER,
                                song            VARCHAR,
                                status          INTEGER,
                                ts              TIMESTAMP,
                                user_agent      VARCHAR,
                                user_id         INTEGER
                                );
                                """)

staging_songs_table_create = ("""CREATE TABLE staging_songs
                                (
                                song_id            VARCHAR,
                                num_songs          INTEGER,
                                title              VARCHAR,
                                artist_name        VARCHAR,
                                artist_latitude    FLOAT,
                                year               INTEGER,
                                duration           FLOAT,
                                artist_id          VARCHAR,
                                artist_longitude   FLOAT,
                                artist_location    VARCHAR
                                );
                                """)

songplay_table_create = ("""CREATE TABLE songplays
                            (
                            songplay_id int IDENTITY(0,1) primary key, 
                            start_time timestamp not null distkey, 
                            user_id int not null, 
                            level varchar, 
                            song_id varchar, 
                            artist_id varchar,
                            session_id int not null, 
                            location varchar, 
                            user_agent varchar not null
                            );
                            """)

user_table_create = ("""CREATE TABLE users
                        (
                        user_id int primary key sortkey, 
                        first_name varchar not null, 
                        last_name varchar, 
                        gender varchar(1), 
                        level varchar
                        ) diststyle all;
                        """)

song_table_create = ("""CREATE TABLE songs
                        (
                        song_id varchar primary key sortkey, 
                        title varchar, 
                        artist_id varchar not null, 
                        year int, 
                        duration float
                        ) diststyle all;
                        """)

artist_table_create = ("""CREATE TABLE artists
                            (
                            artist_id varchar primary key sortkey, 
                            name varchar, 
                            location varchar, 
                            latitude float, 
                            longitude float
                            ) diststyle all;
                        """)

time_table_create = ("""CREATE TABLE time
                        (
                        start_time timestamp primary key sortkey distkey, 
                        hour int, 
                        day int, 
                        week int, 
                        month int, 
                        year int, 
                        weekday int
                        );
                    """)

# STAGING TABLES

staging_events_copy = (""" 
                        COPY staging_events from {}
                        iam_role {}
                        region 'us-west-2'
                        FORMAT as json {}
                        TIMEFORMAT as 'epochmillisecs';
                        """).format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE','ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""COPY staging_songs from {}
                        iam_role {}
                        region 'us-west-2'
                        FORMAT as json 'auto';
                        """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE','ARN'))


# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id , level , song_id , artist_id, session_id, location, user_agent)
                        SELECT DISTINCT(ts) as start_time, 
                               se.user_id                                as user_id,
                               se.level                                 as level,
                               ss.song_id                               as song_id,
                               ss.artist_id                             as artist_id,
                               se.session_id                            as session_id,
                               se.location                              as location,
                               se.user_agent                             as user_agent
                        FROM staging_events se
                        JOIN staging_songs ss ON (se.artist = ss.artist_name AND se.song = ss.title)
                        WHERE se.page = 'NextSong' and ts IS NOT NULL;""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                        SELECT DISTINCT user_id                          as user_id,
                                        first_name                       as first_name,
                                        last_name                        as last_name,
                                        gender                           as gender,
                                        level                            as level
                        FROM staging_events
                        WHERE user_id IS NOT NULL;""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                        SELECT DISTINCT song_id                            as song_id,
                                        title                              as title,
                                        artist_id                          as artist_id,
                                        year                               as year,
                                        duration                           as duration
                        FROM staging_songs
                        WHERE song_id IS NOT NULL;""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
                            SELECT DISTINCT artist_id                       as artist_id,
                                            artist_name                     as name,
                                            artist_location                 as location,
                                            artist_latitude                 as latitude,
                                            artist_longitude                as longitude
                            FROM staging_songs
                            WHERE artist_id IS NOT NULL;""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                        SELECT DISTINCT(ts)                                AS start_time,  
                               EXTRACT(hour FROM ts)                       AS hour,
                               EXTRACT(day FROM ts)                        AS day,
                               EXTRACT(week FROM ts)                       AS week,
                               EXTRACT(month FROM ts)                      AS month,
                               EXTRACT(year FROM ts)                       AS year,
                               EXTRACT(weekday FROM ts)                    AS weekday
                        FROM staging_events
                        WHERE ts IS NOT NULL;""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
