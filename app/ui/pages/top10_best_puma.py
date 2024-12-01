import streamlit as st
import fireducks.pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.api_calls import fetch_data_from_api


st.title("Running Puma Shoes Price Analysis")

api_url = "http://0.0.0.0:8200/api/top10-best-puma/"
data = fetch_data_from_api(api_url)

if data:
    st.cache_data.clear()
    df = pd.DataFrame(data)
    df_sorted = df.sort_values(by="price", ascending=True).head(10)

    st.table(df_sorted)

    fig = px.bar(
        df_sorted,
        x="price",
        y="name",
        color="site",
        orientation="h",
        title="Top 10 cheapest product consedering all websites",
        labels={"price": "Price", "name": "Product", "site": "Wbsite"}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('#### Graph and Table Information:')

    st.write(r"""
    The graph above shows the information of the top 10 best Puma sneakers sold on different websites.
    It helps the user to know the cheaper options of puma shoes on the market. 

    The main insights are:

    - The Mercado Livre website has the lowest prices (ranging from 49.99 BRL to 55.4 BRL) for Puma shoes, representing the most affordable option for customers.
    
    - The puma_site, in contrast, hosts the majority of products (9 out of 10), with prices ranging from 119.9 reais to 209.9 reais, indicating that puma_site likely offers more premium options for customers interested in a wider selection, especially running shoes and sportswear
    
    - Tênis Flyer Beta appears twice, suggesting it may be a popular or promotional item. This could indicate that Puma may be offering bulk deals or stocking this model heavily across multiple platforms.
    """)
    
else:
    st.write('No data to show yet.')