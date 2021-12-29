import streamlit as st
import numpy as np
import sqlite3
import os
import openai
import numpy as np

from .components import generate
from .components import fetch_data
from .components import create

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def app():
    st.title("IDEATE")

    new_database = ''
    new_project = ''
    
    db_list = [file.replace('.sqlite', '') for file in os.listdir(os.path.dirname(__file__)) if file.endswith(tuple(['.sqlite', '.db'])) and not file.startswith('.')] # Ignore hidden files
    selected_database = st.sidebar.selectbox("Select database", db_list)
    
    with st.sidebar.expander("Create new database"):
        new_database = st.text_input("Enter database name")
        click_create_new_db = st.button("Create database")
    if click_create_new_db and new_database != '':
        new_db = sqlite3.connect(os.path.dirname(__file__) + "/" + new_database + '.sqlite')
        create.create_new_db(new_db)
    
    selected_db = sqlite3.connect(os.path.dirname(__file__) + "/" + selected_database + '.sqlite') if selected_database else None
    
    if selected_db:   
        cursor = selected_db.cursor()
        cursor.execute("SELECT name, id FROM projects")
        
        project_list = dict(cursor.fetchall())
        selected_project = st.sidebar.selectbox("Select project", list(project_list.keys()))  
    
        with st.sidebar.expander("Create new project"):
            new_project = st.text_input("Enter new project name")
            click_create_new_project = st.button("Create project")
        if click_create_new_project:
            cursor.execute(
            """
            INSERT INTO projects ( name )
            VALUES( ? )
            """, [new_project])
            selected_db.commit()
    
        if selected_project:
            
            cursor.execute("SELECT name, id FROM prompts WHERE project_id = %d" %project_list[selected_project])
            prompt_list = dict(cursor.fetchall())
            
            openai.api_key = st.text_input("Enter your OpenAI API key", "")
            
            if openai.api_key:
                @st.cache
                def fetch_models(api_key):
                    models = fetch_data.fetch_finetunes(api_key) + fetch_data.fetch_engines(api_key)
                    return models
                models = fetch_models(openai.api_key)
            
                params = Params()

                selected_prompt = st.selectbox("Select from prompts in this project", list(prompt_list.keys()))
                with st.expander("Create new prompt"):
                    new_prompt = st.text_area("Enter new prompt")
                    click_create_new_prompt = st.button("Save prompt")
                    if click_create_new_prompt:
                        cursor.execute(
                        """
                        INSERT INTO prompts ( project_id, name )
                        VALUES( ?, ? )
                        """, [project_list[selected_project], new_prompt])
                        selected_db.commit()
                        st.code("New prompt created:" + new_prompt)

                if selected_prompt:
                    
                    params.prompt_id = prompt_list[selected_prompt]
                    params.prompt = selected_prompt
                    
        # ADJUST MODEL PARAMETERS
    
                    with st.expander("Adjust model parameters"):
                        
                        exploration_type = st.radio("Generation Type", options=["Single Generation", "Parameter Exploration"])
                        if exploration_type == "Single Generation":
                            params.model = [st.selectbox("Select model", models)]
                            params.temp = [st.slider("Temperature", 0.0, 1.0, 0.7)]
                        else:
                            params.model = st.multiselect("Select model", models)
                            temperature_range = st.slider("Temperature", 0.0, 1.0, (0.5, 0.7))
                            params.temp = list(np.arange(temperature_range[0], temperature_range[1], 0.1))

                        params.max_tokens = st.slider("Response Length", 0, 500, 64) # change standard to our length?
                        params.num_output = st.slider("Number of Outputs", 1, 10, 1)
                        show_more_params = st.checkbox("Show more parameters")
                        
                        params.stop_sequences = st.text_input("Stop sequences") if show_more_params else None
                        params.top_p = st.slider("Top P", 0.0, 1.0, 1.0) if show_more_params else 1.0
                        params.freq_penalty = st.slider("Frequency Penalty", 0.0, 2.0, 0.0) if show_more_params else 0.0
                        params.pres_penalty = st.slider("Presence Penalty", 0.0, 2.0, 0.0) if show_more_params else 0.0
                        params.best_of = st.slider("Best Of", 0, 10, 1) if show_more_params else 1

                    
            if openai.api_key:
                if st.button("Run Exploration"):
                    # with st.expander("See Parameters"):
                    #     st.write(params.__dict__)

                    with st.spinner('Generating..'):

                        full_response, parsed_response = generate.generate(params, selected_db, cursor, openai.api_key)
                        # with st.expander("See Full API Response"):
                        #     st.code(full_response)
                        # with st.expander("See Data Table Response"):
                        #     st.write(parsed_response)
                            
                        def display_completion(full_completion, display_key):
                            with st.expander(full_completion['completion']):
                                completion_parameters = full_completion.drop('completion')
                                st.write(completion_parameters.to_dict(), key=display_key)
                        
                        for i in range(len(parsed_response)):
                            display_completion(parsed_response.loc[i], i)

                        st.success('Done!')