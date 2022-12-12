# Import the necessary libraries
import streamlit as st
import pandas as pd
import functions

st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
# Adding a banner and titles 
st.image("banner.jpeg")
st.title("Soccer Space")
st.image("banner2.jpeg")

# Define a dictionary containing soccer-related terms and their definitions, along with image URLs
football_terms = {'Forward' : ["A forward is a player whose primary objective is to score and make assists to other forwards trying to score. They take most of the shots and typically score most of the goals for their team. It is the most glamorous position in soccer since the forwards are the players most associated with a win, even if all players truly contribute to every win or loss.", 'https://www.rookieroad.com/img/soccer/soccer-forward.png'],
                  'Bicycle Kick' : ["A volley in which the player kicks the ball over his own head. This is not just a simple overhead kick, which can be accomplished keeping one foot on the ground. In the true bicycle kick, the player has both feet off the ground. With his body 'floating' horizontally he uses a rapid pedaling motion of both legs (hence the bicycle reference) to kick the ball backward. The player is, in effect, performing a somersault as he kicks. This allows him to get his feet above the level of his head so that the trajectory of the ball can be kept down, essential for one of the bicycle kick's most spectacular uses as a shot on goal. The bicycle kick should not be confused with the Scissor Kick.", "https://img.fcbayern.com/image/upload/t_cms-1x1-seo/v1637690963/cms/public/images/fcbayern-com/homepage/saison-21-22/Galerien/Spiele/DYN%20-%20FCB/08_DYNFCB_231121_GET.jpg"],
                  'Midfielder' : ["The midfielders are a group of well-rounded players who cover the most ground during a game, as their job is to play a combination position of a forward and defender. Like defenders, there are central midfielders and wide midfielders and there are also players who further specialize like attacking or defending midfielders.", 'https://www.rookieroad.com/img/soccer/soccer-midfielder.png'],
                  'Defender' : ["The defenders are a group of players responsible for guarding their team’s goal and preventing the opposing team from scoring. While it may not be as glamorous, defensive soccer is just as important to a team's success as offense.",'https://www.rookieroad.com/img/soccer/soccer-defender.png'],
                  'Nutmeg' : ["A player kicks the soccer ball through another player’s legs.", 'https://www.rookieroad.com/img/soccer/soccer-nutmeg.png'],
                  'Penalty' : ["Beware! The word 'penalty' has a very specific (and very dramatic) meaning in soccer. It should be applied only to the award of a penalty kick -- i.e., the 12-yard direct free kick taken from the penalty spot with only the goalkeeper to beat. It should never be used in connection with any other offense or free kick situation.", 'https://www.rookieroad.com/img/soccer/soccer-penalty-kick.png'],
                  'Offside' : ["A player is considered offside in soccer when they are behind the last defender on the opposing team. An offside violation will be called when a player receives a pass from a teammate while in an offside position.", 'https://www.rookieroad.com/img/soccer/soccer-offside.png'],
                  'Yellow Card' : ["A yellow card is a physical card shown to a player by an official for committing a minor violation or caution during a game. Two of these cards result in a red card, which is much more severe.",'https://www.rookieroad.com/img/soccer/soccer-yellow-card.png'],
                  'Red Card' : ["If an official displays a red card, it is because a serious offense was committed. A red card is a physical red card carried by the head official, and shown to a player to signify that they have been removed from the match, and their team must play with one less player in the match.", 'https://www.rookieroad.com/img/soccer/soccer-red-card.png'],
                  'Corner Kick' : ["In a corner kick, the ball is placed in the corner arc and a player on the opposing team kicks the ball into play. This is a common method for restarting play when the ball is kicked out of bounds. Possession is then given to the team that did not touch the ball last as it traveled out of bounds",'https://www.rookieroad.com/img/soccer/soccer-corner-kick.png']
                  }

# Creating a sidebar to show common football terms                  
with st.sidebar:
    st.title("Common Football Terms")
    for key,val in football_terms.items():
        st.header(key)
        st.caption(val[0])
        st.image(val[1])

# Dividing the UI in appropriate workspaces        
col1, col2,col3,col4 = st.tabs(["Team","Player","Twitter Sentiment","Betting Odds"])

