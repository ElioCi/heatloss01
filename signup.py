import streamlit as st
import sqlite3
import yaml

import bcrypt
#import hashlib


def app():
    #DB management
    conn= sqlite3.connect('data.db')
    c = conn.cursor()

    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        #h = hashlib.new('sha256')
        #h.update(b'{password}')
        #hashed = h.hexdigest()
        return hashed.decode()

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

    st.subheader(":blue-background[Create a new account ]")
    
    form1 = st.form("Signup")
    with form1:
        new_name = st.text_input("Name")
        new_user = st.text_input("Username")
        new_email = st.text_input("E-mail")
        new_password = st.text_input("Password", type= 'password')
        confirm_password = st.text_input("Confirm Password", type= 'password')
        if confirm_password != new_password:
            st.warning("The entered password is not the same!")
            confermapw = "no"
        elif confirm_password == new_password:
            confermapw = "ok"
            hashed_password = hash_password(new_password)
        btn1 = st.form_submit_button("submit")
    
    if btn1 and confermapw == "ok":
        create_usertable()
        add_userdata(new_name, new_user, new_email, hashed_password)
        st.success(":smile: You have successfully created a new valid Account!")
        st.info("Go to Login menu to enter your account")

        db_path = 'data.db'  # Replace with the path to your SQLite3 database
        yaml_path = 'config.yaml'  # Replace with the desired output path for your config.yaml

        users_list = fetch_users_from_db(db_path)
        config = format_authenticator_config(users_list)
        write_config_to_yaml(config, yaml_path)
        #----------------------------------------------------------------

    st.write(":red[* Creation of Account is completely free of charges.]")

