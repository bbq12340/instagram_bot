import os
import csv

def log_login(timestamp):
    with open('logs/activity_log.txt', 'a') as f:
        f.write(f"Safely logged in! TimeStamp: {timestamp}\n\n")

def log_search_tags(progress_string):
    with open('logs/activity_log.txt', 'a') as f:
        f.write(f"{progress_string}\n\n")

def log_post_info(i, post_info):
    with open('logs/activity_log.txt', 'a') as f:
        f.write(f"Post #{i}: {post_info}\n\n")

def log_followers_record(timestamp, followers_count):
    with open('logs/followers_record.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimeter=',')
        csv_writer.writerow([timestamp, followers_count])

def log_followers_list(timestamp, followers_list):
    open ('logs/followers_list.txt', 'w').close()
    with open('logs/followers_list.txt', 'a') as f:
        f.write(f"{timestamp}\nTotal Follwers: {len(followers_list)}\n")
        for name in followers_list:
            f.write(f"{name}\n")