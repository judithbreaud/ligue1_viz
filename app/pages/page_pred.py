import streamlit as st
import pandas as pd
import sys
import os
import json
from src.etl import display_prediction

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

st.title("Prédiction des matchs de la prochaine journée")
df = pd.read_parquet("data/processed/next_matchday_prediction.parquet")

from src.viz import vizualisation_prediction
fig=vizualisation_prediction(df)
st.plotly_chart(fig)



#with open("data/processed/next_opponent.json", "r", encoding="utf-8") as f:
#    obj = json.load(f)
#domicile=obj["team"] +" / "+obj["next_opponent"]
#exterieur=obj["next_opponent"] +" / "+obj["team"]
#if domicile in sorted(df["game_name"].unique()):
#    index=sorted(df["game_name"].unique()).index(domicile)
#else:
#    index=sorted(df["game_name"].unique()).index(exterieur)

#game_name = st.selectbox(
#        "Match",
#        sorted(df["game_name"].unique()),
#        index=index
#)

#st.table(display_prediction(df,game_name))