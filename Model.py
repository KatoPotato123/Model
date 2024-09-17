#pip install langchain-groq

import streamlit as st
import pandas as pd
import numpy as np
from langchain_groq import ChatGroq

document_id = "1gVtZ1Cvu8vvvwMzakWjopIL17xNc32F01Wx4O65gKAQ"
tab_name = "MAIN%20FOR%20FIVERR%20GUY"

# Use the correct URL format for exporting to CSV
full_url = f"https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"

# df = pd.read_csv(full_url)


ncaaf_df=pd.read_csv(full_url)
# ncaaf_df.dropna(inplace=True)
ncaaf_df.rename(columns={"Sheet Name :- ": "Team"}, inplace=True)

GROQ_API_KEY="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"


llm = ChatGroq(
    temperature=0,
    model="llama-3.1-70b-versatile",
    api_key=GROQ_API_KEY
)

def get_prompt(team1,team2):
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




teams=ncaaf_df["Team"].values.tolist()

st.title("AI Win Predictor")


team1=st.selectbox("Team-1", teams)
team2=st.selectbox("Team-2", teams,index=1)

if st.button("Predict"):
	res=llm.invoke(get_prompt(team1,team2))
	st.balloons()
	st.header("Winner is")
	st.write(res.content)

