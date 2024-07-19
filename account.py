import streamlit as st
import home

def app():
    st.write("")
    #Sign_in/Sign_up form
    #def main():   #simple Login app
    menu= ['Login', 'SignUp' ]
    
    choice = st.selectbox(":smile: Hi - Please check in or create a personal account", menu)
    form1 = st.form("Login", clear_on_submit= True, border=True)

    if choice == "Login":
        title= "Login"
        form1.title(title)
        username = form1.text_input("User Name", placeholder= "input UserName")
        password = form1.text_input("Password", placeholder= "input your password", type= 'password')
    elif choice == "SignUp":
        title= "SignUp"
        form1.title(title)
        form1.subheader("Create a new account")
       
   
    login = form1.form_submit_button("Submit")
    if login:
        st.session_state.logged = "logged"
        st.sidebar.success("Logged in as {}".format(username))
        


#if __name__== '__main__':
#    main()

