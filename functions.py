# Importing necessary libraries
import pandas as pd
import tweepy
import re
import statistics
from textblob import TextBlob
from bs4 import BeautifulSoup
from bs4 import Comment
import requests
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# return the win,loss, draw count for a selected team.
def get_count(team_name, matches, wld):
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2018-01-01']
    df = df[df['date'] < '2022-11-20']
    if wld == 'win':
        home = df[(df['home_team'] == team_name) & (df['home_score'] > df['away_score'])]
        away = df[(df['away_team'] == team_name) & (df['away_score'] > df['home_score'])]
    elif wld == 'draw':
        home = df[(df['home_team'] == team_name) & (df['home_score'] == df['away_score'])]
        away = df[(df['away_team'] == team_name) & (df['away_score'] == df['home_score'])]
    elif wld == 'loss':
        home = df[(df['home_team'] == team_name) & (df['home_score'] < df['away_score'])]
        away = df[(df['away_team'] == team_name) & (df['away_score'] < df['home_score'])]
    count = len(home) + len(away)
    return count


# Returns the results of the last 5 matches played by a team
def get_last_5_matches(team_name, matches):
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date', ascending=False)
    team_matches = df[(df['home_team'] == team_name) | (df['away_team'] == team_name)]
    last_5_matches = team_matches.iloc[:5]
    return last_5_matches

# Code to authenticate against the Twitter open source free API - tweepy
def authenticate_tweepy():
    consumer_key="20QCtfjScHSWfzohGhGjYUs7w"
    consumer_secret="Z3tIfmpILNB4kYJIQ7Q1Omg54Ru90mxsCdTz8Yki69010C2EcG"
    access_token="1138374206750482433-UnrC2n2zjvpbMQ0cIMlibTKPfB8s1Q"
    access_token_secret="ExSHUpNT06wYPRL7DvZMIhihWTSpfXiyR633AgQfScCMF"
    auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return api

# Data cleaning on the fetched tweets using regex
def preprocessTweets(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())

# Calculating the sentiment of a set of fetched tweets
def tweets_sentiment_score(tweets):
    total_sentiment = []
    for tweet in tweets:
        analysis=TextBlob(preprocessTweets(tweet))
        total_sentiment.append(analysis.sentiment.polarity)
    print(total_sentiment)
    total_sentiment = [i for i in total_sentiment if i != 0]
    return statistics.mean(total_sentiment)

# Scrapes the draftkings website to fetch latest odds about upcoming matches
def draftKings(): 
    odds1 = []
    odds2 = []
    teams1 = []
    teams2 = []
    url = "https://sportsbook.draftkings.com/leagues/soccer/world-cup-2022"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_odds = soup.find_all("span", class_="sportsbook-odds american default-color")
    for i in range(0,len(all_odds),3):
        odds1.append(all_odds[i].get_text().strip()) 
        odds2.append(all_odds[i+2].get_text().strip())
    all_teams = soup.find_all("span", class_="sportsbook-outcome-cell__label")
    for i in range(0,len(all_teams),3):
        teams1.append(all_teams[i].get_text().strip()) 
        teams2.append(all_teams[i+2].get_text().strip())
    teams_odds = pd.DataFrame({'team1':teams1,'odds1':odds1,'team2':teams2,'odds2':odds2})
    all_links = soup.find_all("a", class_="sportsbook-event-accordion__title")
    hrefs = [title["href"] for title in all_links]
    httpslinks = []
    for i in range(0,len(hrefs)):
        httpslinks.append('https://sportsbook.draftkings.com'+hrefs[i])
    return teams_odds, httpslinks


# Scrapes the betfair website to fetch latest odds about upcoming matches
def betFair():
    odds1 = []
    odds2 = []
    teams1 = []
    teams2 = []
    url = "https://www.betfair.com/sport/football/fifa-world-cup/12469077"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_odds1 = soup.find_all("li", class_="selection sel-0")
    for i in range(len(all_odds1)):
        if i%2!=0:
            odds1.append(all_odds1[i].get_text().strip()) 
    all_odds2 = soup.find_all("li", class_="selection sel-2")
    for i in range(len(all_odds2)):
        odds2.append(all_odds2[i].get_text().strip()) 
    all_teams = soup.find_all("span", class_="team-name")
    for i in range(len(all_teams)):
        if i%2==0:
            teams1.append(all_teams[i].get_text().strip())
        else:
            teams2.append(all_teams[i].get_text().strip())
    teams_odds = pd.DataFrame({'team1':teams1,'odds1':odds1,'team2':teams2,'odds2':odds2})
    all_links = soup.find_all("a", class_="ui-nav markets-number-arrow ui-top event-link ui-gtm-click")
    hrefs = [title["href"] for title in all_links]
    httpslinks = []
    for i in range(0,len(hrefs),len(teams_odds)):
        httpslinks.append('https://www.betfair.com/'+hrefs[i])
    return teams_odds, httpslinks


