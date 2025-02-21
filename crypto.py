import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")


st.title("EDA Cryptocurrency Stats")
about=st.expander("About")
about.markdown('''
This web application retrieves information about top 100 crytocurrencies.\n
**python libraries:** pandas, numpy, matplotlib.\n
**Data source:** [CoinMarketCap.com](https://coinmarketcap.com)
''')

st.write("***")

@st.cache_data
def load_data():
    url="https://coinmarketcap.com"
    html=pd.read_html(url, header=0)
    data=html[0]
    data=pd.DataFrame({"Name":data["Name"],
                       "Price":data["Price"], 
                       "percent_change_1h": data["1h %"], 
                       "percent_change_24h":data["24h %"],
                       "percent_change_7d":data["7d %"], 
                       "Market Cap":data["Market Cap"], 
                       "Volume(24h)":data["Volume(24h)"],
                       "Circulating Supply":data["Circulating Supply"]})
    return data

data=load_data()
col1=st.sidebar
col2, col3=st.columns((2,1))
coin_name=list(data["Name"])

col1.header("Input Options")
seleted_currency=col1.selectbox("Select the currency", ["USD", "INR", "BTC"])
selected_coin=col1.multiselect("Select the coin", coin_name, coin_name)
data=data[data["Name"].isin(selected_coin)]
coin_no=col1.slider("No. of currency", 0,100, 100)
percent_timeframe=col1.selectbox("Percent time change frame", ["1h", "24h", "7d"])


data=data[:coin_no]
col2.subheader("Selected crypto currency")
col2.write("**Dimensions:** "+ str(data.shape[0])+ " rows " + str(data.shape[1]) + " columns")
col2.dataframe(data)

col2.write("***")

col2.subheader("Table of % time change")

timeframe_data=pd.concat([data["percent_change_1h"], data["percent_change_24h"], data["percent_change_7d"]], axis=1)
timeframe_data["percent_change_1h"]=data["percent_change_1h"].str.replace("%", "", regex=True).astype(float)
timeframe_data["percent_change_24h"]=data["percent_change_24h"].str.replace("%","").astype(float)
timeframe_data["percent_change_7d"]=data["percent_change_7d"].str.replace("%", "").astype(float)
timeframe_data['positive_percent_change_1h'] = timeframe_data['percent_change_1h'] > 0
timeframe_data['positive_percent_change_24h'] = timeframe_data['percent_change_24h'] > 0
timeframe_data['positive_percent_change_7d'] = timeframe_data['percent_change_7d'] > 0
timeframe_data=timeframe_data.set_index(data["Name"])

col2.dataframe(timeframe_data)

col3.subheader("Bar plot of % time change")
if (percent_timeframe=="1h"):
    col3.write("Bar plot of 1h timeframe")
    fig, ax=plt.subplots(figsize=(5,25))
    plt.subplots_adjust(top=1, bottom=0)
    timeframe_data["percent_change_1h"].plot(kind="barh", color=timeframe_data["positive_percent_change_1h"].map({True:"g", False:"r"}), ax=ax)
    col3.pyplot(fig)
elif(percent_timeframe=="24h"):
    col3.write("Barplot of 24h timeframe")
    fig, ax=plt.subplots(figsize=(5,25))
    plt.subplots_adjust(top=1, bottom=0)
    timeframe_data["percent_change_24h"].plot(kind="barh", color=timeframe_data["positive_percent_change_24h"].map({True:"g", False:"r"}), ax=ax)
    col3.pyplot(fig)
else:
    col3.write("Barplot of 7d timeframe")
    fig, ax=plt.subplots(figsize=(5,25))
    plt.subplots_adjust(top=1, bottom=0)
    timeframe_data["percent_change_7d"].plot(kind="barh", color=timeframe_data["positive_percent_change_7d"].map({True:"g", False:"r"}), ax=ax)
    col3.pyplot(fig)