# Creating a tab that showcases team data based on search conditions
with col1:
    # with st.expander("Team"):
    team_df = pd.read_csv("results.csv")
    with st.expander("Geographical Representation"):
        longitude = [17.0118954, -14.4529612, 54.5643516, 10.3333283, 9.400138, -4.8379791, 20.55144, 127.6961188, -53.2, -79.3666965, -100.445882, 42.3528328, 19.134422, 13.1535811, 134.755, -102.0077097, -64.9672817, 1.8883335, 51.2295295, -8.1353519, -56.0201525, 8.2319736, 10.4478313, -84.0739102, -7.3362482, -3.73893, -1.0800271, -1.2649062, 5.6343227, 4.6667145, 139.2394179, -107.991707]
        latitude = [45.5643442, 14.4750607, 32.6475314, 55.670249, 33.8439408, 39.3260685, 44.1534121, 36.638392, -10.3333333, -1.3397668, 39.7837304, 25.6242618, 52.215933, 4.6125522, -24.7761086, 23.6585116, -34.9964963, 46.603354, 25.3336984, 39.6621648, -32.8755548, 46.7985624, 51.1638175, 10.2735633, 31.1728205, 52.2928116, 8.0300284, 52.5310214, 52.2434979, 50.6402809, 36.5748441, 61.0666922]
        teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
        chart =  pd.DataFrame({'Team':teams, 'lat':latitude, 'lon':longitude})
        st.map(chart)


    st.title("Select Team")
    teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
    team = st.selectbox("Select an option", teams)
    st.metric("Win", functions.get_count(team,team_df,"win"))
    st.metric("Loss", functions.get_count(team,team_df,"loss"))
    st.metric("Draw", functions.get_count(team,team_df,"draw"))
    last_5_matches = functions.get_last_5_matches(team, team_df)
    st.title("Last 5 Matches")
    st.table(last_5_matches[['home_team', 'home_score', 'away_score', 'away_team']].reset_index(drop=True))


# Creating a tab that showcases player data based on search conditions
with col2:
    st.title("Player Data")
    player_name = st.text_input("Enter player name")
    player_data, short_df = functions.get_player_data(player_name.strip())
    if len(player_data) == 0:
        st.title("Player not found!")
    else:
        if player_name:
            player_data.reset_index(inplace=True)
            player_data.drop(['index'],inplace=True,axis=1)
            # st.image(player_data['Imag
            # e'])
            if len(player_data) == 1:
                st.image(functions.get_google_image(player_name))
            c1, c2 = st.columns(2)
            with c1:
                st.title('Minutes Played v/s Goals')
                st.write(functions.goals_vs_minutesplayed_player(player_data["Player"].to_list()[0]))
                st.title('Expected Assists v/s Goals')
                st.write(functions.expectedgoals_vs_expectedassists_player(player_data["Player"].to_list()[0]))
            with c2:
                st.title('Assists v/s Goals')
                st.write(functions.goals_vs_assists_player(player_data["Player"].to_list()[0]))
                st.title('Starts v/s Goals')
                st.write(functions.goals_vs_starts(player_data["Player"].to_list()[0]))
            st.title("Statistics")
            st.table(player_data.T)

        else:
            functions.relative_all_players()
            st.title("Summarized Players")

            st.dataframe(short_df)

# Creating a tab to fetch twitter tweets and display sentiment
with col3:
    st.title("Twitter Sentiment")
    team = st.selectbox("Select Team", teams)

    api = functions.authenticate_tweepy()


    tweets = api.search_tweets(q=f'"FIFA World Cup" {team}',lang='en',result_type = 'popularity',count=500)

    sentiment = functions.tweets_sentiment_score(tweets)

    teams = ['Croatia', 'Senegal', 'Iran', 'Denmark', 'Tunisia', 'Spain', 'Serbia', 'South Korea', 'Brazil', 'Ecuador', 'United States', 'Saudi Arabia', 'Poland', 'Cameroon', 'Australia', 'Mexico', 'Argentina', 'France', 'Qatar', 'Portugal', 'Uruguay', 'Switzerland', 'Germany', 'Costa Rica', 'Morocco', 'Wales', 'Ghana', 'England', 'Netherlands', 'Belgium', 'Japan', 'Canada']
    st.progress(int(sentiment*50+50))
    c1, c2 , c3 , c4, c5, c6, c7 = st.columns(7)
    with c1:
        st.title("😭")
    with c4:
        st.title("🤨")
    with c7:
        st.title("😄")
    st.write("\n \n \n")
    st.write("\n \n \n")

    for tweet in tweets[:10]:
        st.write(tweet.text)
        st.markdown("""---""")
   
