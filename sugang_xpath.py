import os, time
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
info = "중요한 사항이니 프로그램을 실행하기 전 꼭 읽어주세요.\n1. 실행된 웹 사이트에 접속하여 로그인해주세요.\n2. 내가 신청하고자 하는 과목을 찾아주세요.\n3. 해당 과목의 신청버튼을 소스보기하여 XPATH를 카피해주세요.\n4. 카피한 XPATH를 프로그램에 입력해주세요.\n5. 실행되는 동안 아무 동작도 하지 마시기 바랍니다."
root = Tk()
root.title("한남대학교 수강신청")
root.resizable(False, False) # 창 크기 변경 불가
chrome_options = ChromeOptions()
def start():
    driver.switch_to.default_content()
    driver.switch_to.frame('frameMain3')
    success = len(driver.find_elements_by_class_name("contb_con01")) # 이미 성공한 과목들의 갯수들 모음
    driver.switch_to.default_content()
    driver.switch_to.frame('frameMain2') #신청할 프레임으로 들어가기
    driver.execute_script("NetFunnel.TS_BYPASS=true;")
    xpath = sub_number.get()
    i=0
    while 1:
        driver.find_element_by_xpath(xpath).click()
        pw = driver.find_element_by_id('rand_num')
        pw_login = driver.find_element_by_name("userInput")
        pw_login.clear()
        pw_login.send_keys(pw.text)
        button = "/html/body/div[2]/div/div[2]/div[3]/button"
        driver.find_element_by_xpath(button).click()
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            message = alert.text
            alert.accept()
            driver.switch_to.default_content()
            driver.switch_to.frame('frameMain3')
            new_success = len(driver.find_elements_by_class_name("contb_con01")) # 이미 성공한 과목들의 갯수들 모음
            driver.switch_to.default_content()
            driver.switch_to.frame('frameMain2') #신청할 프레임으로 들어가기
            if new_success > success:
                print("수강신청 성공")
                break
        except TimeoutException:
            pass
        i+=1
        print(str(i) + "번 반복중")
    list_file.insert(END, "정상 종료 " + str(i) + "번 반복")  
##################################################################################
text_frame = LabelFrame(root, labelanchor="n", text="한남대 수강신청 매크로")
text_frame.pack(fill="x", padx=5, pady=5)
label1 = Label(text_frame, text = info);
label1.pack(fill="x", padx=5, pady=5)

#과목 XPAHT 입력
sub_frame = LabelFrame(root, text="과목 XPAHT", labelanchor="n")
sub_frame.pack(fill="x", padx=5, pady=5, ipady=4)

sub_number = Entry(sub_frame)
sub_number.pack(side="left", expand=1, padx=5, pady=5, ipady=4)

#리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="right", fill="both", expand=1)
scrollbar.config(command=list_file.yview)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

############################################################################################
driver = webdriver.Chrome(r'*****크롬 웹드라이버 경로 *****')
URL = 'http://sugangweb.hannam.ac.kr/sugang/common/loginForm.do'
driver.get(URL)


##################################################################################
root.mainloop()

