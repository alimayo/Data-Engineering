# Project: Data Modeling with Cassandra

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions

## Project Overview

In this project, I applied what I have learned on data modeling with Apache Cassandra and complete an ETL pipeline using Python. To complete the project, I modelled data by creating tables in Apache Cassandra to run queries. I developed  ETL pipeline that transfers data from a set of CSV files within a directory to create a streamlined CSV file to model and insert data into Apache Cassandra tables.


## Datasets
For this project, I worked with one dataset: event_data. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:

>event_data/2018-11-08-events.csv
>event_data/2018-11-09-events.csv

### Streamlined CSV file we created and used to import data to Apache Cassandra:

CSV file  <font color=red>event_datafile_new.csv</font>, located within the Workspace directory.  The event_datafile_new.csv contains the following columns: 

- artist 
- firstName of user
- gender of user
- item number in session
- last name of user
- length of the song
- level (paid or free song)
- location of the user
- sessionId
- song title
- userId

The image below is a screenshot of what the denormalized data should appear like in the <font color=red>**event_datafile_new.csv**</font> after the code above is run:<br>

![alt data image]<https://github.com/alimayo/Udacity---Data-Engineering/blob/main/Data%20Modeling/Apache%20Cassandra/image_event_datafile_new.jpg?raw=true>

## Table Design

I designed my tables according to the following three queries:

### 1. Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4


### 2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
    

### 3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

## RUN Code

In order to run the code download the zip file and extract it. Run the ipynb file using jupyter notebook/lab. 
