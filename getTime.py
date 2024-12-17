import datetime
import time

def get_end_of_day_timestamp(date=None):
    # 如果没有提供日期，默认使用当天
    if date is None:
        date = datetime.datetime.now()
    else:
        # 确保提供的日期是datetime.date对象
        date = datetime.datetime.combine(date, datetime.time())

    # 设置时间为23:59:59
    end_of_day = date.replace(hour=23, minute=59, second=59)

    # 将datetime对象转换为Unix时间戳
    timestamp = int(time.mktime(end_of_day.timetuple()))

    return timestamp

def get_timestamp_half_month_ago():
    # 获取当前时间
    now = datetime.datetime.now()
    
    # 计算15天前的日期
    half_month_ago = now - datetime.timedelta(days=15)
    
    # 设置时间为当天的23:59:59
    end_of_day = half_month_ago.replace(hour=23, minute=59, second=59)
    
    # 将datetime对象转换为Unix时间戳
    timestamp = int(time.mktime(end_of_day.timetuple()))
    
    return timestamp

def get_timestamp_three_month_ago():
    # 获取当前时间
    now = datetime.datetime.now()
    
    # 计算15天前的日期
    half_month_ago = now - datetime.timedelta(days=90)
    
    # 设置时间为当天的23:59:59
    end_of_day = half_month_ago.replace(hour=23, minute=59, second=59)
    
    # 将datetime对象转换为Unix时间戳
    timestamp = int(time.mktime(end_of_day.timetuple()))
    
    return timestamp

