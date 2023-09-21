import streamlit as st
import pandas as pd
from functions import gbm_forecast
from pathlib import Path

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


st.markdown("<h1 style='text-align: left; color: black;'>Carbon price forecasting</h1>", unsafe_allow_html=True)
st.write("")

summary = read_markdown_file('summary.md')
st.markdown(summary)
st.write("")

start_date = pd.to_datetime('2013-9-12')

df_choice = st.sidebar.selectbox(label = 'Use dropdown to select commodity:',
                         options = ('New Zealand Units (NZUs)',
                                    'European Union Allowances (EUAs)'
                                    ),
                         index = 0)

if(df_choice == 'New Zealand Units (NZUs)'):
    
    source='./price-data-scrape/nzu_price_raw_data.csv'
    df = pd.read_csv(source, index_col='date', parse_dates=[0])
    df.drop(columns=['url'], inplace=True)
    currency = 'NZD'
    
elif(df_choice == 'European Union Allowances (EUAs)'):
    
    source='./EUdata/eua_price_history.csv'
    df = pd.read_csv(source, index_col='date', parse_dates=[0])
    df.drop(columns=['volume'], inplace=True)
    currency = 'EUR'
    
else:
    pass

df = df.loc[(df.index > start_date)]
df = df.resample('W').mean()
df.ffill(inplace=True)

st.sidebar.divider()

date_slider = st.sidebar.select_slider(label = 'Use slider to select date range for fitting:',
                                       options = df.index,
                                       value = (df.index[0], df.index[-1]),
                                       format_func = lambda x: x.strftime(' %d/%m/%Y ')
                                       )

st.sidebar.divider()

seed_input = st.sidebar.number_input(label = 'Enter integer random seed for MCMC:',
                                     min_value = 1,
                                     step = 1,
                                     value = 1
                                     )
st.sidebar.divider()

nsims_input = st.sidebar.number_input(label = 'Enter number of MCMC simulations:',
                                       min_value = 1,
                                       max_value = 50,
                                       step = 1,
                                       value = 10
                                       )

fig = gbm_forecast(df = df,
                   tscale = 'weeks',
                   nsteps = 261,
                   ymax = 200,
                   nsims = nsims_input,
                   date_range = date_slider,
                   style = 'ggplot',
                   show_title = False,
                   rand_seed = seed_input,
                   currency = currency
                   )

st.pyplot(fig)

st.markdown("<h3 style='text-align: left; color: black;'>Forecast interpretation</h3>", unsafe_allow_html=True)
st.write("")
interp = read_markdown_file('interpretation.md')
st.markdown(interp)

st.markdown("<h3 style='text-align: left; color: black;'>Modelling details</h3>", unsafe_allow_html=True)
st.write("")
methods = read_markdown_file('modelling.md')
st.markdown(methods)

st.markdown("<h3 style='text-align: left; color: black;'>Data sources</h3>", unsafe_allow_html=True)
st.write("")
sources = read_markdown_file('data_sources.md')
st.markdown(sources)
