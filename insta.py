# coding=utf-8
from selenium import webdriver
import time
import datetime
import pandas as pd

browser = webdriver.Chrome(r"C:\Users\user\Documents\instagram.parser\chromedriver.exe")

#Вход в аккаунт
def login(login, password):
    browser.get("https://www.instagram.com")

    time.sleep(4)

    browser.find_element_by_xpath("//section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input").send_keys(login) #Путь к полю с никнеймом юзера в браузере
    browser.find_element_by_xpath("//section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input").send_keys(password) #Путь к полю с паролем юзера в браузере
    browser.find_element_by_xpath("//section/main/article/div[2]/div[1]/div/form/div[4]/button").click()

    time.sleep(3)

#Чтение постов аккаунтов
def read_posts(links):
    all_posts = []

    for link in links:
        browser.get(link)

        #Начальная прокрутка, плавная прокрутка постов
        i = 0
        while i < 2:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            i += 1
        
        #чтение списка постов
        posts = browser.find_elements_by_xpath('//body/div[1]/section/main/div/div[3]/article//a')

        d = []
        for i in posts:
            d.append(i.get_attribute('href'))
        
        #чтение каждого поста
        x = 0
        while x < len(d):
            one_post = []

            browser.get(d[x])
            time.sleep(3)

            #дата сбора информации
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            one_post.append(date)

            #ссылка на профиль
            link = browser.find_element_by_xpath('//header/div[2]/div[1]/div[1]/a').get_attribute('href') #ссылка на профиль
            one_post.append(link)

            views = 0 #кол-во просмотров видео
            likes = 0 #кол-во лайков
            try:
                views = browser.find_element_by_xpath('//section/main/div/div[1]/article/div[2]/section[2]/div/span/span').text #кол-во просмотров видео
                browser.find_element_by_xpath('//section/main/div/div[1]/article/div[2]/section[2]/div/span').click() #открываем попап числа лайков
                time.sleep(1)
                likes = browser.find_element_by_xpath('//section/main/div/div[1]/article/div[2]/section[2]/div/div/div[4]/span').text
            except:
                likes = browser.find_element_by_xpath('//section/main/div/div[1]/article/div[2]/section[2]/div/div/button/span').text
            #time.sleep(3)

            #ссылка на публикацию
            link_post = browser.current_url 
            one_post.append(link_post)

            #дата поста
            date_post = browser.find_element_by_xpath('//section/main/div/div[1]/article/div[2]/div[2]/a/time').get_attribute('title')
            one_post.append(date_post)

            one_post.append(likes)
            one_post.append(views)

            all_posts.append(one_post)

            x += 1
    return all_posts
    
login("ann_mihailovaa", "52ecgSS7%")

accounts = open("list_of_links.txt").readlines()

all_posts = read_posts(accounts)
print(all_posts)

columns = ['дата сбора информации','ссылка на профиль', 'ссылка на пост', 'дата поста', 'кол-во лайков', 'кол-во просмотров видео']

df = pd.DataFrame(all_posts, columns=columns)
df.to_csv(r'df.csv')
print(df)
