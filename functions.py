import pandas as pd
def get_win_count(team_name, df):
    df['date'] = pd.to_datetime(df['date'])

    # Filter the dataframe to only include matches after 2018
    df = df[df['date'] >= '2018-01-01']
    df = df[df['date'] < '2022-11-20']

    # Get the rows where the specified team was the home team and they won (home_score > away_score)
    home_wins = df[(df['home_team'] == team_name) & (df['home_score'] > df['away_score'])]

    # Get the rows where the specified team was the away team and they won (away_score > home_score)
    away_wins = df[(df['away_team'] == team_name) & (df['away_score'] > df['home_score'])]

    # Sum the number of rows in the home_wins and away_wins dataframes to get the total number of wins
    win_count = len(home_wins) + len(away_wins)

    # Print the win count
    return win_count

def get_draw_count(team_name, matches):
    # Load the data into a pandas dataframe
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])

    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Filter the dataframe to only include matches after 2018
    df = df[df['date'] >= '2018-01-01']

    # Get the rows where the specified team was the home team and the match was a draw (home_score = away_score)
    home_draws = df[(df['home_team'] == team_name) & (df['home_score'] == df['away_score'])]

    # Get the rows where the specified team was the away team and the match was a draw (away_score = home_score)
    away_draws = df[(df['away_team'] == team_name) & (df['away_score'] == df['home_score'])]

    # Sum the number of rows in the home_draws and away_draws dataframes to get the total number of draws
    draw_count = len(home_draws) + len(away_draws)

    return draw_count


def get_loss_count(team_name, matches):
    # Load the data into a pandas dataframe
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])

    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Filter the dataframe to only include matches after 2018
    df = df[df['date'] >= '2018-01-01']
    df = df[df['date'] < '2022-11-20']


    # Get the rows where the specified team was the home team and they lost (home_score < away_score)
    home_losses = df[(df['home_team'] == team_name) & (df['home_score'] < df['away_score'])]

    # Get the rows where the specified team was the away team and they lost (away_score < home_score)
    away_losses = df[(df['away_team'] == team_name) & (df['away_score'] < df['home_score'])]

    # Sum the number of rows in the home_losses and away_losses dataframes to get the total number of losses
    loss_count = len(home_losses) + len(away_losses)
    return loss_count


def get_last_5_matches(team_name, matches):
    # Load the data into a pandas dataframe
    df = pd.DataFrame(matches, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])

    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Sort the dataframe by date in descending order
    df = df.sort_values(by='date', ascending=False)

    # Get the rows where the specified team was the home team or the away team
    team_matches = df[(df['home_team'] == team_name) | (df['away_team'] == team_name)]

    # Get the last 5 rows of the team_matches dataframe
    last_5_matches = team_matches.iloc[:5]
    return last_5_matches
    # return_str = ""
    # for i,row in last_5_matches.iterrows():
    #     return_str = return_str + "\n" + f"{row['home_team']} {row['home_score']} - {row['away_score']} {row['away_team']}"

    return return_str