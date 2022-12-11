import pandas as pd
import tweepy
import re
import statistics
from textblob import TextBlob
from bs4 import BeautifulSoup
from bs4 import Comment
import requests


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

def football_data_scraper():
    # url = 'https://fbref.com/en/comps/1/stats/World-Cup-Stats'
    # response = requests.get(url)

    # # Use BeautifulSoup to parse the HTML and extract the table
    # soup = BeautifulSoup(response.text, 'html.parser')
    # table = soup.find('table', {'id': 'stats_standard'})
    # print(table)

    url = 'https://fbref.com/en/comps/1/stats/World-Cup-Stats'
    response = requests.get(url)

    # Use BeautifulSoup to parse the HTML and extract the comments
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    # Convert the comments to HTML
    html_comments = []
    for comment in comments:
        html_comments.append(BeautifulSoup(comment, 'html.parser').prettify())
    print(html_comments)

    # Print the HTML comments
    # for html_comment in html_comments:
    #     print(html_comment)

# football_data_scraper()




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
    detailed_df = df[[( 'Unnamed: 1_level_0',   'Player'),
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


def get_player_data(player_name):
    detailed_df, short_df = player_stats_df()
    player_data = detailed_df.loc[detailed_df['Player'].str.contains(player_name,case=False)]
    # player_data['Image'] = player_data['Player'].apply(lambda x: get_google_image(x))
    return player_data, short_df


def get_google_image(keyword):
  # construct the URL for the Google Images search, specifying that we only want JPEG images
  search_url = "https://www.google.com/search?q={}&tbm=isch&tbo=1&tbs=ift:jpg".format(keyword)

  # send the request to search for the images
  response = requests.get(search_url)

  # if the response was successful, parse the results
  if response.status_code == 200:
    # search the page for all `img` tags that contain images
    img_tags = re.findall("<img[^>]+src=[\"'](.*?)[\"']", response.text)

    if img_tags:
      # if we found any images, return a list of their URLs
      return img_tags[0]

  # if something went wrong, return an empty list
  return []

# def show_image_from_url(image_url):
#     return(f'')

# df['image_url'] = 'https://media.cnn.com/api/v1/images/stellar/prod/221127164140-lionel-messi-inter-miami-rumors-spt-intl.jpg?c=original'
# #Then created a new column
# df['image'] = df.apply( lambda x: show_image_from_url(x['image_url']), axis = 1 )

# #And before run
# df.to_html()

# print(df)





def get_google_image(keyword):
  # construct the URL for the Google Images search
  search_url = "https://www.google.com/search?q={}&tbm=isch".format(keyword)

  # send the request to search for the images
  response = requests.get(search_url)

  # if the response was successful, parse the results
  if response.status_code == 200:
    # search the page for all `img` tags that contain images
    img_tags = re.findall("<img[^>]+src=[\"'](.*?)[\"']", response.text)

    if img_tags:
      # if we found any images, return a list of their URLs
      return img_tags[1]

  # if something went wrong, return an empty list
  return []

def get_goals_scored_by_teams():
    longitude = [17.0118954, -14.4529612, 54.5643516, 10.3333283, 9.400138, -4.8379791, 20.55144, 127.6961188, -53.2, -79.3666965, -100.445882, 42.3528328, 19.134422, 13.1535811, 134.755, -102.0077097, -64.9672817, 1.8883335, 51.2295295, -8.1353519, -56.0201525, 8.2319736, 10.4478313, -84.0739102, -7.3362482, -3.73893, -1.0800271, -1.2649062, 5.6343227, 4.6667145, 139.2394179, -107.991707]
    latitude = [45.5643442, 14.4750607, 32.6475314, 55.670249, 33.8439408, 39.3260685, 44.1534121, 36.638392, -10.3333333, -1.3397668, 39.7837304, 25.6242618, 52.215933, 4.6125522, -24.7761086, 23.6585116, -34.9964963, 46.603354, 25.3336984, 39.6621648, -32.8755548, 46.7985624, 51.1638175, 10.2735633, 31.1728205, 52.2928116, 8.0300284, 52.5310214, 52.2434979, 50.6402809, 36.5748441, 61.0666922]
    teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
    team_df = pd.read_csv("results.csv")
    df = pd.DataFrame(team_df, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score'])
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2018-01-01']
    df = df[df['date'] < '2022-11-20']
    home_goals = []
    away_goals = []
    for team_name in teams:
        home_goals.append(df[(df['home_team'] == team_name)]['home_score'].sum())
        away_goals.append(df[(df['away_team'] == team_name)]['away_score'].sum())
        
    # appending the team and total score in a df
    team_score = pd.DataFrame({'Team':teams, 'Home Score':home_goals, 'Away Score': away_goals, 'lat':latitude, 'lon':longitude})
    
    # for i in range(0,5):
    #     team_score = team_score.append(team_score)
    
    return team_score
