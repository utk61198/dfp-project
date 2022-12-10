import pandas as pd
import tweepy
import re
import statistics
from textblob import TextBlob

def get_win_count(team_name, df):
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2018-01-01']
    df = df[df['date'] < '2022-11-20']
    home_wins = df[(df['home_team'] == team_name) & (df['home_score'] > df['away_score'])]
    away_wins = df[(df['away_team'] == team_name) & (df['away_score'] > df['home_score'])]
    win_count = len(home_wins) + len(away_wins)
    return win_count

def get_draw_count(team_name, matches):
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2018-01-01']
    home_draws = df[(df['home_team'] == team_name) & (df['home_score'] == df['away_score'])]
    away_draws = df[(df['away_team'] == team_name) & (df['away_score'] == df['home_score'])]
    draw_count = len(home_draws) + len(away_draws)
    return draw_count


def get_loss_count(team_name, matches):
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2018-01-01']
    df = df[df['date'] < '2022-11-20']
    home_losses = df[(df['home_team'] == team_name) & (df['home_score'] < df['away_score'])]
    away_losses = df[(df['away_team'] == team_name) & (df['away_score'] < df['home_score'])]
    loss_count = len(home_losses) + len(away_losses)
    return loss_count


def get_last_5_matches(team_name, matches):
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date', ascending=False)
    team_matches = df[(df['home_team'] == team_name) | (df['away_team'] == team_name)]
    last_5_matches = team_matches.iloc[:5]
    return last_5_matches

def authenticate_tweepy():
    consumer_key="20QCtfjScHSWfzohGhGjYUs7w"
    consumer_secret="Z3tIfmpILNB4kYJIQ7Q1Omg54Ru90mxsCdTz8Yki69010C2EcG"
    access_token="1138374206750482433-UnrC2n2zjvpbMQ0cIMlibTKPfB8s1Q"
    access_token_secret="ExSHUpNT06wYPRL7DvZMIhihWTSpfXiyR633AgQfScCMF"
    auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return api


def preprocessTweets(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())

def tweets_sentiment_score(tweets):
    # sentiment_intensity_obj = SentimentIntensityAnalyzer()
    total_sentiment = []
    for tweet in tweets:
        # total_sentiment.append(sentiment_intensity_obj.polarity_scores(tweet.text)['pos'])
        analysis=TextBlob(preprocessTweets(tweet))
        total_sentiment.append(analysis.sentiment.polarity)
    print(total_sentiment)
    total_sentiment = [i for i in total_sentiment if i != 0]
    return statistics.mean(total_sentiment)

# geosearch