import streamlit as st


def last_game_report(df):

    st.write("## Last Game Report")

    # Get the last game
    last_game = df.tail(1)
    opp = last_game.iloc[0]["OPP"]
    day = last_game.iloc[0]["Date"]
    home_away = last_game.iloc[0]["Home/Away"]
    readable_day = day.strftime("%B %d, %Y")

    # Get the second last game
    last_game_2 = df.iloc[[-2]]

    # Get the second to last row of df
    # second_to_last_game = df.iloc[-2]

    # st.write(second_to_last_game)

    st.write(
        f"""On {readable_day}, Stephen Curry and the Golden State Warriors played {'at home against' if home_away == "Home" else "an away game at"} {opp}. The result was  a {last_game.iloc[0]['Result'].__str__().lower()}, where Golden State scored {last_game.iloc[0]['Winner_Score' if last_game.iloc[0]['Result'] == 'Win' else 'Loser_Score']} and {opp} scored {last_game.iloc[0]['Loser_Score' if last_game.iloc[0]['Result'] == 'Win' else 'Winner_Score']}."""
    )

    st.write("### Curry's Stats:")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Points", int(last_game.iloc[0]["PTS"]), int(last_game.iloc[0]["PTS"] - last_game_2.iloc[0]["PTS"]))
    col2.metric("Rebounds", int(last_game.iloc[0]["REB"]), int(last_game.iloc[0]["REB"] - last_game_2.iloc[0]["REB"]))
    col3.metric("Assists", int(last_game.iloc[0]["AST"]), int(last_game.iloc[0]["AST"] - last_game_2.iloc[0]["AST"]))
    col4.metric("Steals", int(last_game.iloc[0]["STL"]), int(last_game.iloc[0]["STL"] - last_game_2.iloc[0]["STL"]))
    col5.metric("Blocks", int(last_game.iloc[0]["BLK"]), int(last_game.iloc[0]["BLK"] - last_game_2.iloc[0]["BLK"]))
    col6.metric(
        "Turnovers", int(last_game.iloc[0]["TO"]), int(last_game.iloc[0]["TO"] - last_game_2.iloc[0]["TO"]), "inverse"
    )