# Creating a tab that showcases the webscraped data for betting websites
with col4:
    tab1, tab2,tab3,tab4 = st.tabs(["WynnBet","BetUs","BetFair","DraftsKing"])
    with tab1:
        wynnBet, wynnBetLink = functions.wynnBet()
        c1 , c2, c3 = st.columns(3)
        with c1:
            st.subheader(f"{wynnBet['team1'][0]}")
            st.metric("", "", wynnBet['odds1'][0])
            st.markdown("---")
            st.subheader(f"{wynnBet['team1'][1]}")
            st.metric("", "", wynnBet['odds1'][1])
        with c2:
            st.subheader("V/S")
            st.write("\n \n \n")
            st.metric("", "", "")
            st.markdown("---")
            st.subheader(f"")
            st.subheader("V/S")
        with c3:
            st.subheader(f"{wynnBet['team2'][0]}")
            st.metric("", "", wynnBet['odds2'][0])
            st.markdown("---")
            st.subheader(f"{wynnBet['team2'][1]}")
            st.metric("", "", wynnBet['odds2'][1])

    with tab2:
        betUs, betUsLink = functions.betUS()
        
        c1 , c2, c3 = st.columns(3)
        with c1:
            st.subheader(f"{betUs['team1'][0]}")
            st.metric("", "", betUs['odds1'][0])
            st.markdown("---")
            st.subheader(f"{betUs['team1'][1]}")
            st.metric("", "", betUs['odds1'][1])
        with c2:
            st.subheader("V/S")
            st.write("\n \n \n")
            st.metric("", "", "")
            st.markdown("---")
            st.subheader(f"")
            st.subheader("V/S")
        with c3:
            st.subheader(f"{betUs['team2'][0]}")
            st.metric("", "", betUs['odds2'][0])
            st.markdown("---")
            st.subheader(f"{betUs['team2'][1]}")
            st.metric("", "", betUs['odds2'][1])

    with tab3:
        betFair, betFairLink = functions.betFair()
        c1 , c2,c3 = st.columns(3)
        with c1:
            st.subheader(f"{betFair['team1'][0]}")
            st.metric("", "", betFair['odds1'][0])
            st.markdown("---")
            st.subheader(f"{betFair['team1'][1]}")
            st.metric("", "", betFair['odds1'][1])
        with c2:
            st.subheader("V/S")
            st.write("\n \n \n")
            st.metric("", "", "")
            st.markdown("---")
            st.subheader(f"")
            st.subheader("V/S")
        with c3:
            st.subheader(f"{betFair['team2'][0]}")
            st.metric("", "", betFair['odds2'][0])
            st.markdown("---")
            st.subheader(f"{betFair['team2'][1]}")
            st.metric("", "", betFair['odds2'][1])

    with tab4:
        draftKings, draftKingsLink = functions.draftKings()
        c1 , c2, c3 = st.columns(3)
        with c1:
            st.subheader(f"{draftKings['team1'][0]}")
            st.metric("", "", draftKings['odds1'][0])
            st.markdown("---")
            st.subheader(f"{draftKings['team1'][1]}")
            st.metric("", "", draftKings['odds1'][1])
        with c2:
            st.subheader("V/S")
            st.write("\n \n \n")
            st.metric("", "", "")
            st.markdown("---")
            st.subheader(f"")
            st.subheader("V/S")
        with c3:
            st.subheader(f"{draftKings['team2'][0]}")
            st.metric("", "", draftKings['odds2'][0])
            st.markdown("---")
            st.subheader(f"{draftKings['team2'][1]}")
            st.metric("", "", draftKings['odds2'][1])