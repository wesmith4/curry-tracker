import streamlit as st
import plotly.express as px
from sympy import preview
from get_data import get_data
from last_game_report import last_game_report
import pandas as pd
import numpy as np


st.title("Stephen Curry by the numbers")

df = get_data()
# Convert the columns REB, AST, BLK, STL, PF, PTS to int
df[["REB", "AST", "BLK", "STL", "PF", "TO", "PTS"]] = df[["REB", "AST", "BLK", "STL", "PF", "TO", "PTS"]]
# Bar chart of Curry's points over time
fig = px.scatter(df, x="Date", y="PTS", color="Home/Away", title="Points by Date and Locatation")
st.plotly_chart(fig)

fig2 = px.box(df, x="Home/Away", y="3PT_Attempts", color="Result", title="3PT Attempts by Location and Result")
st.plotly_chart(fig2)

fig2a = px.box(df, x="Home/Away", y="3PT_Made", color="Result", title="3PT Made by Location and Result")
st.plotly_chart(fig2a)


# Plot the rebounds
fig3 = px.box(df, x="Result", y="REB", color="Home/Away", title="Rebounds by Location and Result")
st.plotly_chart(fig3)

st.write(df)

avg_points_by_opponent = df.groupby(["Home/Away", "OPP"]).mean()["PTS"].reset_index()

# Bar Chart of points by opponent, bars in decreasing order
fig4 = px.bar(
    avg_points_by_opponent,
    x="OPP",
    y="PTS",
    color="Home/Away",
    category_orders={
        "OPP": [
            x
            for x in list(
                avg_points_by_opponent.groupby("OPP")[["PTS"]]
                .mean()
                .sort_values("PTS", ascending=False)
                .reset_index()
                .loc[:, "OPP"]
            )
        ]
    },
    orientation="v",
    title="Average Points by Opponent",
)
st.plotly_chart(fig4)

last_game_report(df)
