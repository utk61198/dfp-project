import streamlit as st
import pandas as pd
import functions
st.set_page_config(layout='wide')
# st.snow()
st.title("Soccer Space")
col1, col2,col3,col4 = st.tabs(["Team","Player","Twitter","Bet odds"])
with col1:
    # with st.expander("Team"):
    team_df = pd.read_csv("results.csv")
    st.title("Select Team")
    teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
    team = st.selectbox("Select an option", teams)
    st.metric("Win", functions.get_win_count(team,team_df))
    st.metric("Loss", functions.get_loss_count(team,team_df))
    st.metric("Draw", functions.get_draw_count(team,team_df))
    last_5_matches = functions.get_last_5_matches(team, team_df)
    st.title("Last 5 Matches")
    st.table(last_5_matches[['home_team', 'home_score', 'away_score', 'away_team']].reset_index(drop=True))
with col2:
    st.write("Player")
with col3:
    teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
    team = st.selectbox("Select a tweet", teams)
    api = functions.authenticate_tweepy()
    tweets = api.search_tweets(q=f'"FIFA World Cup" {team}',lang='en',result_type = 'popularity',count=500)
    for tweet in tweets[:10]:
        st.write(tweet.text)
        st.markdown("""---""")
    sentiment = functions.tweets_sentiment_score(tweets)
    # st.slider(value=sentiment,label="Tweets Sentiment",disabled=True,min_value=-1.0,max_value=1.0,step=0.01)
    st.progress(int(sentiment*50+50))

with col4:
    st.write("Odds")