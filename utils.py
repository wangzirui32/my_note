import time

def strftime(timestamp):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))