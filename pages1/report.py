import streamlit as st

"session_state:", st.session_state

diam = st.session_state['DN']
flag_run = st.session_state['run']
extDia = st.session_state['extDia']
thk = st.session_state['thk']
intDia = st.session_state['intDia']
    
#st.write("Page 2")

#st.title("Pipe Heat Losses Calculation")
if flag_run == "eseguito":
    st.markdown("---")
    st.markdown("<h3 style='text-align: Left;'>📃  Calculation Report </h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("Selected Dia = ", diam, '"')
    st.write("External Dia =", extDia, "mm")
    st.write("Thikness =", thk, "mm")
    st.write("Internal Dia =", intDia, "mm")
