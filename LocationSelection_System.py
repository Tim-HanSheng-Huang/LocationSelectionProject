#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

location_spot=pd.read_csv("location_spot.csv")
location_MRT=pd.read_csv("location_MRT.csv")
location_MALL=pd.read_csv("location_MALL.csv")
location_school=pd.read_csv("location_school.csv")
population_density_byli=pd.read_csv("population_density.csv",encoding='Big5')
rent_data=pd.read_csv("台北市店面租賃交易行情107108109.csv",encoding="Big5")

data=pd.read_csv("all_merge_euclidean.csv",encoding='Big5')


# In[2]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.utils import shuffle

# Build the random forest model
forest_model=RandomForestClassifier(n_estimators=100,random_state=87,max_depth=4)

X=data[['MRT_count_1000','mall_distance1000','school_distance1000','spot_distance_2000','人口密度','租金']]
y=data["選址成功"]

forest_model.fit(X,y)


# In[3]:


import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
options = webdriver.ChromeOptions()
options.add_argument("headless")

# get coordinate and li (village,里) by web crawling
def get_coordinateandli(addr):
    browser = webdriver.Chrome(executable_path='chromedriver.exe',options=options)
    browser.get("http://www.map.com.tw/")
    search = browser.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
    time.sleep(1)    
    iframe = browser.find_elements_by_tag_name("iframe")[2]
    browser.switch_to.frame(iframe)
    
    addr_detail = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[1]/td/table/tbody/tr[4]/td").text
    index_before = addr_detail.find('區')
    index_after = addr_detail.find('里')
    li = addr_detail[index_before+1:index_after]
    # print(li)
    
    coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    coor_btn.click()
    coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    log = coor[0].split("：")[-1]
    browser.quit()
    # print(lat, log)
    
    return li, lat, log


# In[4]:


import math

def count_MRT1000(myX,myY):
    mrt_num=0
    for i in range(len(location_MRT)):
        MRT_location=location_MRT.iloc[i,4].split(",")
        MRTX=float(MRT_location[1])
        MRTY=float(MRT_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-MRTX),2)+math.pow((myY-MRTY)*110.574,2))
        if d<=1:
            mrt_num=mrt_num+1
    return mrt_num

def count_mall1000(myX,myY):
    mall_num=0
    for i in range(len(location_MALL)):
        MALL_location=location_MALL.iloc[i,3].split(",")
        MALLX=float(MALL_location[1])
        MALLY=float(MALL_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-MALLX),2)+math.pow((myY-MALLY)*110.574,2))
        if d<=1:
            mall_num=mall_num+1
    return mall_num

def count_school1000(myX,myY):
    school_num=0
    for i in range(len(location_school)):
        school_location=location_school.iloc[i,4].split(",")
        schoolX=float(school_location[1])
        schoolY=float(school_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-schoolX),2)+math.pow((myY-schoolY)*110.574,2))
        if d<=1:
            school_num=school_num+1
    return school_num

def count_spot2000(myX,myY):
    spot_num=0
    for i in range(len(location_spot)):
        spot_location=location_spot.iloc[i,4].split(",")
        spotX=float(spot_location[1])
        spotY=float(spot_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-spotX),2)+math.pow((myY-spotY)*110.574,2))
        if d<=2:
            spot_num=spot_num+1
    return spot_num


# In[5]:


def get_population_density(li):
    li+="里"
    index=population_density_byli[population_density_byli["里名"]==li].index.values
    index=int(index)
    return population_density_byli.iloc[index][2]


# In[6]:


def get_rent_cost(myX,myY):
    
    rent_X=rent_data["經度"]
    rent_Y=rent_data["緯度"]
    distance=[]
    
    for j in range(len(rent_data)):
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-rent_X[j]),2)+math.pow((myY-rent_Y[j])*110.574,2))
        distance.append(d)
        
    first=distance.index(min(distance))
    distance[first]=100
    
    second=distance.index(min(distance))
    distance[second]=100
    
    third=distance.index(min(distance))
    distance[third]=100
    
    cost=(rent_data.iloc[first,5]+rent_data.iloc[second,5]+rent_data.iloc[third,5])/3
    return cost


# In[7]:


