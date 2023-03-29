from dynamic import create_driver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from settings import *
from datetime import datetime


# PROXY
def read_proxy_file():
    data = open('proxy.txt', 'r').read().split('\n')
    proxies = [{'host': i.split(":")[0], 'port': i.split(":")[1], 'login':
                i.split(":")[2], 'password': i.split(":")[3]} for i in data]
    return proxies

# useragent
def get_useragent():
    file = open('useragent.txt', 'r').read().split('\n')
    return file[randint(0, len(file)) - 1]


def search_ad(driver, wait):
    """Поиск нужного объявления"""

    search_status = False
    cicle = 0
    while search_status == False:
        cicle += 1
        time.sleep(SLEEP)
        try:
            elements = driver.find_elements(
                By.XPATH, f'//*[contains(text(),"{KEY_PHRASE}")]')

            if len(elements) > 0:
                element = elements[0]
                element.click()
                search_status = True
         
            if search_status == False:
                time.sleep(SLEEP)
                
                next_page_el = (By.XPATH, '//span[@data-marker="pagination-button/next"]')
                next_page = wait.until(EC.presence_of_element_located(next_page_el))
                next_page.click()
                time.sleep(SLEEP)
                    
            else:
                break
            
        except Exception as e:
            break
        
        if cicle > 10:
            break
    
    
    # переходим на послежнюю открытую вкладку
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    
    return search_status


def visit_others_ad(driver):
    """Посещение сторонних объявлений"""

    cicle = 1  # кол-во посещаемых левых объявления
    
    time.sleep(SLEEP)
    while cicle <= 3:
        
        try:
            # все объявления на странице
            elements = driver.find_elements(
            By.XPATH, '//a[@data-marker="item-title"]')
            
            if len(elements) > 0:

                # ссылка на рандомное обхеяление
                element = elements[randint(0, len(elements))]
                time.sleep(SLEEP/2)
                
                # скрол до объявления (из за этого вылетает с ошибкой)
                # driver.execute_script("arguments[0].scrollIntoView();", element)
                # time.sleep(SLEEP)
                
                element.click()
                time.sleep(SLEEP)
                
                driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
                time.sleep(SLEEP + 3)
                
                # скрол страницы
                
                n = 0  # на сколько сдвигаемся на странице
                while n < 10:
                    driver.execute_script(f'window.scrollBy(0, {randint(70, 120)})')
                    time.sleep(SLEEP/3)
                    n += 1
                
                n = 0  # на сколько сдвигаемся на странице
                while n < 10:
                    driver.execute_script(f'window.scrollBy(0, -{randint(70, 100)})')
                    time.sleep(SLEEP/3)
                    n += 1
                
                time.sleep(randint(TIME_AWAIT_OTHER_AD_FROM, TIME_AWAIT_OTHER_AD_TO))
                
                driver.switch_to.window(driver.window_handles[0])
                
                time.sleep(SLEEP)
        except Exception as e:
            pass

        cicle += 1
    
    driver.switch_to.window(driver.window_handles[0])


def action_on_ad(driver, wait):
    """Действия на странице нужного объявлние"""
    
    time.sleep(SLEEP * 2)
    
    try:
        # скрол страницы
        n = 0  # сколько сдвигаемся на странице
        while n < 5:
            driver.execute_script(f'window.scrollBy(0, {randint(60, 160)})')
            time.sleep(SLEEP/3)
            n += 1
    except Exception as e:
        pass
        
    # --- карта
    
    try:
        map = driver.find_elements(By.XPATH, "//*[contains(text(),'Показать карту')]")
        if len(map) > 0:
            map[0].click() 
            
    except Exception as e:
        pass
    
    # ---
    
    time.sleep(SLEEP*10)
    
    try:
        n = 0  # сколько сдвигаемся на странице
        while n < 5:
            driver.execute_script(f'window.scrollBy(0, -{randint(60, 130)})')
            time.sleep(SLEEP/3)
            n += 1
    except Exception as e:
        pass
    
    
    try:
        # добавляем в избранное
        add_to_favorite = driver.find_elements(
                By.XPATH, '//button[@data-marker="item-view/favorite-button"]')
        if (len(add_to_favorite) > 0):
            add_to_favorite[1].click()
    except Exception as e:
        pass
    
    # --- телефон
    
    try:
        phone_btn = driver.find_element(By.XPATH, '//button[@data-marker="item-phone-button/card"]')
        phone_btn.click()
        
        time.sleep(SLEEP*5)
        # закрываем попап
        close_btn = driver.find_element(By.XPATH, '//svg[@data-marker="item-popup/close"]')
        close_btn.click()
    except Exception as e:
        pass
    
    time.sleep(SLEEP*3)
    
    # ---
    
    try:
        # скрол страницы
        n = 0  # сколько сдвигаемся на странице
        while n < 10:
            driver.execute_script(f'window.scrollBy(0, {randint(60, 160)})')
            time.sleep(SLEEP/3)
            n += 1
    except Exception as e:
        pass
    
   
    # сидим на странице
    time.sleep(randint(TIME_AWAIT_AD_FROM, TIME_AWAIT_AD_TO))


def bot(proxy: str, useragent: str):
    """Инициализация бота для посещения авито"""

    driver = create_driver(proxy=proxy, useragent=useragent, headless=False)

    driver.get('https://avito.ru/')
    time.sleep(SLEEP)
    wait = WebDriverWait(driver, SLEEP)

    # поиск инпута для ввода запроса и воод запроса
    element = (By.XPATH, '//input[@data-marker="search-form/suggest"]')
    input_search = wait.until(EC.presence_of_element_located(element))
    input_search.send_keys(TEXT_REQUEST)

    time.sleep(SLEEP/2)

    # нажатие на кнопку поиск
    element = (By.XPATH, '//button[@data-marker="search-form/submit-button"]')
    button_search = wait.until(EC.presence_of_element_located(element))
    button_search.click()

    # посещаем левые обхявления
    # только на первой странице так как потом будет сложно найти нужное
    visit_others_ad(driver)

    # находим нужное объявлние
    status = search_ad(driver, wait)
    
    # если объявление нашли
    if status:
        # совершаем дейсттвия на странице
        action_on_ad(driver, wait)
        log(str(f'OK - {proxy}'))
    else:
        log(str(f'ERROR - {proxy}'))
    
    # закрывает браузер
    driver.quit()


def log(msg):
    """Логируем данные"""
    
    with open('log.txt', 'a+') as log_file:
        log_file.write(f'[{datetime.now()}]: ' + msg + "\n")

def main():
    # получаем прокси
    proxies = read_proxy_file()

    if len(proxies) > 0:
        for proxy in proxies:

            proxy_ = f"{proxy['login']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"

            try:
                bot(proxy=proxy_, useragent=get_useragent())

                time.sleep(
                    randint(SLEEP_BEETWEEN_PROXY[0], SLEEP_BEETWEEN_PROXY[1]))  # сон
            except Exception as e:
                log(str(f'ERROR - {proxy_}'))
                
    else:
        print("Нет прокси или txt заполнен не верно")


main()
