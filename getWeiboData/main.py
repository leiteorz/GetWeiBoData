import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


# 将页面向下滑动px像素
def scroll_page(px):
    driver.execute_script("window.scrollTo(0, {});".format(px))

# 更新href列表
def refresh_href_list(href_element_list):
    hrefList.clear()
    for href_element in href_element_list:
        href = ""
        try:
            href = href_element.get_attribute("href")
        except:
            href = ""
        finally:
            hrefList.append(href)

# 访问微博实时页
def visit_weibo_live_page():
    # 访问微博页
    driver.get("https://weibo.com/mygroups?gid=110007800021953")
    # sleep 2s 确保网页能够加载完毕
    sleep(2)
    # 点击实时按钮, 切换到实时微博
    driver.find_elements(By.CSS_SELECTOR, ".wbpro-textcut")[1].click()
    # sleep 5s 确保网页能够加载完毕
    sleep(5)

# 初始化一开始的item list
def init_item_list():
    like_count_element_list = driver.find_elements(By.CSS_SELECTOR, ".woo-like-count")
    wb_content_element_list = driver.find_elements(By.CSS_SELECTOR, ".woo-content")
    come_from_element_list = driver.find_elements(By.CSS_SELECTOR, ".head-info_cut_1tPQI.head-info_source_2zcEX")
    time_element_list = driver.find_elements(By.CSS_SELECTOR, ".head-info_time_6sFQg")

    # 刷新href列表
    refresh_href_list(time_element_list)
    # 点赞数
    for item in like_count_element_list:
        if item.text == "赞":
            likeCountList.append("0")
        else:
            likeCountList.append(item.text)
    # 微博内容
    for item in wb_content_element_list:
        wbContentList.append(item.text)
    # 来自哪里
    for item in come_from_element_list:
        comeFromList.append(item.text[4::])
    # 时间
    for item in time_element_list:
        # 时间列表加进去
        if item.text == "刚刚" or item.text == "刚刚点赞" or item.text == "刚刚互动":
            current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            timeList.append(current_time)
        else:
            timeList.append(item.text)

# 加入新的item
def add_new_item(like_count_element_item, wb_content_element_item, time_element_item, come_from_element_item):
    like_count = ""
    wb_content = ""
    time_text = ""
    come_from_text = ""
    try:
        # 点赞数
        like_count = like_count_element_item.text
        if like_count == "赞":
            like_count = "0"
        # 微博内容
        wb_content = wb_content_element_item.text
        if wb_content is None:
            wb_content = "null"
        # 时间
        time_text = time_element_item.text
        if time_text == "刚刚" or time_text == "刚刚点赞" or time_text == "刚刚互动":
            time_text = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        # 来自哪里
        come_from_text = come_from_element_item.text[4::]
    except:
        like_count = "0"
        wb_content = "null"
        time_text = "1999-01-01 00:00"
        come_from_text = "北京"
    finally:
        timeList.append(time_text)
        likeCountList.append(like_count)
        wbContentList.append(wb_content)
        comeFromList.append(come_from_text)

# 打印数据
def print_item_list():
    total_count = len(wbContentList)
    for i in range(total_count):
        print("发布时间:" + timeList[i] +  "\n发布地点:" + comeFromList[i] + "\n微博内容:\n" + wbContentList[i] + "\n点赞数:" + likeCountList[i] + "\n")


# 拿到浏览器对象
driver = webdriver.Chrome()
# 访问微博实时页
visit_weibo_live_page()

# 需要的data list
hrefList = []   # 微博的具体href, 只是当前item list的, 不保存总的
timeList = [] # 时间
likeCountList = []  # 点赞数
wbContentList = []  # 微博内容
comeFromList = [] # 来自哪里

# 初始化: 把初始的item list填充进去
init_item_list()

# 向下滑动100条微博的像素值
for i in range(200):
    scroll_page(i * 450)
    # 等待3s加载时间
    sleep(3)
    # 获取新的href list
    newHrefList = driver.find_elements(By.CSS_SELECTOR, ".head-info_time_6sFQg")
    # 获取新的item list
    newLikeCountList = driver.find_elements(By.CSS_SELECTOR, ".woo-like-count")
    newWbContentList = driver.find_elements(By.CSS_SELECTOR, ".detail_wbtext_4CRf9")
    newComeFromList = driver.find_elements(By.CSS_SELECTOR, ".head-info_cut_1tPQI.head-info_source_2zcEX")
    newTimeList = driver.find_elements(By.CSS_SELECTOR, ".head-info_time_6sFQg")
    # 通过比较href判断是否有新的item
    for j in range(len(newHrefList)):
        currentHref = ""
        # 这里得捕获异常, 防止href拿不到
        try:
            currentHref = newHrefList[j].get_attribute("href")
        except:
            currentHref = ""
        finally:
            if currentHref not in hrefList:
                # 表示是新的item, 加入列表中
                add_new_item(newLikeCountList[j], newWbContentList[j], newTimeList[j], newComeFromList[j])
    # 更新href list
    refresh_href_list(newHrefList)

print_item_list()

sleep(500)
