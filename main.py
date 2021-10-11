from re import T
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import io
from PIL import Image
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import time
import numpy as np
import plotly.express as px
import datetime

st.write("""
# TOYOKOU Works
*Test!*
""")  

placeholder0 = st.empty()
placeholder1 = st.empty()
placeholder6 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()

#streamlit run c:\Users\nissh\OneDrive\デスクトップ\EV\esp32\調整用\Streamlit\main.py



def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet("Test") 
    return worksheet

jsonf = "gspread-test-323309-74a00bc35193.json"
spread_sheet_key = "15QFzP2mnyo36nGmwGIttfap5z7WbUGmjdX5TLRgWl-A"
ws = connect_gspread(jsonf,spread_sheet_key)

v_list = ws.col_values(3)
v_list_f = [float(s) for s in v_list]
c_list = ws.col_values(2)
c_list_f = [float(s) for s in c_list]
w_list = ws.col_values(4)
w_list_f = [float(s) for s in w_list]
thou_c_list_f = [int(1000*s) for s in c_list_f]
start_time = str(ws.acell('A1').value)
dt1 = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
time_list = ws.col_values(1)

sum1 = 0
current_sum_list = []
for i in range(len(c_list_f)):
    date = datetime.datetime.strptime(time_list[i-1], '%Y/%m/%d %H:%M:%S')
    delta = date - dt1
    date_seconds = delta.seconds
    sum1 = sum1 + thou_c_list_f[i-1]
    if i == 0:
        ave1 = sum1
    else:
        ave1 = sum1/i
    cursum = ave1*(date_seconds/3600)
    current_sum_list.append(cursum/1000)
#index = []
 
#i = 1


while True:

    one_list = ws.col_values(1)
    rows_index = len(one_list)
    values_list = ws.row_values(rows_index)

    v_value = float(values_list[2])
    if v_value < 1000:
        continue
    c_value = float(values_list[1])
    w_value = float(values_list[3])
    lat_value = values_list[4]
    lng_value = values_list[5]
    end_time = str(values_list[0])
    dt2 = datetime.datetime.strptime(end_time, '%Y/%m/%d %H:%M:%S')
    time_difference = dt2 - dt1
    date_seconds = time_difference.seconds

    v_list_f.append(v_value)
    c_list_f.append(c_value)
    w_list_f.append(w_value)
    thou_c_list_f.append(int(c_value*1000))

    sum1 = sum(thou_c_list_f)
    ave1 = sum1/rows_index
    print(date_seconds)
    print(ave1)
    cursum = ave1*(date_seconds/3600)
    current_sum_list.append(cursum/1000)
    
    #index.append(i)

    

    data_dic = {
        '電圧': v_list_f,
        '電流': c_list_f,
        '電力': w_list_f
    }
    v_data = {
        '電圧': v_list_f
    }
    c_data = {
        '電流': c_list_f
    }
    w_data = {
        '電力': w_list_f
    }
    sum_c_data = {
        '電圧': v_list_f,
        '積算電流': current_sum_list
    }
    df = pd.DataFrame(data=data_dic)
    df_v = pd.DataFrame(data=v_data)
    df_c = pd.DataFrame(data=c_data)
    df_w = pd.DataFrame(data=w_data)
    df_s = pd.DataFrame(data=sum_c_data)


    #dat = np.random.rand(20, 4)
    #dfi = pd.DataFrame(dat, columns=['base', 'soc,', 'bas', 'golf',])
    #dfi.index.name = 'Time'

    
    BASE_URL = "https://maps.googleapis.com/maps/api/staticmap?"

    API_KEY = "AIzaSyAXN7tv_HFIsBNjON6ieR2PYazdxpystY4"

    POSITION = str(lat_value) + "%2C" + str(lng_value)
    ZOOM = 18

    URL1 = BASE_URL + "center=" + POSITION + "&markers=size%3Amid%7Ccolor%3Apurple%7Clabel%3AE%7C" + POSITION + "&zoom=" + str(ZOOM) + "&format=jpg&scale=2&size=600x600&key=" + API_KEY

    print(POSITION)
    print(URL1)

    file = io.BytesIO(requests.get(URL1).content)
    img = Image.open(file)

    with placeholder0:
        st.write("""
        ## 経過時間
        """)  
        st.write(time_difference)
        st.write("積算：" + str(int(cursum/1000)) + " mAh")

    with placeholder1:
        st.image(img)
    with placeholder6:
        st.write(
            px.scatter(df_s, x='積算電流', y='電圧', title='放電曲線')
        )
    
    with placeholder2:
        st.write(
            px.line(df, title="Mix")
        )
    with placeholder3:
        st.write(
            px.line(df_c, title="電流")
        )
    with placeholder4:
        st.write(
            px.line(df_v, title="電圧")
        )
    with placeholder5:
        st.write(
            px.line(df_w, title="電力")
        )
    time.sleep(2.0)
    #i += 1

    