def goanalysis():
    
    current_show.config(text="正在分析中...")
    li_show.config(text="")
    MRT_show.config(text="")
    mall_show.config(text="")
    school_show.config(text="")
    spot_show.config(text="")
    popden_show.config(text="")
    renocost_show.config(text="")
    final_pred_show.config(text="")
    final_lab_show.config(text="")
    win.update()
    
    address=address_entry.get()
    
    li,coordinateY,coordinateX=get_coordinateandli(address)
    coordinateY=float(coordinateY)
    coordinateX=float(coordinateX)
    
    lishow_text="位置："+address+"("+li+")"
    li_show.config(text=lishow_text)
    
    MRT_count_1000=count_MRT1000(coordinateX,coordinateY)
    mrtshow_text="1000m內捷運站數量："+str(MRT_count_1000)
    MRT_show.config(text=mrtshow_text)
    
    mall_count_1000=count_mall1000(coordinateX,coordinateY)
    mallshow_text="1000m內商場數量："+str(mall_count_1000)
    mall_show.config(text=mallshow_text)
    
    school_count_1000=count_school1000(coordinateX,coordinateY)
    schoolshow_text="1000m內學校數量："+str(school_count_1000)
    school_show.config(text=schoolshow_text)
    
    spot_count_2000=count_spot2000(coordinateX,coordinateY)
    spotshow_text="2000m內景點數量："+str(spot_count_2000)
    spot_show.config(text=spotshow_text)
    
    population_density=get_population_density(li)
    popudenshow_text="人口密度（每平方公里）："+str(round(population_density,2))
    popden_show.config(text=popudenshow_text)
    
    rent_cost=get_rent_cost(coordinateX,coordinateY)
    rentcost_text="粗估租金（每平方公尺）："+str(round(rent_cost,2))
    renocost_show.config(text=rentcost_text)
    
    X_query=np.array([MRT_count_1000,mall_count_1000,school_count_1000,spot_count_2000,population_density,rent_cost])
    outcome=forest_model.predict_proba(X_query.reshape(1, -1))
    final_lab_show.config(text="開店成功預測(Predicted Probability)")
    outcome_text=str(round(outcome[0][1]*100,2))+"%"
    final_pred_show.config(text=outcome_text)
    
    current_show.config(text="分析結果")

# layout
from tkinter import*
import time
win=Tk()
win.title("Handshake Beverage Stores Location Selection")
win.geometry("800x600+800+200")

topic_lab=Label(text="手搖飲料店選址分析")
topic_lab.config(font="微軟正黑體 24 bold underline")
topic_lab.place(x=35,y=30)

input_remind=Label(text="請輸入欲開店地址")
input_remind.config(font="微軟正黑體 12")
input_remind.place(x=35,y=100)

input_example=Label(text="（格式如：台北市大安區羅斯福路四段1號）")
input_example.config(font="微軟正黑體 12")
input_example.place(x=200,y=100)

address_entry=Entry()
address_entry.config(font="微軟正黑體 15")
address_entry.place(x=35,y=140,width=500)

btn_analysis=Button(text="ANALYSIS!!",command=goanalysis)
btn_analysis.config(font="微軟正黑體 12")
btn_analysis.place(x=600,y=110,width=150,height=60)

current_show=Label(text="")
current_show.config(font="微軟正黑體 12")
current_show.place(x=35,y=200)

li_show=Label(text="")
li_show.config(font="微軟正黑體 12")
li_show.place(x=35,y=240)

MRT_show=Label(text="")
MRT_show.config(font="微軟正黑體 12")
MRT_show.place(x=35,y=280)

mall_show=Label(text="")
mall_show.config(font="微軟正黑體 12")
mall_show.place(x=35,y=320)

school_show=Label(text="")
school_show.config(font="微軟正黑體 12")
school_show.place(x=35,y=360)

spot_show=Label(text="")
spot_show.config(font="微軟正黑體 12")
spot_show.place(x=35,y=400)

popden_show=Label(text="")
popden_show.config(font="微軟正黑體 12")
popden_show.place(x=35,y=440)

renocost_show=Label(text="")
renocost_show.config(font="微軟正黑體 12")
renocost_show.place(x=35,y=480)

final_lab_show=Label(text="")
final_lab_show.config(font="微軟正黑體 12")
final_lab_show.place(x=450,y=240)

final_pred_show=Label(text="")
final_pred_show.config(font="微軟正黑體 55 underline")
final_pred_show.place(x=450,y=280)

win.mainloop()

