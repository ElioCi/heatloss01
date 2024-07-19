import streamlit as st
#import pickle     #pip install streamlit-authenticator
#from pathlib import Path

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def app():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader= SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    authenticator.login()

    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', location= 'sidebar')
        st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
        st.title("Authentication Page")
    elif st.session_state["authentication_status"] is False:
        st.error("Invalid Username/Password")
        st.warning("If you do not remember or you want to reset your password, please click **pw reset** in the sidebar")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please, insert a valid username")
    else:
        st.warning("Please, insert a valid username")


    
        
        
        
    





