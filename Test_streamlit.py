#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 22:40:06 2022

@author: satoshi_matsuno
"""

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px

st.title("UBER pikeups in NYC")


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    
    return data


data_load_state=st.text("Loading data....")
data=load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

st.bar_chart(hist_values)

data[DATE_COLUMN].dt.hour

fig = px.histogram(data[DATE_COLUMN].dt.hour, x=DATE_COLUMN)
st.plotly_chart(fig)

st.subheader('Map of all pickups')
st.map(data)

values = st.slider(
     'Select a range of values',
     0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)
hour_to_filter = st.slider('How old are you?', 0, 23, 17)
filtered_data=data[data[DATE_COLUMN].dt.hour==hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


