import time


# generate log
def log(*args, **kwargs):
    time.time()
    # return unix time
    # convert unix time to formatted time
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
