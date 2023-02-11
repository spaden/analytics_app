from flask import Flask, request, jsonify
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

app = Flask(__name__)


def address_Addition(address1,new_df):
    address_list = address1.split(',')
    new_df['address'] = address_list[0]
    new_df['city'] = address_list[1]
    return new_df

def get_review_summary(result_set):
    rev_dict = {'Review Name': [],
        'Review Text' : []}
    for result in result_set:
        review_name = result.find(class_='d4r55').text
        review_text = result.find('span',class_='wiI7pd').text
        rev_dict['Review Name'].append(review_name)
        rev_dict['Review Text'].append(review_text)
     
    return(pd.DataFrame(rev_dict))


def scrape_util(url):
    driver = webdriver.Chrome("D:\softwares\chromedriver.exe")
    
    driver.get(url)
    time.sleep(5)

    # Finding the address of the location
    response = BeautifulSoup(driver.page_source, 'html.parser')
    address = response.find('div',class_= 'rogA2c').text
    driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]').click()
    time.sleep(3)
    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    number = 0

    while True:
        number = number+1

        # Scroll down to bottom

        #old_==ele = driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        ele = driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')
        driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

        # Wait to load page

        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        #print(f'last height: {last_height}')

        ele = driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')

        new_height = driver.execute_script("return arguments[0].scrollHeight", ele)

        #print(f'new height: {new_height}')

        if new_height == last_height:
            break

        #print('cont')
        last_height = new_height
    next_item = driver.find_elements('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]')
    time.sleep(3)

    for i in next_item:
        button = i.find_elements(By.TAG_NAME,'button')
        for m in button:
            if m.text == "More":
                m.click()
        time.sleep(5)

    response = BeautifulSoup(driver.page_source, 'html.parser')
    next_2 = response.find_all('div',class_ = 'jftiEf')


    df = get_review_summary(next_2)
    
    df1 = df.copy()
    final_df = address_Addition(address,df1)
    
    return 'Completed'




@app.route('/test')
def index():
    return scrape_util('https://www.google.com/maps/place/Tim+Hortons/@43.7607366,-79.5321831,14z/data=!4m10!1m2!2m1!1stim+hortons!3m6!1s0x882b31d93eab2809:0xa9ea7bb65f9da6ec!8m2!3d43.7607366!4d-79.4992241!15sCgt0aW0gaG9ydG9ucyIDiAEBWg0iC3RpbSBob3J0b25zkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F1vyxk0xz')
    
   

@app.route("/getSimilarQuote", methods=['POST'])
def postTest():
    data = request.json
    
    remove_noise(data['userInput'])
    Xt = vectorizer.fit_transform([data['userInput']])
    
    mod_Pt = [0 for i in range(0, 500)]

    for i in range(len(Xt.toarray()[0])):
        mod_Pt[i] = Xt.toarray()[0][i]
    pred_group =  savedModel.predict([mod_Pt])[0]   
    pred_group_list = quotes_data[str(pred_group)]
    return {'res': random.choice(pred_group_list)}



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = '8002')
