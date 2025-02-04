import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
import streamlit.components.v1 as components

st.title("DiamondScope")
st.write("If it is not visible due to pop-up blocking, please access this link. https://public.tableau.com/app/profile/ran.xing/viz/MLB_17387022664210/Dashboard2#1")

# Tableau Public Dashboard
st.title("MLB Player Performance")
html_temp = """
<div style="background-color:#e6005c ;padding:10px">
<h2 style="color:white;text-align:center;">Player Performance Analysis ML App </h2>
</div>
<br>
"""
st.markdown(html_temp, unsafe_allow_html=True)
tableau_public_url = "https://public.tableau.com/views/Benefit_17382844900600/BenefitDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
tableau_embed_code = """
<div class='tableauPlaceholder' id='viz1738702614148' style='position: relative'><noscript><a href='#'><img alt='Dashboard 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ML&#47;MLB_17387022664210&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='MLB_17387022664210&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ML&#47;MLB_17387022664210&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1738702614148');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
st.markdown(tableau_embed_code, unsafe_allow_html=True)

components.html(tableau_embed_code, width=1130, height=1100)
