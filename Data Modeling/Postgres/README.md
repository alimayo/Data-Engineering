# Data Modeling with Postgres
## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

I have created a Postgres database with tables designed to optimize queries on song play analysis and help Sparkify through the problem. I have developed a database schema and ETL pipeline for this analysis.

## Project Description
In this project, I have applied what I learned in data modeling with Postgres and built an ETL pipeline using Python. In order to complete the project,I defined fact and dimension tables for a star schema for a particular analytic focus, and wrote an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

>{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
## Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.
![Log Data](log_data.PNG)

If you would like to look at the JSON data within log_data files, you will need to create a pandas dataframe to read the data. Remember to first import JSON and pandas libraries (these have been done in the etl.py notebood already!).

>df = pd.read_json(filepath, lines=True)

For example,
>df = pd.read_json('data/log_data/2018/11/2018-11-01-events.json', lines=True) would read the data file 2018-11-01-events.json.


#### The dataset is provided in data.zip, unzip it in the folder where other project files are present.


## Project Files
You can download the project template files if you'd like to develop your project locally.

In addition to the data files, the project workspace includes six files:

1. test.ipynb displays the first few rows of each table to check the database.
2. create_tables.py drops and creates the tables. Run this file to reset your tables before each time ETL scripts are run.
3. etl.ipynb reads and processes a single file from song_data and log_data and loads the data into the tables. This notebook contains detailed instructions on the ETL process for each of the tables.
4. etl.py reads and processes files from song_data and log_data and loads them into the tables. You can fill this out based on the work in the ETL notebook.
5. sql_queries.py contains all the sql queries, and is imported into the last three files above.

## ETL Pipeline

An ETL Pipeline refers to a set of processes extracting data from an input source, transforming the data, and loading into an output destination such as a database, data mart, or a data warehouse for reporting, analysis, and data synchronization. The letters stand for Extract, Transform, and Load.

I have establised an ETL pipeline in this project, in the etl.py file. A more basic and sectored version has been provided in etl.ipynb file.

## Sample Queries

>SELECT s.title as song name, a.name as artist name FROM artists as a JOIN songs as s WHERE s.song_id = a.artist_id
