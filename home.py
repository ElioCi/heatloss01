import streamlit as st

def app():
    st.info(":smile: Hi   - This Application allows you to analyse heat losses in piping systems. It is necessary to have an account and to Login for using the App. If you do not have one yet, please click '***signup***' in the sidebar for registration. Registration is completely free.")
    
    st.markdown("---")
    #st.title("🌈 Pipe Heat Loss Analysis")
    st.markdown("<h1 style='text-align: center;'>🌈 Pipe heat loss analysis </h1>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    col1.page_link("https://enginapps.it", label="Website - www.enginapps.it", icon="🏠")
    #flag_ns = col2.radio("Select one option", ["New Calculation", "Saved Calculation"])
    st.markdown("")

    st.info("-- App developed by ing. Pasquale Aurelio Cirillo - @ 2024 --")
   
    #st.page_link("pages/page_1.py", label="New Calculation", icon="1️⃣")
    #col1.markdown("")
    #col1.markdown("")

    # col1.page_link("pages/new_calculation.py", label="Calculation Sheet", icon="📝")
    # st.page_link("pages/saved_calculation.py", label="Saved Calculation", icon="📂", disabled=False)
    #st.page_link("http://www.google.com", label="Google", icon="🌎")
    

    #st.session_state['flag_ns'] = flag_ns

    #if flag_ns== "Saved Calculation":
    #    st.page_link("pages/calculationSheet.py", label="Archived file data", icon="📂")
    #    st.markdown("click the button to open a saved calculation sheet")
        
    #else:
    #    st.page_link("pages/calculationSheet.py", label="New Calculation Sheet", icon="📝")
    #    st.markdown("click the button to open a new calculation sheet")


