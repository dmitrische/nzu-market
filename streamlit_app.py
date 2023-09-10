import streamlit as st
import pandas as pd
from functions import gbm_forecast

st.markdown("<h1 style='text-align: left; color: green;'>NZU price forecasting App</h1>", unsafe_allow_html=True)

st.write("")

source='./price-data-scrape/nzu_price_raw_data.csv'
df = pd.read_csv(source, index_col='date', parse_dates=[0])
df.drop(columns=['url'], inplace=True)

start_date = pd.to_datetime('2013-9-1')
df = df.loc[(df.index > start_date)]

df_w = df.resample('W').mean()
df_w.ffill(inplace=True)

slider = st.select_slider(label = 'Date',
                 options = df_w.index,
                 value = (df_w.index[0], df_w.index[-1]),
                 format_func = lambda x: x.strftime(' %d/%m/%Y ') # is this legit?
                 )

fig = gbm_forecast(df=df_w,
                   tscale = 'weeks',
                   nsteps = 261,
                   ymax = 300,
                   nsims = 10,
                   date_range = slider
                   )

st.pyplot(fig)
