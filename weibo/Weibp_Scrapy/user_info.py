import re
import xlwt
import pandas as pd
import os

class user():
    def __init__(self, driver):

        self.brief_intro = ''
        self.concern_count = ''
        self.followers_count = ''
        self.blogs_count = ''
        self.driver = driver
        self.user_info = {}

    def get_brief_intro(self):

        str_intro = self.driver.find_element_by_xpath("//div[@class='pf_intro']")
        str_t = str_intro.text.split(" ")
        self.brief_intro = str_t[0]   # 空格分隔 获取第一个值 "Eastmount 详细资料 设置 新手区"
        print(self.brief_intro)

    def get_concern_count(self):
        try:
            str_wb = self.driver.find_element_by_xpath("//td[1]/a[@class='t_link S_txt1']/strong")
        except:
            str_wb = self.driver.find_element_by_xpath("//td[@class='S_line1'][1]/strong")
        pattern = r"\d+\.?\d*"  # 正则提取"微博[0]" 但r"(\[.*?\])"总含[]
        guid = re.findall(pattern, str_wb.text, re.S | re.M)
        concern_count = ''
        for value in guid:
            concern_count = int(value)
            break
        self.concern_count = concern_count
        print(u'关注数: ' + str(concern_count))

    def get_followers_count(self):

        pattern = r"\d+\.?\d*"  # 正则提取"微博[0]" 但r"(\[.*?\])"总含[]
        try:
            str_gz = self.driver.find_element_by_xpath("//td[2]/a[@class='t_link S_txt1']/strong")
        except:
            str_gz = self.driver.find_element_by_xpath("//td[@class='S_line1'][2]/strong")
        guid = re.findall(pattern, str_gz.text, re.M)
        followers_count = int(guid[0])
        print(u'粉丝数: ' + str(followers_count))

    def get_blogs_count(self):

        pattern = r"\d+\.?\d*"  # 正则提取"微博[0]" 但r"(\[.*?\])"总含[]
        try:
            str_fs = self.driver.find_element_by_xpath("//td[3]/a[@class='t_link S_txt1']/strong")
        except:
            str_fs = self.driver.find_element_by_xpath("//td[@class='S_line1'][3]/strong")
        guid = re.findall(pattern, str_fs.text, re.M)
        blogs_count = int(guid[0])
        self.blogs_count = blogs_count
        print(u'微博数: ' + str(blogs_count))

    def get_user_blog(self):

        self.get_blogs_count()
        self.get_brief_intro()
        self.get_concern_count()
        self.get_followers_count()

        user_blog = {}
        user_blog['blogs_count'] = [self.blogs_count]
        user_blog['brief_intro'] = [self.brief_intro]
        user_blog['concern_count'] = [self.concern_count]
        user_blog['followers_count'] = [self.followers_count]
        self.user_info = user_blog
        return self.user_info


if __name__ == '__main__':

    path = os.getcwd()+'/'+"银豆网.xls"
    x = pd.read_excel(path)
