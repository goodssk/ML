import time
from Weibp_Scrapy.time_fix import time_fix

# 根据微博的url抓取评论信息，抓取策略是，因为网页不显示所的评论，所以先模拟下拉，显示所有评论信息再进行抓取．


class comment():
    def __init__(self, driver, mid):

        self.driver = driver
        self.comment_info = {}    # 一条微博的所有评论
        self.mid = mid

    def get_comment(self):

        js = "var q=document.documentElement.scrollTop=100000"
        start_out = 0

        # 模拟下拉
        while(1):
            start_out = start_out+1
            time.sleep(1)
            self.driver.execute_script(js)
            print("two")
            try:
                self.driver.find_element_by_xpath("//div[@class='list_ul' and @node-type='comment_list']/a[@action-type='click_more_comment']")
                break
            except:
                if start_out == 3:
                    break
        # 循环模拟点击查看更多，直到显示所有评论
        while(1):
            try:
                time.sleep(1)
                self.driver.execute_script(js)   # 下拉
                out = self.driver.find_element_by_xpath("//div[@class='list_ul' and @node-type='comment_list']/a[@action-type='click_more_comment']")
                print(out.text)
                out.click()
            except:
                print("comment_finally")
                break

        index = 0
        names = []
        comment_url = []
        comment_content = []
        comment_time = []
        mid = []
        brief_intro = []

        # 抓取该条微博所有评论信息
        while(1):
            index = index+1
            try:
                #用户名
                name = self.driver.find_element_by_xpath("//div[@class='list_ul' and @node-type='comment_list']/div["+str(index)+"]//div[@class='list_con']/div[@class='WB_text']/a[@usercard]")
                name = name.text
                print(name)
                url = self.driver.find_element_by_xpath("//div[@class='list_ul' and @node-type='comment_list']/div["+str(index)+"]//div[@class='list_con']/div[@class='WB_text']/a[@usercard]").get_attribute('href')
                print(url)
                content = self.driver.find_element_by_xpath("//div[@class='list_ul' and @node-type='comment_list']/div["+str(index)+"]//div[@class='list_con']/div[@class='WB_text']")
                content = content.text
                content = content.split("：")
                content = content[-1]
                print(content)
                time1 = self.driver.find_element_by_xpath("//div[@class='list_ul' and @node-type='comment_list']/div["+str(index)+"]/div[@class='list_con']/div[@class='WB_func clearfix']/div[@class='WB_from S_txt2']").text
                time1 = time_fix(time1)
                print(time1)
                names.append(name)
                comment_url.append(url)
                comment_content.append(content)
                comment_time.append(time1)
                mid.append(self.mid)
                brief_intro.append('comment')

            except Exception as e:
                print(e)
                break
        comment_info = {}
        comment_info['name'] = names
        comment_info['url'] = comment_url
        comment_info['content'] = comment_content
        comment_info['time'] = comment_time
        comment_info['brief_intro'] = brief_intro
        comment_info['mid'] = mid

        self.comment_info = comment_info
        return comment_info
