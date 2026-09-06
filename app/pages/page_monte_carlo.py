import streamlit as st
import pandas as pd
import sys
import os
import json
from src.viz import plot_all_zones

with open("data/processed/last_md.txt", "r") as f:
    last_finished_md = int(f.read())
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

st.title("Prédiction du classement en fin de saison")
if last_finished_md<21:
    st.text("Disponible après la J20")
else:
    rank_prob = pd.read_parquet("data/processed/monte_carlo_rank_probs.parquet")
    fig_top, fig_bottom, fig_other = plot_all_zones(rank_prob)

    st.subheader("Top 7 contenders")
    st.plotly_chart(fig_top, use_container_width=True)

    st.subheader("Relegation battle")
    st.plotly_chart(fig_bottom, use_container_width=True)

    st.subheader("Mid-table teams")
    st.plotly_chart(fig_other, use_container_width=True)

