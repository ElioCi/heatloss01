import streamlit as st
import sqlite3
import yaml
import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz

def app():
    #DB management
    
    conn= sqlite3.connect('data.db')
    c = conn.cursor()
    def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(name TEXT, username TEXT, email TEXT, password TEXT)')

    def add_userdata(name, username, email, password):
        c.execute('INSERT INTO userstable(name, username, email, password) VALUES(?,?,?,?)', (name, username, email, password))
        conn.commit()

    def login_user(name, username, email, password):
        c.exceute('SELECT * FROM userstable WHERE username = ? AND password = ?', (name, username, email, password))
        data = c.fetchall()
        return data
    
    def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
       
        return data
    
    # funzione per convertire database in config.yaml -----
    def fetch_users_from_db(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name, username, email, password FROM userstable")
        rows = cursor.fetchall()

        users_list = [{'name': name, 'username': username, 'email': email, 'password': password} for name, username, email, password in rows]

        conn.close()
        return users_list
    
    def format_authenticator_config(users_list):
        config = {
            'credentials': {
                'usernames': {}
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'some_random_secret_key',
                'name': 'some_cookie_name'
            },
            'preauthorized': {
                'emails': []
            }
        }

        for user in users_list:
            config['credentials']['usernames'][user['username']] = {
                'password': user['password'],
                'name': user['name'],
                'email': user['email'],
            }

        return config

    def write_config_to_yaml(config, yaml_path):
        with open(yaml_path, 'w') as yaml_file:
            yaml.dump(config, yaml_file, default_flow_style=False)



    # ------------------------------------------------------

    # password reset

    # -------------------------------------------------------
    # Token storage (in memory for simplicity; use a database in production)
    #reset_tokens = {}
    #utc = pytz.UTC
    utc= pytz.timezone("Europe/Rome")
    # Initialize reset_tokens in session state if it doesn't exist
    if 'reset_tokens' not in st.session_state:
        st.session_state.reset_tokens = {}

    def send_reset_email(email, token, expiry_time):
        # Placeholder function to send an email
        st.write(f"Sending email to {email} with *token" )

        sender_email = "solvingvv@gmail.com"
        sender_password = "ocfa uypo udbb hsfy"
        # sender_password = "omda cxlg ncuy rguj"
        recipient_email = email
        subject = "Password Reset Request"
        body = f"Use the following token to reset your password: {token}\n\nThis token will expire at {expiry_time} (UTC)."

        msg = MIMEMultipart()
        msg['From'] = "Heat_Loss" #sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            st.success("Password reset email sent")
        except Exception as e:
            st.error(f"Failed to send email: {e}")



    def generate_reset_token(email):
        token = secrets.token_urlsafe()
        expiry_time = datetime.now(utc) + timedelta(hours=1)
        st.session_state.reset_tokens[token] = {"email": email, "expiry": expiry_time}
    
        return token, expiry_time

    def reset_password(token, new_password):
 
        token_data = st.session_state.reset_tokens.get(token)


        if token_data and token_data["expiry"] > datetime.now(utc):
            email = token_data["email"]
            #user = c.query(userstable).filter_by(email=email).first()
            c.execute('SELECT email FROM userstable WHERE email= ?', (email,))
            user = c.fetchone()

            if user:
                #hashed_password = stauth.Hasher([new_password]).generate()[0]
                #c.execute(userstable.update().where(userstable.c.email == email).values(password= new_password))
                c.execute('UPDATE userstable SET password=? WHERE email=?', (new_password, email))
                conn.commit()
                del st.session_state.reset_tokens[token]
                st.success("Password reset successfully")
            else:
                st.error("Invalid token")
        else:
            st.error("Token expired or invalid")

    # Initialize session state for token and new password
    if 'token' not in st.session_state:
        st.session_state.token = ''
    if 'new_password' not in st.session_state:
        st.session_state.new_password = ''

    # Password reset request form
    st.title("PASSWORD RESET FORM")

    st.session_state.token = ''
    st.session_state.new_password = ''

    #data = view_all_users()
    #print("data", data)

    #if st.button("Forgot Password"):
    #    st.write('Reset your password')
    #    email = st.text_input("Enter your email")
    
    email = st.text_input("Enter your email")
    
    if st.button("Request Token"):
        
        #user = c.query(userstable).filter_by(email=email).first()
        #conn= sqlite3.connect('data.db')
        #c = conn.cursor()
        c.execute('SELECT email FROM userstable WHERE email= ?', (email,))
        user = c.fetchone()
        
        
        if user:
            token, expiry_time = generate_reset_token(email)
            send_reset_email(email, token, expiry_time.strftime('%Y-%m-%d %H:%M:%S'))
            st.success("Password reset email sent")

            
        else:
            st.error("Email not found")

    
    
    # Password reset form using st.form
    
    with st.form("reset_form", clear_on_submit= True):
        st.session_state.token = st.text_input("Enter the token you received via email", value=st.session_state.token)
        st.session_state.new_password = st.text_input("Enter new password", type="password", value=st.session_state.new_password)
        submitted = st.form_submit_button("Reset Password")

    if submitted:
        reset_password(st.session_state.token, st.session_state.new_password)
    
        db_path = 'data.db'  # Replace with the path to your SQLite3 database
        yaml_path = 'config.yaml'  # Replace with the desired output path for your config.yaml

        users_list = fetch_users_from_db(db_path)
        config = format_authenticator_config(users_list)
        write_config_to_yaml(config, yaml_path)

    #----------------------------------------------------------------

    
