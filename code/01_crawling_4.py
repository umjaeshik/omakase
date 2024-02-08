from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import time
import glob
import datetime
import functools
import re
import os
import multiprocessing
functools.lru_cache(maxsize=10000)


proc=[]
def page_schroll():

    num = 0
    schroll_count = 0
    for i in range(300):
        try:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(0.1)
        except:
            continue

        try:

            sample = driver.find_element(By.CLASS_NAME, 'fvwqf')
            if sample:
                driver.execute_script("arguments[0].click();", sample)
                num = 0
                schroll_count += 1
            if schroll_count % 100 == 0:
                print(schroll_count)
        except:
            num += 1
            if num == 1:
                break


def click_element(target):
    sample = res_list.find_element(By.CLASS_NAME, target)
    driver.execute_script("arguments[0].click();", sample)
    time.sleep(0.5)
def change_iframe(target):
    driver.switch_to.default_content()
    iframe_element = driver.find_element(By.ID, target)
    driver.switch_to.frame(iframe_element)
    time.sleep(0.2)
def concat(addr1, addr2):
    print('concat시작')
    last_data = []

    data_paths = glob.glob('../crawling_data/{}_{}_*'.format(addr1,addr2))
    df = pd.DataFrame()
    for path in data_paths:
        df_temp = pd.read_csv(path)
        df_temp.dropna(inplace=True)
        df = pd.concat([df, df_temp])
    if not df.empty:
        # Check if 'keyword' column is present in the DataFrame
        if 'names' in df.columns:
            print(df['names'].value_counts())
        else:
            print("Column 'names' not found in the DataFrame.")

        df.info()
        df.drop_duplicates(subset='names',inplace=True)
        df.info()
        df.to_csv('../{}_{}_음식점_sum.csv'.format(addr1,addr2),index=False)
        print('concat완료')
    else:
        print("DataFrame is empty. No CSV file generated.")

def restaurant_page_down(target_page):
    while(1):
        try:
            pages=driver.find_elements(By.CLASS_NAME,'mBN2s ')
            for page in pages:
                if page.text==str(target_page):
                    driver.execute_script("arguments[0].click();", page)
                    break


            first_restaurant_list = driver.find_elements(By.CLASS_NAME, 'UEzoS')
            action.move_to_element(first_restaurant_list[-1]).perform()
            time.sleep(0.2)
            last_restaurant_list = driver.find_elements(By.CLASS_NAME, 'UEzoS')

            if first_restaurant_list == last_restaurant_list:
                return 0
            else:
                #print('page down')
                continue
        except:
            continue
# f-string
options = Options()
key_count = 0
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('User-Agent=' + user_agent)
options.add_argument('lang=ko_KR')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")


prefs = {'profile.default_content_setting_values': {
    'cookies' : 500, 'images': 0, 'plugins' : 2, 'popups': 2,'geolocation': 2, 'notifications' : 2,
    'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2,
    'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2,
    'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2,
    'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2,
    'durable_storage' : 2}}

options.add_experimental_option('prefs', prefs)
options.add_argument('headless')
options.add_argument("disable-gpu")


addr1_list=['고양시']
addr2_list=['덕이동','가좌동','탄현동','대화동','법곳동''일산동','정발산동','주엽동','마두동','문봉동','백석동','사리현동','마두동'
            ,'장항동','식사동','성석동','마두동','중산동','정발산동','풍동']
#addr2_list=['덕이동','가좌동','탄현동','대화동','법곳동''일산동','정발산동','주엽동','마두동','문봉동','백석동','사리현동','마두동'
 #           ,'장항동','식사동','성석동','마두동','중산동','정발산동','풍동']

options.add_argument('--start-maximized')
while(1):
    try:

        for list1 in addr1_list:

            for list2 in addr2_list:

                concat(list1,list2)
                try:

                    imsi = pd.read_csv('../{}_{}_음식점_sum.csv'.format(list1,list2))
                    print(imsi)
                    res_listed = imsi['names'].to_list()
                    print('res_listed 의 타입',type(res_listed))
                    print(res_listed)
                except:
                    print('파일없음(처음일경우 나옴.)')

                base_url = 'https://map.naver.com/p/search/{} {} 음식점'.format(list1, list2)
                driver = wb.Chrome(options=options)
                # driver.implicitly_wait(0.5)

                try:
                    driver.get(base_url)
                    time.sleep(2)
                except:
                    print('drivet.get')
                    exit(1)
                change_iframe('searchIframe')

                action = ActionChains(driver)

                for page in range(4,5):

                    restaurant_page_down(page)

                    res_lists = driver.find_elements(By.CLASS_NAME, 'UEzoS')
                    print('검색된 음식점 갯수:', len(res_lists))

                    dup_num = 0
                    for res_list in res_lists:  # 식당명 가져와서 리뷰 가져오는 부분
                        change_iframe("searchIframe")

                        try:
                            res_name = res_list.find_element(By.CLASS_NAME, 'TYaxT').text

                        except:
                            print('리스트 반복중 엘레먼트 못가져옴')
                            continue
                        try:
                            if res_name in res_listed:
                                dup_num = dup_num + 1
                                print('중복된 카페 제외', dup_num, res_name)
                                continue
                        except:
                            print('파일없음(처음일경우 나옴).')

                        click_element('tzwk0')
                        time.sleep(1)
                        change_iframe('entryIframe')

                        review_links = driver.find_elements(By.CLASS_NAME, 'tpj9w')
                        for link in review_links:
                            if link.text == '리뷰':
                                driver.execute_script("arguments[0].click();", link)
                            if link.text == '사진':
                                pic_url=link.get_attribute('href')
                                print(pic_url)

                        time.sleep(1)
                        # 아래로 스크롤 후 더보기 클릭 가장 밑으로 내려간후에
                        page_schroll()

                        review_class = driver.find_elements(By.CLASS_NAME, 'xHaT3')
                        print('음식점이름:', res_name, '   리뷰갯수:', len(review_class))
                        text = ' '

                        for idx, r_view in enumerate(review_class):

                            try:
                                sample = r_view.find_element(By.CLASS_NAME, 'rvCSr')
                            except:
                                text = text + ' ' + re.compile('[^가-힣]').sub(
                                    ' ', r_view.find_element(By.CLASS_NAME, 'zPfVt').text)
                                continue

                            driver.execute_script("arguments[0].click();", sample)

                            # time.sleep(0.1)
                            text = text + ' ' + re.compile('[^가-힣]').sub(' ', r_view.find_element(By.CLASS_NAME,
                                                                                                  'zPfVt').text)
                            if idx >500:
                                break


                        print('{} : 리뷰길이 :{}'.format(res_name, len(text)))
                        # xHaT3(리뷰클래스)찾아서 더보기가 있으면 더보기 클릭 없으면 리뷰에 있는 텍스트 가져오기
                        # zPfVt(리뷰)
                        # rvCSr(리뷰더보기)

                        df_list = pd.DataFrame({'names':[res_name],'reviews':text,'addr1':list1,'addr2':list2,
                                                'review_num':len(review_class),'pic_url':pic_url})


                        df_list.to_csv('../crawling_data/{}_{}_음식점_{}_{}.csv'.format(list1, list2, page, res_name),
                                       index=False)
                        print('{}저장완료'.format(res_name))
                driver.close()
                time.sleep(2)

    except Exception as e:

        print('Retry code : ',e)
        try:
            driver.close()
            driver.quit()

        except :
            continue


