import streamlit as st
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from oafuncs.oa_down.literature import download5doi
import streamlit as st
import tkinter as tk
from tkinter import filedialog
def wenxian(topic,dirname):
    opt = Options()
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
    opt.add_argument("--disable-blink-features=AutomationControlled")
    # opt.add_argument("--headless")
    # opt.add_argument("disbale-gpu")

    web = Chrome(options=opt)
    web.implicitly_wait(10)
    web.get('https://webofscience.clarivate.cn/wos/alldb/basic-search')
    time.sleep(10)
    web.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    time.sleep(3)
    web.find_element(By.XPATH, '//*[@id="snSelectDb"]/button').click()             # //*[@id="snSelectDb"]/button/mat-icon/svg
    web.find_element(By.XPATH, '//*[@id="global-select"]/div[1]/div/div[2]/span').click()
    web.find_element(By.XPATH, '//*[@id="snSelectEd"]/button').click()             # //*[@id="snSelectEd"]/button/mat-icon/svg
    time.sleep(1)
    web.find_element(By.XPATH, '//*[@id="snSelectEd"]/button').click()
    web.find_element(By.XPATH, '//*[@id="snSelectEd"]/button/span[1]').click()
    time.sleep(2)
    el = web.find_element(By.XPATH, '//*[@id="search-option"]')
    el.send_keys(topic, Keys.ENTER)
    web.find_element(By.XPATH, '//*[@id="snSearchType"]/div[3]/button[2]/span[1]').click()
    time.sleep(10)
    # html = web.page_source
    link_href = []
    dois = []
    page = 1
    while page < 3:
        actions = ActionChains(web)
            # 模拟按 "Page Down" 键
        for i in range(30):  # 根据需要的滚动次数来调整循环次数
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            time.sleep(2)  # 每次滚动后等待页面加载


        links = web.find_elements(By.XPATH, '//*[@class="app-records-list"]//h3/a')
        time.sleep(10)
        for link in links:
            link_element = link.get_attribute('href')
            link_href.append(link_element)
        page += 1
        try:
            web.find_element(By.XPATH, '/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-base-summary-component/div/div[2]/app-page-controls[2]/div/form/div/button[2]').click()
        except:
            break

    for link_element in link_href:
        web.get(link_element)
        time.sleep(2)
        try:
            doi = web.find_element(By.XPATH, '//*[@id="FullRTa-DOI"]').text

            download5doi(store_path=dirname, doi_list=doi)
        except Exception as e:
            print(e)
    st.write('已经爬完')


st.title('WOS文献爬取小工具')
topic=st.text_input('请输入与文献相关的topic(英文，Entert提交):',key='input')
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)
st.title('下载路径选择')
st.write('请选择你的下载路径:')
clicked = st.button('选择文件夹')
if clicked:
    dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
    wenxian(topic,dirname)