# Scrapes the betus website to fetch latest odds about upcoming matches
def betUS():
    odds1 = []
    odds2 = []
    teams1 = []
    teams2 = []
    url = "https://www.betus.com.pa/sportsbook/soccer/fifa-world-cup/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_odds1 = soup.find_all("div", class_="g-ln col-3 col-lg-2 p-0 border-left-0 line-container")
    for i in range(4,len(all_odds1),5):
        odds1.append(all_odds1[i].get_text().strip()) 
    all_odds2 = soup.find_all("div", class_="g-ln col-3 p-0 col-lg-2 line-container border-bottom-0")
    for i in range(1, len(all_odds2),2):
        odds2.append(all_odds2[i].get_text().strip())
    all_teams1 = soup.find_all("span", id="awayName")
    for i in range(0, len(all_teams1),2):
        teams1.append(all_teams1[i].get_text().strip())
    all_teams2 = soup.find_all("span", id="homeName")
    for i in range(0, len(all_teams2),2):
        teams2.append(all_teams2[i].get_text().strip())
    teams_odds = pd.DataFrame({'team1':teams1,'odds1':odds1,'team2':teams2,'odds2':odds2})
    all_links = soup.find_all("a", id="lnkMarkets")
    hrefs = [title["href"] for title in all_links]
    httpslinks = []
    for i in range(0,len(hrefs),len(teams_odds)):
        httpslinks.append('https://www.betus.com.pa'+hrefs[i])

    return teams_odds, httpslinks


# Scrapes the wynnbet website to fetch latest odds about upcoming matches
def wynnBet():
    odds1 = []
    odds2 = []
    teams1 = []
    teams2 = []
    url = "https://va.wynnbet.com/competition/19401175"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    all_odds = soup.find_all("span", class_="odd ml-1")
    
    for i in range(0,len(all_odds),3):
        odds1.append(all_odds[i].get_text().strip()) 
        odds2.append(all_odds[i+2].get_text().strip())
    all_teams = soup.find_all("div", class_="teamName") 
    for i in range(0, len(all_teams),2):
        teams1.append(all_teams[i].get_text().strip())
        teams2.append(all_teams[i+1].get_text().strip())
    teams_odds = pd.DataFrame({'team1':teams1,'odds1':odds1,'team2':teams2,'odds2':odds2})
    all_links = soup.find_all("span", class_="wager")
    httpslinks = []
    for link in all_links:
        tag = link.find('a')
        httpslinks.append('https://va.wynnbet.com'+tag.get('href'))

    return teams_odds, httpslinks

# Scrapes a website to build a dataframe containing statistics of all players
def player_stats_df():
    url = 'https://fbref.com/en/share/bhMcv'
    r=requests.get(url)
    table = pd.read_html(r.text)
    df = pd.DataFrame(table[0])
    df.index.to_flat_index()
    new_df = pd.DataFrame(df[[('Unnamed: 1_level_0','Player'), ( 'Unnamed: 3_level_0','Squad'), ('Performance','Gls'), ('Performance','Ast')]])
    new_df.columns=['Player','Team','Goals','Assists']
    new_df.sort_values(by=['Goals','Assists'], inplace=True, ascending=(False))
    new_df['Team'] = new_df['Team'].str[3:]
    new_df['Team'] = new_df['Team'].apply(lambda x: x.strip())
    detailed_df = df[[
    ( 'Unnamed: 1_level_0',   'Player'),
    ( 'Unnamed: 2_level_0',      'Pos'),
    ( 'Unnamed: 3_level_0',    'Squad'),
    ( 'Unnamed: 4_level_0',      'Age'),
    ( 'Unnamed: 5_level_0',     'Club'),
    ( 'Unnamed: 6_level_0',     'Born'),
    (       'Playing Time',       'MP'),
    (       'Playing Time',   'Starts'),
    (       'Playing Time',      'Min'),
    (       'Playing Time',      '90s'),
    (        'Performance',      'Gls'),
    (        'Performance',      'Ast'),
    (        'Performance',     'G-PK'),
    (        'Performance',       'PK'),
    (        'Performance',    'PKatt'),
    (        'Performance',     'CrdY'),
    (        'Performance',     'CrdR'),
    (     'Per 90 Minutes',      'Gls'),
    (     'Per 90 Minutes',      'Ast'),
    (     'Per 90 Minutes',      'G+A'),
    (           'Expected',       'xG'),
    (           'Expected',      'xAG'),
    ]]
    detailed_df.columns=['Player','Position(s)','Team','Age','Club','DOB','Matches Played','Starts','Minutes Played','90s','Goals','Assists','Non-Penalty Goals','Penalty Goals','Penalty Kicks Attempted','Yellow Cards','Red Cards','Goals per 90','Assists per 90','G+A per 90','Expected Goals','Expected Assists']
    detailed_df['Team'] = detailed_df['Team'].str[3:]
    detailed_df['Team'] = detailed_df['Team'].apply(lambda x: x.strip())
    return detailed_df, new_df

