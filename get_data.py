import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import re
import streamlit as st


@st.cache
def get_data(url="https://www.espn.com/nba/player/gamelog/_/id/3975/stephen-curry"):

    month_names_lowercase = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    # Get the data from the game log
    game_log = rq.get(url).text

    soup = BeautifulSoup(game_log, 'html.parser')

    # Find all tables that contain columns "Date", "OPP", and "PTS"

    all_tables = soup.find_all('table')

    master = pd.DataFrame()

    # Iterate through all the tables in reverse

    for table in all_tables[::-1]:
        # Import the first table into a df
        df = pd.read_html(str(table))[0]
        cols = df.columns.tolist()
        # If the df does not have columns "Date", "OPP", and "PTS", skip it
        if "Date" not in cols or "OPP" not in cols or "PTS" not in cols:
            continue
        # Remove all rows where the "Date" column is in month_names_lowercase
        df = df[~df["Date"].str.lower().isin(month_names_lowercase)]

        # In the Date column, remove the first 4 characters of all values
        df["Date"] = df["Date"].str[4:]
        df["Date"] = df["Date"].apply(lambda x: x + "/2021" if len(x.split("/")[0]) == 2 else x + "/2022")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Home/Away"] = df.OPP.apply(lambda x: "Home" if "vs" in x else "Away")
        df["Win/Loss"] = df.Result.apply(lambda x: "Win" if "W" in x else "Loss")

        df["3PT_Attempts"] = df["3PT"].apply(lambda x: int(x.split("-")[1]) if x != "-" else 0)
        df["3PT_Made"] = df["3PT"].apply(lambda x: int(x.split("-")[0]) if x != "-" else 0)

        score_regex = r'\d+-\d+'
        df["Score"] = df.Result.apply(lambda x: re.findall(score_regex, x)[0])
        df["Winner_Score"] = df.Score.apply(lambda x: int(x.split("-")[0]))
        df["Loser_Score"] = df.Score.apply(lambda x: int(x.split("-")[1]))
        df.drop(columns=["Result", "Score"], inplace=True)
        df.rename(columns={"Win/Loss": "Result"}, inplace=True)

        df.OPP = df.OPP.apply(lambda x: x.replace("vs", "").replace("@", "").strip())
        df = df.sort_values(by="Date", ascending=True)
        master = master.append(df)

    master.reset_index(inplace=True, drop=True)

    return master
