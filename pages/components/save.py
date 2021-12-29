from __future__ import print_function
import pandas as pd

def save_work(selected_database, selected_db):
    
    table_list = ['projects', 'prompts', 'completions']
    writer = pd.ExcelWriter('pages/%s.xlsx'%selected_database)
    
    for table in table_list:
    
        projects_df = pd.read_sql_query("SELECT * FROM %s"%table, selected_db)
        projects_df.to_excel(writer, table)
        
    writer.save()
 