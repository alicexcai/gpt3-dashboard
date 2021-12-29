import streamlit as st
import pandas as pd
import sqlite3
import os

from .components import save

def app():
    st.title("DATABASE")

    db_list = [file for file in os.listdir(os.path.dirname(__file__)) if file.endswith(tuple(['.sqlite', '.db'])) and not file.startswith('.')] # Ignore hidden files
    selected_database = st.sidebar.selectbox("Select a database", db_list)

    selected_db = sqlite3.connect(os.path.dirname(__file__) + "/" + selected_database) if selected_database else None
    
    if selected_db:   
        cursor = selected_db.cursor()

        cursor.execute("""
                       SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                       """)
        tables_list = sum(cursor.fetchall(), ())
        selected_table = st.sidebar.selectbox("Select a table", tables_list)
        
        selected_table_data = pd.read_sql_query("SELECT * from %s" %selected_table, selected_db)
        
        st.dataframe(selected_table_data, height=10000)
        
        with open(os.path.dirname(__file__) + "/" + selected_database, "rb") as fp:
            download_button = st.sidebar.download_button(
                label="Download .sqlite file",
                data=fp,
                file_name=selected_database,
                mime="application/octet-stream"
            )
            
        save_work_button = st.sidebar.button("Save database to .xlsx file")
        if save_work_button:
            save.save_work(selected_database, selected_db)
        
        if os.path.exists(os.path.dirname(__file__) + "/" + selected_database + '.xlsx'): 
            download_xlsx_button = st.sidebar.download_button(
                label="Download xlsx file",
                data=open(os.path.dirname(__file__).replace(".sqlite", "") + "/" + selected_database + '.xlsx', "rb"),
                file_name=selected_database + '.xlsx',
                mime="application/octet-stream"
            )
