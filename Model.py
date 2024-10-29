import streamlit as st
import openai
import pandas as pd

# Set up OpenAI API key securely from Streamlit secrets
openai.api_key = st.secrets["general"]["openai_api_key"]

# Google Sheets document details
document_id = st.secrets["documents"]["document_id"]
tab_name = st.secrets["tab_name"]["tab_name_id"]
full_url = f"https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"

# Load data from Google Sheets
ncaaf_df = pd.read_csv(full_url)
ncaaf_df.rename(columns={"Sheet Name :- ": "Team"}, inplace=True)

def get_prompt(team1, team2):
  team1_stats=ncaaf_df[ncaaf_df["Team"]==team1].to_markdown()
  team2_stats=ncaaf_df[ncaaf_df["Team"]==team2].to_markdown()
  
  prompt=f"""Below given details are different metrics two football teams accross different matches.
  # Team1 Stats:
  {team1_stats}
  
  # Team2 Stats:
  {team2_stats}
    Great Job. Analyze these stats and predict the winner of the match based on these stats, use your knowledge and find previous matches results between these two teams\
  and your cognitive skills. Just give me winner team name output and score margin only two things as output.
  Here is the team1:{team1} and team2: {team2}
  """
  return prompt

def predict_winner(prompt):
    # Use the compatible OpenAI API method
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

teams = ncaaf_df["Team"].unique().tolist()

st.title("AI Win Predictor")

team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams, index=1)

if st.button("Predict"):
    prompt = get_prompt(team1, team2)
    result = predict_winner(prompt)
    st.balloons()
    st.header("Predicted Winner")
    st.write(result)
