import streamlit as st
import pandas as pd
import functions
st.set_page_config(layout='wide')
# st.snow()
st.title("Soccer Space")


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
with st.sidebar:
    st.title("Common Football Terms")
    for key,val in football_terms.items():
        st.header(key)
        st.caption(val[0])
        st.image(val[1])
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
    st.title("Player Data")
    player_name = st.text_input("Enter player name")
    player_data, short_df = functions.get_player_data(player_name.strip())
    if len(player_data) == 0:
        st.write("Data not found!!")
    else:
        if player_name:

            player_data.reset_index(inplace=True)
            player_data.drop(['index'],inplace=True,axis=1)
            # st.image(player_data['Image'])
            if len(player_data) == 1:
                st.image(functions.get_google_image(player_name))
            st.table(player_data.T)

        else:
            st.dataframe(short_df)
with col3:
    st.title("Tweets and Sentiment")
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
    c1 , c2 = st.columns(2)
    with c1:
        st.title("Wynn Bet")
        wynnBet, wynnBetLink = functions.wynnBet()
        st.dataframe(wynnBet)
        st.title("Bet US")

        betUs, betUsLink = functions.betUS()
        st.dataframe(betUs)
    with c2:
        st.title("BetFair")
        betFair, betFairLink = functions.betFair()
        st.dataframe(betFair)
        st.title("DraftKings")
        draftKings, draftKingsLink = functions.draftKings()
        st.dataframe(wynnBet)
