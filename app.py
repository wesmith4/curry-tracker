import streamlit as st
import plotly.express as px
import pandas as pd
from get_data import get_data
from last_game_report import last_game_report

st.set_page_config(page_title="NBA Player Stats", layout="centered")


@st.cache
def get_players():
    return pd.read_csv("./players.csv")


players = get_players()


# In players, get the index of the row where "name" is "Stephen Curry"
curry_index = players.index[players["name"] == "Stephen Curry"].tolist()[0]

which_player = st.selectbox("Which player?", players["option_label"], index=curry_index)

selected_player_object = dict(players[players["name"] == which_player.split(" (")[0]].iloc[0])

st.title(f"{selected_player_object.get('name')} by the numbers")

if which_player:
    df = get_data(selected_player_object.get("url"))
    # Convert the columns REB, AST, BLK, STL, PF, PTS to int
    df[["REB", "AST", "BLK", "STL", "PF", "TO", "PTS"]] = df[["REB", "AST", "BLK", "STL", "PF", "TO", "PTS"]]

    last_game_report(df, selected_player_object)

    """
    ## 2021-2022 Season Trends
    """

    # Bar chart of Curry's points over time
    fig = px.scatter(df, x="Date", y="PTS", color="Home/Away", title="Points")
    st.plotly_chart(fig)

    sep_by_result = st.checkbox("Separate by Win/Loss", value=False)

    points_box = px.box(df, x="Home/Away", y="PTS", title="Points", color="Result" if sep_by_result else None)
    st.plotly_chart(points_box)

    threes_attempts = px.box(
        df,
        x="Home/Away",
        y="3PT_Attempts",
        color="Result" if sep_by_result else None,
        title="3PT Attempts",
    )
    st.plotly_chart(threes_attempts)

    threes_made = px.box(
        df,
        x="Home/Away",
        y="3PT_Made",
        color="Result" if sep_by_result else None,
        title="3PT Made",
    )
    st.plotly_chart(threes_made)

    # Plot the rebounds
    reb = px.box(df, x="Home/Away", y="REB", color="Result" if sep_by_result else None, title="Rebounds")
    st.plotly_chart(reb)

    # Plot the assists
    ast = px.box(df, x="Home/Away", y="AST", color="Result" if sep_by_result else None, title="Assists")
    st.plotly_chart(reb)

    # Plot the blocks
    blk = px.box(df, x="Home/Away", y="BLK", color="Result" if sep_by_result else None, title="Blocks")
    st.plotly_chart(blk)

    # Plot the steals
    stl = px.box(df, x="Home/Away", y="STL", color="Result" if sep_by_result else None, title="Steals")
    st.plotly_chart(stl)

    avg_points_by_opponent = df.groupby(["Home/Away", "OPP"]).mean()["PTS"].reset_index()

    # Bar Chart of points by opponent, bars in decreasing order
    by_opp = px.bar(
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
    st.plotly_chart(by_opp)
