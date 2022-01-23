import requests as rq
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import re

TEAM_LINKS_URL = "http://www.espn.com/nba/players"

team_links_page = rq.get(TEAM_LINKS_URL).text
team_links_soup = BeautifulSoup(team_links_page, 'html.parser')

# Get all the links to the player pages

# Find all li > div > a tags
lists = team_links_soup.find_all('ul', {"class": "small-logos"})


teams = []

for list in lists:
    # Get all the list items
    list_items = list.find_all('li')
    for item in list_items:
        # Get the first <a>
        a = item.find('a')
        # Get the href
        href = a.get('href')
        # Replace "team" with "roster" in the href
        href = href.replace("team", "team/roster")
        # Remove all text after and including the last "/"
        href = href[: href.rfind("/")]

        team_code = href.split("name/")[1].split("/")[0].upper()

        # Append the team object to the list
        teams.append({"team": team_code, "url": href})
# print(team_urls)

players = []

# In each team_url, get the player urls
for team in teams:
    roster = rq.get(team.get("url")).text
    roster_soup = BeautifulSoup(roster, 'html.parser')
    d = roster_soup.find('tbody')
    rows = d.find_all('tr')
    for row in rows:
        # Find the second <a>
        a = row.find_all('a')[1]
        # Get the anchor text
        anchor_text = a.get_text()
        # Get the href
        href = a.get('href')
        # Replace "player" with "player/gamelog" in the href
        href = href.replace("player", "player/gamelog")
        # Add a player object to players
        players.append({"name": anchor_text, "url": href, "team": team.get("team")})

# Convert players to a dataframe
players_df = pd.DataFrame(players)
players_df['option_label'] = players_df.apply(lambda x: f"{x['name']} ({x['team']})", axis=1)

# Export the dataframe to a csv
players_df.to_csv("players.csv", index=False)
