import streamlit as st
st.set_page_config(
    page_title="Ligue 1 en un coup d'oeil",
    layout="wide",       # options : "centered" (par défaut), "wide"
    initial_sidebar_state="expanded"  # ou "collapsed"
)
create_page = st.Page("pages/page_viz.py", title="Visualisation",icon=":material/show_chart:")
delete_page = st.Page("pages/page_pred.py", title="Prediction",icon=":material/cognition:")
new_page = st.Page("pages/page_monte_carlo.py", title="End of season prediction",icon=":material/cognition:")

pg = st.navigation([delete_page,new_page,create_page])
pg.run()