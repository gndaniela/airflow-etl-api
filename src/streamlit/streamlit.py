import base64
import os
import streamlit as st
from PIL import Image
from postgres_cli import (
    PostgresCli,
    card_content_ada,
    card_content_btc,
    card_content_eth,
)

post_cli = PostgresCli("postgresql+psycopg2://airflow:airflow@postgres:5432/daniela")

icon = Image.open(os.path.dirname(__file__) + "/img/coin.png")

# Screen size config
st.set_page_config(layout="wide", page_title="Cryptos Dashboard", page_icon=icon)
st.set_option("deprecation.showPyplotGlobalUse", False)

file_ = open(os.path.dirname(__file__) + "/img/currency.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


def main():
    st.sidebar.title("Building a data system with Airflow")
    scol1, scol2, scol3 = st.sidebar.columns(3)
    with scol1:
        st.write(" ")
    with scol2:
        st.sidebar.markdown(
            f"""<p align="center">
                              <img src="data:image/gif;base64,{data_url}" />
                              </p>""",
            unsafe_allow_html=True,
        )
    with scol3:
        st.write(" ")
    st.sidebar.write("API data source: www.alphavantage.co")
    st.title("Cryptos Dashboard")
    colbtc, coleth, colada = st.columns(3)
    with colbtc:
        st.markdown(
            card_content_btc("BTC", "Bitcoin", post_cli.get_last_value("BTC")),
            unsafe_allow_html=True,
        )
    with coleth:
        st.markdown(
            card_content_eth("ETH", "Ethereum", post_cli.get_last_value("ETH")),
            unsafe_allow_html=True,
        )
    with colada:
        st.markdown(
            card_content_ada("ADA", "Cardano", post_cli.get_last_value("ADA")),
            unsafe_allow_html=True,
        )
    st.write(" ")
    st.write(" ")
    ## Date range selector
    start_date, end_date = post_cli.get_maxmin_date()
    date_slider = st.slider(
        "Select date to analyze",
        min_value=start_date,
        value=[start_date, end_date],
        max_value=end_date,
        format="MMM DD, YYYY",
    )
    # date_slider
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Open", "Close", "High", "Low", "Volume", "All"]
    )
    with tab1:
        st.subheader("Open")
        post_cli.plot_lines("open", date_slider[0], date_slider[1])
    with tab2:
        st.subheader("Close")
        post_cli.plot_lines("close", date_slider[0], date_slider[1])
    with tab3:
        st.subheader("High")
        post_cli.plot_lines("high", date_slider[0], date_slider[1])
    with tab4:
        st.subheader("Low")
        post_cli.plot_lines("low", date_slider[0], date_slider[1])
    with tab5:
        st.subheader("Volume")
        post_cli.plot_lines("volume", date_slider[0], date_slider[1])
    with tab6:
        st.subheader("All")
        post_cli.plot_all("BTC", date_slider[0], date_slider[1], "Bitcoin")
        post_cli.plot_all("ETH", date_slider[0], date_slider[1], "Ethereum")
        post_cli.plot_all("ADA", date_slider[0], date_slider[1], "Cardano")

    st.markdown(
        """<div style="text-align: right"> <em>ITBA - Cloud Data Engineering | TP3 | Daniela García Nistor</em> </div>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