# Returns a scatterplot all players' goals and minutes played with a selected player highlighted on the plot
def goals_vs_minutesplayed_player(p):
    detailed_df = player_stats_df()[0]
    fig = px.scatter(detailed_df, x="Minutes Played", y="Goals")
    trace = next(fig.select_traces())
    n = len(trace.x)
    index = detailed_df.index[detailed_df['Player'] == p]
    k = index[0]
    color = [trace.marker.color] * n
    color[k] = "red"
    size = [8] * n
    size[k] = 15
    symbol = [trace.marker.symbol] * n
    symbol[k] = "star"
    fig.update_traces(marker=dict(color=color, size=size, symbol=symbol))
    return fig

# Returns a scatterplot all players' goals and assists with a selected player highlighted on the plot
def goals_vs_assists_player(p):
    detailed_df = player_stats_df()[0]
    fig = px.scatter(detailed_df, x="Assists", y="Goals")
    trace = next(fig.select_traces())
    n = len(trace.x)
    index = detailed_df.index[detailed_df['Player'] == p]
    k = index[0]
    color = [trace.marker.color] * n
    color[k] = "red"
    size = [8] * n
    size[k] = 15
    symbol = [trace.marker.symbol] * n
    symbol[k] = "star"
    fig.update_traces(marker=dict(color=color, size=size, symbol=symbol))
    return fig


# Returns a scatterplot all players' expected goals and assists with a selected player highlighted on the plot
def expectedgoals_vs_expectedassists_player(p):
    detailed_df = player_stats_df()[0]
    fig = px.scatter(detailed_df, x="Expected Assists", y="Expected Goals")
    trace = next(fig.select_traces())
    n = len(trace.x)
    index = detailed_df.index[detailed_df['Player'] == p]
    k = index[0]
    color = [trace.marker.color] * n
    color[k] = "red"
    size = [8] * n
    size[k] = 15
    symbol = [trace.marker.symbol] * n
    symbol[k] = "star"
    fig.update_traces(marker=dict(color=color, size=size, symbol=symbol))
    return fig


# Returns a scatterplot all players' goals and starts with a selected player highlighted on the plot
def goals_vs_starts(p):
    detailed_df = player_stats_df()[0]
    fig = px.scatter(detailed_df, x="Starts", y="Goals")
    trace = next(fig.select_traces())
    n = len(trace.x)
    index = detailed_df.index[detailed_df['Player'] == p]
    k = index[0]
    color = [trace.marker.color] * n
    color[k] = "red"
    size = [8] * n
    size[k] = 15
    symbol = [trace.marker.symbol] * n
    symbol[k] = "star"
    fig.update_traces(marker=dict(color=color, size=size, symbol=symbol))
    return fig

# Returns a bar graph of top 10 players' statistics
def relative_all_players():
    detailed_df = player_stats_df()[0]
    detailed_df_sorted = detailed_df[['Player','Minutes Played', 'Goals', 'Assists', 'Yellow Cards']].sort_values(by='Goals', ascending=False)
    df_sklearn = detailed_df_sorted.copy()
    column = 'Minutes Played'
    df_sklearn[column] = MinMaxScaler().fit_transform(np.array(df_sklearn[column]).reshape(-1,1))
    column = 'Assists'
    df_sklearn[column] = MinMaxScaler().fit_transform(np.array(df_sklearn[column]).reshape(-1,1))
    column = 'Yellow Cards'
    df_sklearn[column] = MinMaxScaler().fit_transform(np.array(df_sklearn[column]).reshape(-1,1))
    column = 'Goals'
    df_sklearn[column] = MinMaxScaler().fit_transform(np.array(df_sklearn[column]).reshape(-1,1))
    detailed_df = df_sklearn[['Player','Minutes Played', 'Goals', 'Assists', 'Yellow Cards']]
    st.title('Top 10 Goal Scorers')
    st.bar_chart(detailed_df.head(20), x='Player',y = ['Minutes Played', 'Goals', 'Assists', 'Yellow Cards'])

# Fetches the statistics for a selected player
def get_player_data(player_name):
    detailed_df, short_df = player_stats_df()
    player_data = detailed_df.loc[detailed_df['Player'].str.contains(player_name,case=False)]
    return player_data, short_df

# Fetches the google image of the selected player
def get_google_image(keyword):
  search_url = "https://www.google.com/search?q={}&tbm=isch".format(keyword)
  response = requests.get(search_url)
  if response.status_code == 200:
    img_tags = re.findall("<img[^>]+src=[\"'](.*?)[\"']", response.text)
    if img_tags:
      return img_tags[1]
  return []



