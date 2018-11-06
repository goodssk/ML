#coding=utf-8

from selenium import webdriver
from Weibp_Scrapy import blog_info
from Weibp_Scrapy import user_info
from Weibp_Scrapy import comment_info
import selenium.webdriver.support.ui as ui
import pandas as pd
import time
import os


class Weibo():

    def __init__(self):

        self.page_info = []   #  每个搜索页的所有信息
        self.driver = webdriver.Chrome()
        self.username = '***********'     # 帐号
        self.password = '***********'　　　# 密码
        self.LoginWeibo()
        self.key_word = '银豆网'
        self.write_path = os.getcwd()+'/'+self.key_word+".xls"
        self.next_page = "https://s.weibo.com/weibo/"+self.key_word+"?topnav=1&wvr=6&b=&page=15"
        self.KW_all_info = pd.DataFrame()

        if os.path.exists(self.write_path):
            frame = pd.read_excel(self.write_path)
            self.KW_all_info = self.KW_all_info.append(frame)

    def LoginWeibo(self):
        try:
            # **********************************************************************
            # 直接访问driver.get("http://weibo.cn/5824697471")会跳转到登陆页面 用户id
            #
            # 用户名<input name="mobile" size="30" value="" type="text"></input>
            # 密码 "password_4903" 中数字会变动,故采用绝对路径方法,否则不能定位到元素
            #
            # 勾选记住登录状态check默认是保留 故注释掉该代码 不保留Cookie 则'expiry'=None
            # **********************************************************************
            wait = ui.WebDriverWait(self.driver, 10)
            # 输入用户名/密码登录
            print(u'准备登陆Weibo.cn网站...')
            self.driver.get("https://weibo.com/")
            time.sleep(10)   #　等待页面载入
            elem_user = self.driver.find_element_by_id('loginname')
            elem_user.clear()
            elem_user.send_keys(self.username)  # 用户名
            elem_pwd = self.driver.find_element_by_class_name('password').find_element_by_name('password')
            elem_pwd.clear()
            elem_pwd.send_keys(self.password)  # 密码

            elem_sub = self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')
            elem_sub.click()  # 点击登陆
            time.sleep(30)    # 重点: 暂停时间输入验证码
            elem_sub.click()  # 点击登陆

            # 获取Coockie 推荐 http://www.cnblogs.com/fnng/p/3269450.html
            #print driver.get_cookies()  # 获得cookie信息 dict存储
            #print u'输出Cookie键值对信息:'
            print(self.driver.get_cookies())
            for cookie in self.driver.get_cookies():
                # print cookie
                for key in cookie:
                    print(key, cookie[key])

            print(u'登陆成功...')
            time.sleep(5)

        except Exception as e:
            print("Error5: ", e)

    # *************************************************************
    #  先把一个搜索页面的信息抓取下来，包括三个部分
    #  1.一条微博的信息
    #  2.微博的评论
    #  3.博主的url
    # *************************************************************
    def get_page(self):
        index = 0
        print("进入搜索页")
        self.driver.get(self.next_page)

        while(1):
            try:
                blogs = {}
                index = index + 1

                blog_data = blog_info.blog(self.driver, index)
                blog = blog_data.get_blog()                 # 抓取一条微博的基本信息

                user_url = blog_data.get_user_url()         # 博主的url
                comment_url = blog_data.get_comment_url()   # 如果评论比较多，抓取评论的url
                comment = blog_data.get_comment()           # 如果评论比较少，直接把评论抓下来

                try:
                    self.next_page = blog_data.get_next_page()   # 获得下一页的url
                except:
                    print("finally:", self.key_word)
                    self.next_page = 'finally'

                blogs['blog'] = blog
                blogs['user_url'] = user_url
                blogs['comment_url'] = comment_url
                blogs['comment'] = comment
                self.page_info.append(blogs)
            except Exception as e:
                print(e)
                break
        print(self.next_page)

    def get_all_page(self):

        while(self.next_page != 'finally'):

            self.get_page()
            print('开始抓取每个用户信息和评论信息')
            print(len(self.page_info))
            print(self.page_info)

            for blogs in self.page_info:
                try:
                    mid = blogs['blog']['mid'][0]

                    blog_url = blogs['user_url']
                    self.driver.get(blog_url)
                    print(blog_url)
                    user = user_info.user(self.driver)
                    user_infos = user.get_user_blog()
                    blog = dict(user_infos, **blogs['blog'])
                    self.KW_all_info = self.KW_all_info.append(pd.DataFrame(blog))

                    print("comment_url", blogs['comment_url'])
                    if blogs['comment_url'] == '':
                        self.KW_all_info = self.KW_all_info.append(pd.DataFrame(blogs['comment']))

                    if blogs['comment_url'] != 'zero' and blogs['comment_url'] != '':
                        self.driver.get(blogs['comment_url'])
                        comment = comment_info.comment(self.driver, mid)
                        self.KW_all_info = self.KW_all_info.append(pd.DataFrame(comment.get_comment()))
                        self.write_xls()

                except Exception as e:
                    print(e)

            self.KW_all_info.to_excel(self.write_path, index=False)
            self.page_info = []

        self.KW_all_info = pd.DataFrame()

    def get_all_user(self):
        users = ['微贷网', '钱盆网', '团贷网', '银豆网', '多多理财', '小猪理财']
        for user in users:

            self.key_word = user
            self.write_path = os.getcwd()+'/'+self.key_word+".xls"
            self.next_page = "https://s.weibo.com/weibo/"+self.key_word+"?topnav=1&wvr=6&b="

            print(self.next_page)
            print(user)
            self.get_all_page()

    def write_xls(self):

        if not os.path.exists(self.write_path):
            frame = pd.DataFrame()
            frame.to_excel(excel_writer=self.write_path)

        frame = pd.DataFrame(self.KW_all_info)
        frame.to_excel(self.write_path, index=False)


def write_xls(blog, path):

    if not os.path.exists(path):
        frame = pd.DataFrame()
        frame.to_excel(excel_writer=path)

    frame = pd.read_excel(path)
    frame1 = pd.DataFrame(blog)
    frame_out = frame.append(frame1)
    frame_out.to_excel(path, index=False)


if __name__ == "__main__":

    weibo = Weibo()

    weibo.get_all_page()

  
