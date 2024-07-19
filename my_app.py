import streamlit as st  # pip install streamlit
import pandas as pd
import home, account, login, signup, pwreset

from modules import calculationSheet, report
from pathlib import Path

from streamlit_option_menu import option_menu # pip intsall streamlit-option-menu
from matplotlib import pyplot as plt
from math import log
# from tkinter.filedialog import asksaveasfilename
# from tkinter.filedialog import askopenfilename

import csv

st.set_page_config(
    page_title= "Heat Loss",
    page_icon= "🌈"
)
# import "pages/CalculationSheet"

# from csv import DictReader
# Session State


class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
            
        #= st.sidebar.checkbox(testochk, key= "chk", value= valore, label_visibility= statochk)
    
    def run():
        # --- sidebar navigation menu  ---
        

        if 'authentication_status' not in st.session_state:
            st.session_state["authentication_status"] = None
        if 'name' not in st.session_state:
            st.session_state["name"] = ""         
        
        if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] is False:
            options = ["home", "login", "signup", "pw reset"]
            icons = ["house-up", "person-square", "person-square", "person-fill-slash"]
        elif st.session_state["authentication_status"]:
            options = ["home", "logout", "new project", "open project", "report"]
            icons = ["house-up", "person-square", "file-earmark-plus", "book", "printer"]

        #if st.session_state.logged == "not_logged":
        #    options = ["home", "login"]
        #    icons = ["house-up", "person-square"]
        #elif st.session_state.logged == "logged":
        #    options = ["home", "login", "new project", "open project", "report"]
        #    icons = ["house-up", "person-square", "file-earmark-plus", "book", "printer"]


        with st.sidebar:
            
            app = option_menu(
                menu_title= "Menu",  # required
                options = options, # required
                icons= icons,  # optional
                #menu_icon= "cast",          # optional
                default_index= 0,           # optional
            )
            
            
        #leggi dati di input da temDati.csv
        with open('files/tempDati.csv') as file_input:
            dftemp = pd.read_csv(file_input)   # lettura file e creazione
            dftemp.drop(dftemp.columns[dftemp.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)
                    
        # inizializza variabili session_state
       

        if 'run' not in st.session_state:
            st.session_state.run = ""
        if 'modifica' not in st.session_state:
            st.session_state.modifica = "non_modificabile"
        if 'DN' not in st.session_state or 'fT' not in st.session_state:
            st.session_state.DN = str(dftemp.loc[0, 'DN'])
            st.session_state.fT = dftemp.loc[0,'fT']
        if 'eT' not in st.session_state or 'fR' not in st.session_state:
            st.session_state.eT = dftemp.loc[0,'eT']
            st.session_state.fR = dftemp.loc[0,'fR']
        if 'sH' not in st.session_state or 'cP' not in st.session_state or 'cI' not in st.session_state:
            st.session_state.sH = dftemp.loc[0,'sH']
            st.session_state.cP = dftemp.loc[0,'cP']
            st.session_state.cI = dftemp.loc[0,'cI']
        if 'hi' not in st.session_state or 'he' not in st.session_state:
            st.session_state.hi = dftemp.loc[0,'hi']
            st.session_state.he = dftemp.loc[0,'he']
        if 'iThk' not in st.session_state or 'PLen' not in st.session_state:
            st.session_state.iThk = dftemp.loc[0,'iThk']
            st.session_state.PLen = dftemp.loc[0,'PLen']
        if 'numValves' not in st.session_state or 'eDvalve' not in st.session_state:
            st.session_state.numValves = dftemp.loc[0,'numValves']
            st.session_state.eDvalve = dftemp.loc[0,'eDvalve']
        if 'Lvalve' not in st.session_state or 'insulated' not in st.session_state:
            st.session_state.Lvalve = dftemp.loc[0,'Lvalve']
            st.session_state.insulated = dftemp.loc[0,'insulated']
        #st.write("my_app--> DN = ", st.session_state.DN)
        if app== "home":
            home.app(),
        if app== "login" or app== "logout":
            login.app()
        if app== "signup":
            signup.app()
        if app== "pw reset":
            pwreset.app()           
        
        if st.session_state["authentication_status"]:
            
            nome = st.session_state["name"]
            st.info(f'🔒 logged-in as {nome}')  
             

            if app== "new project":
            
                st.info("-- Started New project ---")
                flag_ns = "new"
                st.session_state['flag_ns'] = flag_ns
                #flag_run = ""
                #st.session_state['run'] = flag_run
                st.markdown("<h1 style='text-align: center;'>🌈 Pipe heat loss analysis </h1>", unsafe_allow_html=True)
                st.write("")
                
                #leggi dati di input da temDati.csv
                #with open('files/tempDati.csv') as file_input:
                #    dftemp = pd.read_csv(file_input)   # lettura file e creazione
                #    dftemp.drop(dftemp.columns[dftemp.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)
                
                flag_mod= st.session_state['modifica']    
                if flag_mod != "modificabile" and flag_ns =="new":
                    DN = dftemp.loc[0, 'DN'] 
                    thksel = dftemp.loc[0,'thksel']
                    eDia = dftemp.loc[0,'eDia']
                    thk = dftemp.loc[0,'thk']
                    iDia = dftemp.loc[0,'iDia']
                    fT = dftemp.loc[0,'fT']
                    eT = dftemp.loc[0,'eT']
                    fR = dftemp.loc[0,'fR']
                    sH = dftemp.loc[0,'sH']
                    cP = dftemp.loc[0,'cP']
                    cI = dftemp.loc[0,'cI']
                    hi = dftemp.loc[0,'hi']
                    he = dftemp.loc[0,'he']
                    iThk = dftemp.loc[0,'iThk']
                    PLen = dftemp.loc[0,'PLen']
                    numValves = dftemp.loc[0,'numValves']
                    eDvalve = dftemp.loc[0,'eDvalve']
                    Lvalve = dftemp.loc[0,'Lvalve']
                    insulated = dftemp.loc[0,'insulated']
                # st.write("DN = ", DN)
                    
                    # Delete all the items in Session state
                    for key in st.session_state.keys():
                        if key != "flag_ns" and key != "authentication_status" and key != "name" and key != "username":
                            del st.session_state[key]
                    
                    st.session_state['DN']= str(DN)
                    st.session_state['thksel']= str(thksel) 
                    st.session_state['extDia']= eDia
                    st.session_state['thk']= thk
                    st.session_state['iDia']= iDia
                    st.session_state['fT']= fT
                    st.session_state['eT']= eT
                    st.session_state['fR']= fR
                    st.session_state['sH']= sH
                    st.session_state['cP']= cP
                    st.session_state['cI']= cI
                    st.session_state['hi']= hi
                    st.session_state['he']= he
                    st.session_state['iThk']= iThk
                    st.session_state['PLen']= PLen
                    st.session_state['numValves']= numValves
                    st.session_state['eDvalve']= eDvalve
                    st.session_state['Lvalve']= Lvalve
                    st.session_state['insulated']= insulated   

                           
                calculationSheet.app()
            # "st.session_state = ", st.session_state
                   
                # Inizializzazione dello stato
                #if 'checkbox_visible' not in st.session_state:
                #    st.session_state.checkbox_visible = True
                # Visualizzazione condizionale della checkbox
                #if st.session_state.checkbox_visible:
                #    checkbox_value = st.sidebar.checkbox("-- New analysis running! --", value=True)
                #    st.markdown("<h1 style='text-align: center;'>🌈 Pipe heat loss calculation </h1>", unsafe_allow_html=True)
                #    calculationSheet.app(),
                #    if not checkbox_value:
                #        st.session_state.checkbox_visible = False
                #        st.experimental_rerun()
                #else:
                    #
                    #if st.sidebar.button("close analysis"):
                #    st.session_state.checkbox_visible = True
                    #app= "home"
                    
                #    st.session_state.option_menu_default_index= 0#
                #    home.app()
                    
                    # option_menu.default_index =0,
                #chkClose = st.sidebar.checkbox(label="bravo", key= "chk", value=True, label_visibility= "visible", on_change= modchk)
                
                #if not chkClose:
                    
                    # st.sidebar.checkbox(testochk, key= "chk", value=True, label_visibility= statochk)
                
                    #st.markdown("<h1 style='text-align: center;'>🌈 Pipe heat loss calculation </h1>", unsafe_allow_html=True)
                    #calculationSheet.app(),
        
            if app== "open project":
                
                st.info("-- Archived project ---")
                #  st.success("Saved File")
                #nomeArchivio = askopenfilename(defaultextension= 'csv')
                st.markdown("<h1 style='text-align: center;'>🌈 Pipe heat loss analysis </h1>", unsafe_allow_html=True)
                st.write("")
                datafile = st.file_uploader("upload file dati", type= ['csv'])
            
                #print("datafile =", datafile)
                #if 'modifica' not in st.session_state:
                #    st.session_state.modifica = "non_modificabile"
                
                if datafile is not None:
                            
                    flag_run = ""
                    st.session_state['run'] = flag_run
                    flag_ns = "Saved Calculation" 
                    st.session_state['flag_ns'] = flag_ns
                    #st.write("-- Opened saved calculation! --")
                    st.subheader("Dataset")
                    file_details = {"FileName": datafile.name, "File Type": datafile.type}
                    # file_details = {"FileName": datafile.name, "File Type": datafile.type}
                    #with open(nomeArchivio) as f:
                    #      dati = pd.read_csv(f, delimiter = "," )   # lettura file e creazione dataFrame
                
                    dati = pd.read_csv(datafile)
                        
                    dati.drop(dati.columns[dati.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)
                
                    st.dataframe(dati, hide_index= True)
                    st.session_state["dati"] = dati
                    #for i in range(10000):
                    #    i+=1
                    flag_mod= st.session_state['modifica']
                    print("logged", st.session_state['authentication_status'])
                    if flag_mod != "modificabile":
                        print("if flag_mod != modificabile   ", flag_mod)   
                        DN = dati.loc[0, 'DN'] 
                        thksel = dati.loc[0,'thksel']
                        eDia = dati.loc[0,'eDia']
                        thk = dati.loc[0,'thk']
                        iDia = dati.loc[0,'iDia']
                        fT = dati.loc[0,'fT']
                        eT = dati.loc[0,'eT']
                        fR = dati.loc[0,'fR']
                        sH = dati.loc[0,'sH']
                        cP = dati.loc[0,'cP']
                        cI = dati.loc[0,'cI']
                        hi = dati.loc[0,'hi']
                        he = dati.loc[0,'he']
                        iThk = dati.loc[0,'iThk']
                        PLen = dati.loc[0,'PLen']
                        #st.write("DN = ", DN)
                        # Delete all the items in Session state
                        for key in st.session_state.keys():
                            if key != "flag_ns" and key != "authentication_status" and key != "name" and key != "username":
                                del st.session_state[key]
                        
                        st.session_state['DN']= str(DN)
                        st.session_state['thksel']= str(thksel) 
                        st.session_state['extDia']= eDia
                        st.session_state['thk']= thk
                        st.session_state['iDia']= iDia
                        st.session_state['fT']= fT
                        st.session_state['eT']= eT
                        st.session_state['fR']= fR
                        st.session_state['sH']= sH
                        st.session_state['cP']= cP
                        st.session_state['cI']= cI
                        st.session_state['hi']= hi
                        st.session_state['he']= he
                        st.session_state['iThk']= iThk
                        st.session_state['PLen']= PLen
                    calculationSheet.app()
            
            if app== "report":
                # inizializza variabili session_state
                    
                flag_run = st.session_state['run']
                if flag_run == "eseguito":
                    report.app()
                    
                else:
                    st.warning("--- ⚠️ Report empty - No calculations performed! ---")
                    
                flag_mod= "non modificabile"
                st.session_state['modifica']= flag_mod              
    run()









# st.set_page_config(initial_sidebar_state="collapsed")
# st.set_page_config(page_title= "pages/saved_calculation.py", None) -> None
