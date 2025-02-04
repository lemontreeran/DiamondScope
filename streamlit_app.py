import streamlit as st
from openai import OpenAI

import random
import os
from streamlit_extras.switch_page_button import switch_page
from st_pages import add_page_title, get_nav_from_toml
from streamlit_extras.colored_header import colored_header
from datetime import datetime, timedelta
import requests

# Setup page.
st.set_page_config(layout='wide')

sections = st.sidebar.toggle("Sections", value=True, key="use_sections")


pg = st.navigation([
    st.Page("pages/Home.py", title="Home", icon="🔥"),
    st.Page("pages/Chatbot.py", title="Chatbot", icon="🤖"),
    st.Page("pages/Tableau.py", title="Tableau", icon="🖥️"),
])

add_page_title(pg)

pg.run()
