import streamlit as st
import pandas as pd
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)
st.title("Comparer les résultats de deux équipes de Ligue 1")
df = pd.read_parquet("data/processed/standings_long.parquet")
col1, col2 = st.columns(2)
with col1:
    team_1 = st.selectbox(
        "Equipe 1",
        sorted(df["team"].unique()),
        index=16
    )
with col2:
    team_2 = st.selectbox(
        "Equipe 2",
        sorted(df["team"].unique()),
    )


from src.viz import compare_gdif, compare_ga, compare_gf, compare_points_total, compare_rank, compare_resultats

col3, col4 = st.columns(2)
with col3:
    fig=compare_rank(df,team_1,team_2)
    st.pyplot(fig)

with col4:
    fig2=compare_points_total(df,team_1,team_2)
    st.pyplot(fig2)

col5, col6=st.columns(2)
with col5:
    fig3=compare_resultats(df,team_1,team_2)
    st.pyplot(fig3)

with col6:
    fig4=compare_gf(df,team_1,team_2)
    st.pyplot(fig4)
col7, col8 = st.columns(2)

with col7:
    fig5=compare_ga(df,team_1,team_2)
    st.pyplot(fig5)

with col8:
    fig6=compare_gdif(df,team_1,team_2)
    st.pyplot(fig6)
