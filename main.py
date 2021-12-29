import streamlit as st

from multipage import MultiPage
from pages import database, ideate

app = MultiPage()
apptitle = 'CAI GPT3'
st.set_page_config(page_title=apptitle, page_icon=":brain:")

st.sidebar.markdown("## Select a page")
app.add_page("IDEATE", ideate.app)
app.add_page("DATABASE", database.app)

app.run()