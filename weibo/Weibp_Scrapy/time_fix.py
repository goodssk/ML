import datetime
import re


def time_fix(time_string):
    now_time = datetime.datetime.now()

    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        created_at = now_time - datetime.timedelta(minutes=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M:%S')

    if '小时前' in time_string:
        minutes = re.search(r'^(\d+)小时', time_string).group(1)
        created_at = now_time - datetime.timedelta(hours=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M:%S')

    if '今天' in time_string:
        time = now_time.strftime('%Y-%m-%d') + ' '
        time_string = time_string.replace('今天', time)
        return time_string

    if '月' in time_string and '年' not in time_string:
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string

    if '年' in time_string:
        time_string = time_string.replace('年', '-').replace('月', '-').replace('日', '')
        return time_string

    return time_string

class time():
    def __init__(self, time_string):
        self.time_string = time_string

    def time_fix(self):
        now_time = datetime.datetime.now()
        if '分钟前' in self.time_string:
            minutes = re.search(r'^(\d+)分钟', self.time_string).group(1)
            created_at = now_time - datetime.timedelta(minutes=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M:%S')

        if '小时前' in self.time_string:
            minutes = re.search(r'^(\d+)小时', self.time_string).group(1)
            created_at = now_time - datetime.timedelta(hours=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M:%S')

        if '今天' in self.time_string:
            time = now_time.strftime('%Y-%m-%d') + ' '
            time_string = self.time_string.replace('今天', time)
            return time_string

        if '月' in self.time_string and '年' not in self.time_string:
            time_string = self.time_string.replace('月', '-').replace('日', '')
            time_string = str(now_time.year) + '-' + time_string
            return time_string

        if '年' in self.time_string:
            time_string = self.time_string.replace('年', '-').replace('月', '-').replace('日', '')
            return time_string


if __name__ == "__main__":

    str1 = '3小时前'
    out = time_fix(str1)
    print(out)
