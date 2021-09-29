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

st.write("""
# TOYOKOU Works
*Test!*
""")  

placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()

#streamlit run c:/Users/nissh/OneDrive/デスクトップ/MyPython/KivyTest/streamlit_roop.py



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
c_list = ws.col_values(2)
w_list = ws.col_values(4)
#index = []

#i = 1

while True:

    one_list = ws.col_values(1)
    rows_index = len(one_list)
    values_list = ws.row_values(rows_index)

    v_value = values_list[2]
    c_value = values_list[1]
    w_value = values_list[3]
    lat_value = values_list[4]
    lng_value = values_list[5]

    v_list.append(v_value)
    c_list.append(c_value)
    w_list.append(w_value)
    #index.append(i)

    data_dic = {
        '電圧': v_list,
        '電流': c_list,
        '電力': w_list
    }
    v_data = {
        '電圧': v_list
    }
    c_data = {
        '電流': c_list
    }
    w_data = {
        '電力': w_list
    }
    df = pd.DataFrame(data=data_dic)
    df_v = pd.DataFrame(data=v_data)
    df_c = pd.DataFrame(data=c_data)
    df_w = pd.DataFrame(data=w_data)
    print(df)


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

    with placeholder1:
        st.image(img)
    
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

    
