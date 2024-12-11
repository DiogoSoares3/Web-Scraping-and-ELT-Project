import streamlit as st
import fireducks.pandas as pd
import plotly.express as px

from utils.api_calls import fetch_data_from_api


st.title("Running Puma Shoes Price Analysis")

api_url = "http://0.0.0.0:8200/api/metrics/"
data = fetch_data_from_api(api_url)

if data:
    df = pd.DataFrame(data)
        
    st.subheader("Running Puma Shoes price distribution by website")
    
    fig = px.box(
        df,
        x="site",
        y=["min_price", "median_price", "max_price"],
        color="site",
        labels={"value": "Price", "site": "Website"},
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('##### Graph Information:')
    
    st.write("""
    The graph above shows the distribution of minimum, median and maximum prices for Puma sneakers sold on different websites.
    It helps to identify price variations and possible discrepancies. 

    The main insights are:

    - Mercado Livre has the smallest standard deviation (158.02), indicating that its prices are the most consistent and concentrated around the mean.
    
    - Puma webiste has a moderate standard deviation (291.46), reflecting more variability in prices compared to Mercado Livre.
    
    - Mercado Livre has a price range from R$49.99 to R$595.65, with a mean of R$299.42. This site appears to target budget-conscious customers.    
    
    - Puma website has a much wider price range (R$119.90 to R$1,999.90), with a mean of R$592.05, suggesting it caters to a broader audience, including premium segments.
    
    - The Puma Site and Magalu exhibit higher maximum prices (R$1,999.90 and R$1,079.99, respectively), which could be outliers pushing up the mean and increasing the standard deviation. This is evident in the longer upper whiskers in the box plot.
    """)
    
    st.subheader("Average Price by website with confidence interval")
    
    fig = px.bar(
        df,
        x="site",
        y="mean_price",
        error_y="stddev_price",
        color="site",
        labels={"mean_price": "Average Price", "site": "Website"}
    )

    st.plotly_chart(fig, use_container_width=True)
    st.table(df[["site", "mean_price", "stddev_price"]].rename(columns={"site": "Website", "mean_price": "Average Price", "stddev_price": "Standard Deviation"}))
    
    st.markdown('#### Graph Information:')
    
    st.write(r"""
    The graph above shows the distribution of average prices by website for Puma sneakers sold on different websites.
    It helps to identify price variations and possible discrepancies. 

    The main insights are:

    - The Puma wbsite has the highest standard deviation, which may indicate a wide range of prices, from budget options to premium products.
    
    - For Mercado Livre website, the typical range would be 134.60 reais to 391.12 reais (262.86 ± 128.26). This shows that most prices are concentrated in this range, while Puma website has a much wider range.
    
    - Mercado Livre and Magalu websites seems to focus on a more uniform and lower purchasing power, while Puma website offers prices for different consumer segments.
    """)

    fig.show()
    
else:
    st.write("No data to show yet.")