import streamlit as st
st.set_page_config(
    page_title="Mon App Ligue1",
    layout="wide",       # options : "centered" (par défaut), "wide"
    initial_sidebar_state="expanded"  # ou "collapsed"
)
create_page = st.Page("pages/page_viz.py", title="Visualisation")
delete_page = st.Page("pages/page_pred.py", title="Prediction")

pg = st.navigation([create_page, delete_page])
pg.run()