from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


class PostgresCli:
    def __init__(self, conn_url):
        self.conn_url = conn_url
        self.engine = create_engine(self.conn_url, echo=False)

    def get_maxmin_date(self):
        q = text("SELECT MIN(date), MAX(date) from crypto_data")
        result = self.engine.execute(q)
        mindate = None
        maxdate = None

        for i in result:
            mindate = i[0]
            maxdate = i[1]
        # print('Min value : ',mindate)
        # print('Max value : ',maxdate)
        return mindate, maxdate

    def get_last_value(self, symbol):
        q = text(
            f"SELECT close from crypto_data WHERE date = (SELECT MAX(date) FROM crypto_data) AND symbol = '{symbol}'"
        )
        result = self.engine.execute(q)
        last_close = None
        for i in result:
            last_close = i[0]
        return last_close

    def get_all_data(self):
        q = text("SELECT date,symbol,open,close,high,low,volume from crypto_data")
        result = self.engine.execute(q)
        df_from_records = pd.DataFrame.from_records(
            result, columns=["date", "symbol", "open", "close", "high", "low", "volume"]
        )
        return df_from_records

    def plot_lines(self, column: str, min_date, max_date):
        diff = max_date - min_date
        diff = diff.days
        df = self.get_all_data()
        df = df.pivot(index="date", columns="symbol", values=column).reset_index()
        df = df[(df["date"] >= min_date) & (df["date"] <= max_date)]
        # plot

        fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["BTC"],
                line_color="rgba(255,193,7,0.6)",
                mode="lines+markers",
                showlegend=True,
                name="Bitcoin",
            ),
            row=1,
            col=1,
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["ETH"],
                line_color="rgba(111,66,193,0.6)",
                mode="lines+markers",
                showlegend=True,
                name="Ethereum",
            ),
            row=2,
            col=1,
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["ADA"],
                line_color="rgba(232,62,140,0.6)",
                mode="lines+markers",
                showlegend=True,
                name="Cardano",
            ),
            row=3,
            col=1,
            secondary_y=False,
        )

        fig.update_layout(
            legend_traceorder="normal",
            hovermode="x unified",
            yaxis_tickformat="D1",
            title=f"Evolution - Period: last {diff} days",
        )
        return st.write(fig)

    def plot_all(self, symbol: str, min_date, max_date, title):
        df = self.get_all_data()
        df = df[(df["date"] >= min_date) & (df["date"] <= max_date)]
        # plot
        fig = px.line(
            df[df.symbol == symbol],
            x="date",
            y=["open", "close", "high", "low"],
            hover_data={"date"},
            title=title,
            markers=True,
            color_discrete_sequence=["#45afcc", "#8045cc", "#16c919", "#cf5615"],
            template="simple_white",
        )
        return st.write(fig)


def card_content_ada(header, body, value):
    return (
        f"<style>div.card{{background-color:rgba(232,62,140,0.6);border-radius: 5px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s;}}</style>"
        '<div class="card">'
        '<div class="container">'
        f"<h3 style='text-align:center; color:rgba(108, 117, 125, 1)'><b>{header}</b></h3>"
        f"<p style='text-align:center; color:rgba(108, 117, 125, 1)'>{body}</p>"
        f"<p style='text-align:center; color:rgba(108, 117, 125, 1)'>Current value (USD): <b>{value}</b></p>"
        "</div></div>"
    )


def card_content_eth(header, body, value):
    return (
        f"<style>div.card1{{background-color:rgba(111,66,193,0.6);border-radius: 5px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s;}}</style>"
        '<div class="card1">'
        '<div class="container">'
        f"<h3 style='text-align:center; color:rgba(108, 117, 125, 1)'><b>{header}</b></h3>"
        f"<p style='text-align:center; color:rgba(108, 117, 125, 1)'>{body}</p>"
        f"<p style='text-align:center; color:rgba(108, 117, 125, 1)'>Current value (USD): <b>{value}</b></p>"
        "</div></div>"
    )


def card_content_btc(header, body, value):
    return (
        f"<style>div.card2{{background-color:rgba(255,193,7,0.6);border-radius: 5px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s;}}</style>"
        '<div class="card2">'
        '<div class="container">'
        f"<h3 style='text-align:center; color:rgba(108, 117, 125, 1)'><b>{header}</b></h3>"
        f"<p style='text-align:center; color:rgba(108, 117, 125, 1)'>{body}</p>"
        f"<p style='text-align:center; color:rgba(108, 117, 125, 1)'>Current value (USD): <b>{value}</b></p>"
        "</div></div>"
    )
