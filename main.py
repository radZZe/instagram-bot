from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import os
import requests
import re
username = "ваш логин"
password = "ваш пороль"


class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        options = Options()
        options.set_preference('dom.webdriver.enabled', False)
        # options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com/')
        time.sleep(random.randrange(4, 6))

        username_input = browser.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(5)
        password_input = browser.find_element_by_name("password")
        password_input.clear()
        password_input.send_keys(password)

        password_input = browser.find_element_by_css_selector('.L3NKy').click()
        time.sleep(10)

    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')

        posts_urls = [item.get_attribute(
            'href') for item in hrefs if "/p/" in item.get_attribute('href')]
        print(posts_urls)

        for url in posts_urls[0:2]:
            try:
                browser.get(url)
                time.sleep(5)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(50, 60))
            except Exception as ex:
                print(ex)
            self.close_browser()

    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    # функция собирает ссылки на все посты пользователя
    def get_all_posts_urls(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute(
                    'href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # функция ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(3)
        browser.get(userpage)
        time.sleep(4)

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:1000]:
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)

                    print(f"Лайк на пост: {post_url} успешно поставлен!")
                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()
    # отписка от пользователей

    def unsubscribe_for_all_users(self, userpage):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        # если количество подписчиков больше 999, убираем из числа запятые
        if ',' in following_count:
            following_count = int(''.join(following_count.split(',')))
        else:
            following_count = int(following_count)

        print(f"Количество подписок: {following_count}")

        time.sleep(random.randrange(2, 4))

        loops_count = int(following_count / 10) + 1
        print(f"Количество перезагрузок страницы: {loops_count}")

        following_users_dict = {}

        for loop in range(1, loops_count + 1):

            count = 10
            browser.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.randrange(3, 6))

            # кликаем/вызываем меню подписок
            following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

            following_button.click()
            time.sleep(random.randrange(3, 6))

            # забираем все li из ul, в них хранится кнопка отписки и ссылки на подписки
            following_div_block = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div")
            following_users = following_div_block.find_elements_by_tag_name("li")
            time.sleep(random.randrange(3, 6))

            for user in following_users:

                if not count:
                    break

                user_url = user.find_element_by_tag_name("a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                # добавляем в словарь пару имя_пользователя: ссылка на аккаунт, на всякий, просто полезно сохранять информацию
                following_users_dict[user_name] = user_url

                following_button = user.find_element_by_tag_name("button").click()
                time.sleep(random.randrange(3, 6))
                unfollow_button = browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]").click()

                print(f"Итерация #{count} >>> Отписался от пользователя {user_name}")
                count -= 1

                # time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(2, 4))

        with open("following_users_dict.txt", "w", encoding="utf-8") as file:
            json.dump(following_users_dict, file)

        self.close_browser()
    # подписка на всех подписчиков данного аккаунта
    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split('/')[-2]

        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(
                f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписичиков!")
            time.sleep(2)

            followers_button = browser.find_element_by_css_selector(
                "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span")
            followers_count = followers_button.text
            if "," in followers_count:
                followers_count = (''.join(followers_count.split(',')))
                followers_count = (''.join(followers_count.split('тыс.')))
                followers_count = int(followers_count.split(' ')[0])
                followers_count = followers_count * 100
            elif " " in followers_count:
                followers_count = (''.join(followers_count.split(' ')))
                followers_count = int(''.join(followers_count.split('.')))
            elif 'тыс.' in followers_count:
                followers_count = (''.join(followers_count.split('тыс.')))
                followers_count = int(followers_count.split(' ')[0])
                followers_count = followers_count * 1000
            else:
                followers_count = int(followers_count.split(' ')[0])

            print("Количество подписчиков " + str(followers_count))

            time.sleep(2)

            loops_count = 100
            #  int(followers_count / 12)
            # if loops_count > 300:
            #     loops_count = 100
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]")
            print(followers_ul)

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name(
                        "a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем подписчиков в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:100000]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt', 'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(
                                            f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                # print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):

                                print(
                                    "Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists(
                                    "/html/body/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"):
                                print(
                                    f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_css_selector(
                                            "#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div > button").click()
                                        print(
                                            f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists("/html/body/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button"):
                                            follow_button = browser.find_element_by_css_selector(
                                                "#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div > div > span > span.vBF20._1OSdk > button").click()
                                            print(
                                                f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                            time.sleep(3)
                                            new_like = browser.find_element_by_css_selector("span.-nal3 > span:nth-child(1)").text
                                            new_like = int(new_like)
                                            browser.find_element_by_css_selector("div.Nnq7C:nth-child(1) > div:nth-child(1)").click()
                                            time.sleep(2)
                                            browser.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()
                                            time.sleep(random.randrange(1, 3))
                                            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a").click()
                                            time.sleep(random.randrange(1, 3))
                                            if new_like >= 3:
                                                loop_new_like = 1
                                                while loop_new_like < 3:
                                                    time.sleep(1)
                                                    loop_new_like = loop_new_like + 1
                                                    browser.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()
                                                    time.sleep(1)
                                                    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
                                                    
                                            else:
                                                browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a").click()
                                                time.sleep(random.randrange(1, 3))
                                                browser.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()
                                        else:
                                            follow_button = browser.find_element_by_css_selector(
                                                "#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div > div > span > span.vBF20._1OSdk > button").click()
                                            print(
                                                f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                            time.sleep(3)
                                            new_like = browser.find_element_by_css_selector("span.-nal3 > span:nth-child(1)").text
                                            new_like = int(new_like)
                                            browser.find_element_by_css_selector("div.Nnq7C:nth-child(1) > div:nth-child(1)").click()
                                            time.sleep(2)
                                            browser.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()
                                            time.sleep(random.randrange(1, 3))
                                            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a").click()
                                            time.sleep(random.randrange(1, 3))
                                            if new_like >= 3:
                                                loop_new_like = 1
                                                while loop_new_like < 3:
                                                    time.sleep(1)
                                                    loop_new_like = loop_new_like + 1
                                                    browser.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()
                                                    time.sleep(1)
                                                    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
                                                    
                                            else:
                                                browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a").click()
                                                time.sleep(random.randrange(1, 3))
                                                browser.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()

                                    except Exception as ex:
                                        print(ex)
                                    # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                    with open(f'{file_name}/{file_name}_subscribe_list.txt', 'a') as subscribe_list_file:
                                        subscribe_list_file.write(user)

                                    time.sleep(random.randrange(8, 12))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()

    def statistics(self, username):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 5))
        posts = browser.find_element_by_css_selector("span.-nal3").text
        posts = int(posts.split(' ')[0])
        print(posts)
        publication = browser.find_element_by_css_selector(
            "div.Nnq7C:nth-child(1) > div:nth-child(1)").click()
        likes = []
        time.sleep(random.randrange(3, 5))
        browser.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button")
        print("не знаю что сделали")
        like = browser.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button").text
        like = int(like.split(' ')[0])
        likes.append(like)
        print(likes)
        nexxt = browser.find_element_by_xpath(
            "/html/body/div[5]/div[1]/div/div/a").click()
        print("не знаю что сделали")
        time.sleep(random.randrange(3, 5))
        print(likes)
        a = 1
        while a < posts:
            if self.xpath_exists("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button"):
                like = browser.find_element_by_xpath(
                    "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button").text
                like = int(like.split(' ')[0])
                likes.append(like)
                a += 1
                print(likes)
                if self.xpath_exists("/html/body/div[5]/div[1]/div/div/a[2]"):
                    nexxt = browser.find_element_by_xpath(
                        "/html/body/div[5]/div[1]/div/div/a[2]").click()
                    print("не знаю что сделали")
                    pass
                else:
                    pass
                time.sleep(random.randrange(4, 6))

            elif self.xpath_exists("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span"):
                browser.find_element_by_xpath(
                    "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span").click()
                print("не знаю что сделали")
                time.sleep(2)
                likes_in_video = browser.find_element_by_xpath(
                    "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/div[4]").text
                like = int(likes_in_video.split(' ')[0])
                likes.append(like)
                a += 1
                print(likes)
                browser.find_element_by_xpath(
                    "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/div[1]").click()
                time.sleep(random.randrange(4, 6))
                if self.xpath_exists("/html/body/div[5]/div[1]/div/div/a[2]"):
                    nexxt = browser.find_element_by_xpath(
                        "/html/body/div[5]/div[1]/div/div/a[2]").click()
                    pass
                else:
                    pass
                time.sleep(random.randrange(4, 6))
                pass

        def listsum(numList):
            theSum = 0
            for i in numList:
                theSum = theSum + i
            return theSum

        print("Количество лайков на странице:" + str(listsum(likes)))
        self.close_browser


print("1-Подписка на подписчиков конкурента")
print("2-Отписка от всех подписок")
print("3-статистика вашего аккаунта(Лайки + подписчики)")


function = input("Выберите одну из функций: ")
if function == "1":
    concurent = input("Вставьте ссылку на конкурента: ")
    my_bot = InstagramBot(username, password)
    my_bot.login()
    my_bot.get_all_followers(concurent)
elif function == "2":
    userpage = input("Введите никнейм вашего аккаунта:")
    my_bot = InstagramBot(username, password)
    my_bot.login()
    my_bot.unsubscribe_for_all_users(userpage)
elif function == "3":
    username = "bot_by_dr"
    password = "danila200342"
    name = input("Введите никнейм вашего аккаунта:")
    my_bot = InstagramBot(username, password)
    my_bot.login()
    my_bot.statistics(name)
