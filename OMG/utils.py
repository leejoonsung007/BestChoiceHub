import time

# 生成日志文件
def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 转换unix time成正常显示的时间
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)