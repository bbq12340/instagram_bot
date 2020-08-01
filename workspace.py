import os

def log_login(timestamp):
    f = open('logs/activity_log.txt', 'a')
    f.write(f"Safely logged in! TimeStamp: {timestamp}\n\n")
    f.close()

def log_search_tags(progress_string):
    f = open('logs/activity_log.txt', 'a')
    f.write(f"{progress_string}\n\n")

def log_post_info(i, post_info):
    f = open('logs/activity_log.txt', 'a')
    f.write(f"Post #{i}: {post_info}\n")
    f.close()