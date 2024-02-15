# app.py  
from detailed_analysis import get_common_opponents, get_match_details, format_match_details, get_summary_statistics
from predictor import P, prepare_match_results, list_players  
from datetime import datetime  
import streamlit as st  

# Initialize the state  
if 'predict_pressed' not in st.session_state:  
    st.session_state['predict_pressed'] = False  
  
if 'start_year' not in st.session_state:  
    st.session_state['start_year'] = 2023  # Default start year  
  
# Set page layout to wide  
st.set_page_config(layout="wide")  
  
# Display the title and subtitle  
st.title('Tennis Match Predictor')  
st.markdown('Calculate the probability of winning a tennis match and determine the optimal bet size using the Kelly Criterion.')  
  
# Create columns for timeframe selection  
col1, col2, col3 = st.columns(3)  
  
with col1:  
    # Load the list of players to display as options in the selectbox  
    gender = st.radio("Select Gender", ('men', 'women'), horizontal=True) 

    # Let the user select a start year  
    st.session_state['start_year'] = st.number_input('Select start year for analysis',   
                                                     min_value=1990,   
                                                     max_value=datetime.now().year,   
                                                     value=st.session_state['start_year'])  
  
# Call prepare_match_results with the dynamic start year  
prepare_match_results((st.session_state['start_year'], datetime.now().year), gender)  
players = list_players()   
  
# Create columns for player selection and odds input  
col1, col2 = st.columns(2)  
  
with col1:  
    player_A = st.selectbox('Choose Player A', players)  
    odds_A = st.number_input('Enter decimal odds for Player A', min_value=1.01, value=2.00)  
  
with col2:  
    player_B = st.selectbox('Choose Player B', [p for p in players if p != player_A])  
    odds_B = st.number_input('Enter decimal odds for Player B', min_value=1.01, value=2.00)  
  
# Center the predict button below the columns  
if st.button('Predict Outcome and Calculate Bet Sizes', key='predict_button'):  
    st.session_state['predict_pressed'] = True  
  
# Use tabs to separate the main content from the additional information  
tab1, tab2, tab_theory = st.tabs(["Main Results", "Detailed Analysis", "The Theory"])  
  
with tab1:    
    if st.session_state['predict_pressed']:    
        # Perform the calculations    
        probability, real_odds_A, real_odds_B = P(player_A, player_B, gender)    
    
        if probability is None:    
            # Display a message to the user when there are no common opponents    
            st.error("No common opponents found between the two players.")    
        else:  
            # This block should be indented to be part of the `else` condition  
            col1, col2 = st.columns(2)    
            with col1:    
                st.metric(label=f"Probability of {player_A} beating {player_B}", value=f"{probability:.2%}")    
                st.metric(label=f"Real odds for {player_A} winning", value=f"{real_odds_A:.2f}")    
    
                # Calculate the Kelly Bet for Player A    
                kelly_bet_A = (probability * (odds_A - 1) - (1 - probability)) / (odds_A - 1)    
                if kelly_bet_A > 0:    
                    st.metric(label=f"Optimal bet size for {player_A}", value=f"{kelly_bet_A:.2%} of your bankroll")    
                else:    
                    st.write("The Kelly Criterion suggests not to bet on this outcome.")    
    
            with col2:    
                st.metric(label=f"Probability of {player_B} beating {player_A}", value=f"{1 - probability:.2%}")    
                st.metric(label=f"Real odds for {player_B} winning", value=f"{real_odds_B:.2f}")    
    
                # Calculate the Kelly Bet for Player B    
                kelly_bet_B = ((1 - probability) * (odds_B - 1) - probability) / (odds_B - 1)    
                if kelly_bet_B > 0:    
                    st.metric(label=f"Optimal bet size for {player_B}", value=f"{kelly_bet_B:.2%} of your bankroll")    
                else:    
                    st.write("The Kelly Criterion suggests not to bet on this outcome.")  
  
with tab2:  
    if st.session_state['predict_pressed']:  
        common_opponents = get_common_opponents(player_A, player_B)  
        if common_opponents:  
            match_details = get_match_details(player_A, player_B, common_opponents)  
            formatted_details = format_match_details(match_details)  
              
            # Get the summary statistics  
            summary_stats = get_summary_statistics(player_A, player_B, common_opponents)  
              
            # Display the summary statistics  
            st.subheader("Summary Statistics")  
            st.text(f"Total Games: {summary_stats['total_games']}")  
            st.text(f"Common Opponents: {summary_stats['common_opponents']}")  
            st.text(f"{player_A} Wins: {summary_stats['player_A_wins']}")  
            st.text(f"{player_A} Losses: {summary_stats['player_A_losses']}")  
            st.text(f"{player_B} Wins: {summary_stats['player_B_wins']}")  
            st.text(f"{player_B} Losses: {summary_stats['player_B_losses']}")  
              
            # Display the formatted match details  
            st.subheader("Detailed Match Results")  
            st.text(formatted_details)  
        else:  
            st.write("No common opponents found.")  
              
        # Reset the predict_pressed flag after displaying the analysis  
        st.session_state['predict_pressed'] = False    

with tab_theory:  
    st.write("""  
    ### Common-Opponent Stochastic Model for Tennis Match Prediction  
  
    This model is based on a hierarchical Markov model that estimates the pre-play probability of each player winning a professional singles tennis match. The key idea is to provide a fair comparison between players by analyzing match statistics against common opponents both players have faced in the past.  
    
    #### Abstract:  
    Tennis features among the most popular sports internationally, with professional matches played for 11 months of the year around the globe. The rise of the internet has stimulated a dramatic increase in tennis-related financial activity, much of which depends on quantitative models. This paper presents a hierarchical Markov model which yields a pre-play estimate of the probability of each player winning a professional singles tennis match. Crucially, the model provides a fair basis of comparison between players by analysing match statistics for opponents that both players have encountered in the past. Subsequently the model exploits elements of transitivity to compute the probability of each player winning a point on their serve, and hence the match. When evaluated using a data set of historical match statistics and bookmakers odds, the model yields a 3.8% return on investment over 2173 ATP matches played on a variety of surfaces during 2011.
    
    #### Key Points:  
    - **Popularity and Betting**: The popularity of tennis and the growth of internet betting have increased the demand for quantitative predictive models.  
    - **Hierarchical Nature of Tennis**: Tennis matches consist of sequences of sets, games, and points. This structure lends itself well to hierarchical modeling.  
    - **Assumptions**: The model assumes that points are independent and identically distributed, allowing for a simplified calculation of match probabilities.  
    - **Serving and Returning**: The model focuses on estimating the probabilities of winning a point on serve and return, crucial variables in determining match outcomes.  
    - **Common Opponents**: By comparing players' performances against shared opponents, the model leverages transitivity in tennis to predict outcomes.  
    - **Evaluation**: The model was tested on historical match data and yielded a positive return on investment, suggesting its effectiveness.  
    - **Improvement Potential**: While the model shows promise, there is room for further refinement, such as considering more sophisticated betting strategies or recursive approaches.  
    
    #### Authors:  
    William J. Knottenbelt, Demetris Spanias, and Agnieszka M. Madurska  
  
    Department of Computing, Imperial College London, South Kensington Campus, London, SW7 2AZ, United Kingdom.  
  
    [Get the full document on sciencedirect](https://www.sciencedirect.com/science/article/pii/S0898122112002106)  
    """)  