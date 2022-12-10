import streamlit as st
import pandas as pd
import functions

st.set_page_config(layout='wide')

col1, col2 = st.columns(2)


with col1:
    with st.expander("Team"):
        # team_name = st.text_input("Enter a team name")
        team_df = pd.read_csv("results.csv")
        # st.dataframe(pd.read_csv("results.csv"))
        st.title("Select Team")
        teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
        team = st.selectbox("Select an option", teams)
        # col_inner_1, col_inner_2, col_inner_3 = st.columns(3)
        st.metric("Win", functions.get_win_count(team,team_df))
        st.metric("Loss", functions.get_loss_count(team,team_df))
        st.metric("Draw", functions.get_draw_count(team,team_df))
        last_5_matches = functions.get_last_5_matches(team, team_df)
        st.title("Last 5 Matches")
        st.table(last_5_matches[['home_team', 'home_score', 'away_score', 'away_team']].reset_index(drop=True))
    with st.expander("Twitter"):
        st.write("twitter")
with col2:
    with st.expander("Player"):
        st.write("player")
    
    with st.expander("Betting odds"):
        st.write("ods")