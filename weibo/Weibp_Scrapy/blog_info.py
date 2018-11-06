import re
import time
from Weibp_Scrapy.time_fix import time_fix
# 搜索页面上每条微博的信息
class blog():
    def __init__(self, driver, index):
        self.name = ''
        self.forward = ''
        self.content = ''
        self.driver = driver
        self.index = index
        self.mid = ''
        self.like = ''
        self.public_time = ''
        self.user_url = ''
        self.comment_url = ''
        self.blog = {}
        self.comment_count = ''
        self.next_page = ''
        self.comments_info = {}

    def get_name(self):
        name = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='info']//a[@class='name']").text
        name = name.encode('utf-8', 'ignore')
        self.name = name.decode('utf-8', 'ignore')
        print(self.name)

    def get_content(self):

        content = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//p[@node-type='feed_list_content' and @nick-name]").text
        content = content.encode('utf-8', 'ignore')
        self.content = content.decode('utf-8', 'ignore')
        print(self.content)

    def get_mid(self):

        self.mid = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]").get_attribute("mid")
        print(self.mid)

    def get_forward(self):

        forward = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='card-act']/ul/li[2]").text
        self.forward = re.sub("\D", "", forward)
        print(self.forward)

    def get_like(self):

        like = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='card-act']/ul/li[4]").text
        self.like = re.sub("\D", "", like)
        print(self.like)

    def get_time(self):

        public_time = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='content']/p[@class='from']/a[@target='_blank']").text
        self.public_time = time_fix(public_time)
        print(self.public_time)

    def get_comment_count(self):

        comment_count = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='card-act']/ul/li[3]").text
        self.comment_count = re.sub("\D", "", comment_count)

    def get_user_url(self):

        self.user_url = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='content']//div[@class='info']//a[@class='name' and @nick-name]").get_attribute("href")
        print(self.user_url)
        return self.user_url

    def get_comment_url(self):
        # 当没有评论时，当评论比较少能全显示和评论比较多三种情况
        if self.comment_count == '':
            self.comment_url = "zero"
        else:
            print("click")
            comment_click = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='card-act']/ul/li[3]/a")
            print("click_out")
            comment_click.click()
            time.sleep(1)
            try:
                print("comment_url")
                self.comment_url = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='card-more-a']/a").get_attribute('href')
            except:
                print("comment_url")
                self.comment_url = ''
            print(self.comment_url)
        return self.comment_url

    def get_next_page(self):
        try:
            self.next_page = self.driver.find_element_by_xpath("//a[@class='next' and text()='下一页']").get_attribute('href')

        except Exception as e:
            print(e)
            self.next_page = ''
        return self.next_page

    def get_comment(self):
        if self.comment_url == '':
            comment_index = 0
            comment_text = []
            comment_url = []
            comment_time = []
            brief_intro = []
            mid = []
            name = []
            while(1):
                try:
                    comment_index = comment_index + 1
                    #length = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]").size
                    comment = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='list']/div[@comment_id]["+str(comment_index)+"]//div[@class='txt']").text
                    print("comments", comment)
                    comment_url.append(self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='list']/div[@comment_id]["+str(comment_index)+"]//div[@class='txt']/a").get_attribute('href'))
                    print(comment_url)
                    times = self.driver.find_element_by_xpath("//div[@class='m-wrap']//div[@action-type='feed_list_item' and @mid]["+str(self.index)+"]//div[@class='list']/div[@comment_id]["+str(comment_index)+"]//div[@class='fun']/p").text
                    comment_time.append(time_fix(times))
                    print(comment_time)
                    comment = comment.split("：")   # 中文冒号
                    print(comment)
                    name.append(comment[0])
                    comment_text.append(comment[-1])
                    #print(length)
                    print(comment_index)
                    brief_intro.append('comment')
                    mid.append(self.mid)
                    print("why1")
                except Exception as e:
                    print("why")
                    print(e)
                    break

            self.comments_info['name'] = name
            self.comments_info['content'] = comment_text
            self.comments_info['time'] = comment_time
            self.comments_info['url'] = comment_url
            self.comments_info['brief_intro'] = brief_intro
            self.comments_info['mid'] = mid
            print(self.comments_info)
        return self.comments_info

    def get_blog(self):

        self.get_name()
        self.get_mid()
        self.get_content()
        self.get_like()
        self.get_forward()
        self.get_time()
        self.get_comment_count()
        self.blog['name'] = [self.name]
        self.blog['mid'] = [self.mid]
        self.blog['content'] = [self.content]
        self.blog['forward'] = [self.forward]
        self.blog['time'] = [self.public_time]
        self.blog['url'] = [self.user_url]
        self.blog['like'] = [self.like]
        self.blog['comment_count'] = [self.comment_count]
        return self.blog


if __name__ == "__main__":

    comment = 'MIRACLE_CROWN ： 为啥不把水印去掉'
    comment = comment.split('：')
    print(comment)
    name = comment[0]
    co = comment[-1]
    print(name)
    print(co)
