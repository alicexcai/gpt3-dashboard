# GPT3 Dashboard

# Introduction

This software allows you to generate and systematically store text using GPT3. From creative writing to question answering to classification, GPT3's versatility makes it a customizable AI assistant for almost any purpose. GPT3's effectiveness depends largely on prompt design and model parameters, which requires much exploration and optimization. This system exponentiates that process by allowing efficient exploration of different parameter ranges and systematic management of your data.

## Directory Structure
```
gpt3-dashboard
├── LICENSE
├── README.md
├── main.py
├── multipage.py
├── pages
│   ├── components
│   │   ├── __init__.py
│   │   ├── create.py
│   │   ├── fetch_data.py
│   │   ├── generate.py
│   │   └── save.py
│   ├── database.py
│   └── ideate.py
└── requirements.txt
```

## Features
* ```Design of Experiment``` - Full factorial matrices of parameters are automatically created based on user-inputted parameter ranges. Automated DOE allows users to efficiently explore a parameter space without having to rerun individual parameter combinations.
* ```Call-Response Exposure``` - Calls and responses made to and from APIs are exposed on the front end in collapsible sections of the UI to provide transparency to the user so that they can trace back the steps they took to create a particular experiment.
* ```Database Storage``` - The software stores data in user-specified local databases. Users can create and edit their own databases from the UI. The database is structured such that users can easily fetch the parameters of past experiments and continue experimentation with specific parameter combinations.
* ```Database Exposure``` - Users can view their database from the UI on the DATABASE page. Users can also view specific relevant parts of their raw data in collapsible sections of the UI in the IDEATE page.

## Usage Guide

### Initialization

1. Clone this repository onto your local device.
2. Install the dependencies:
```
pip install -r requirements.txt
```
3. To run the dashboard, run the following command:
```
streamlit run main.py
```
4. To access your sqlite database, run the following command:
```
sqlite_web <databasepath>
```

## Database Structure

The database is structured as follows:

## Projects Table

| id  | name | notes | starred | time |
| --- | ---- | ----- | ------- | ---- |
| --  | --   | --    | --      | --   | 

SQL Command:
```
CREATE TABLE projects  (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  notes TEXT,
  starred INT DEFAULT 0,
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Prompts Table

| id  | project_id | name | notes | starred | time |
| --- | ---------- | ---- | ----- | ------- | ---- |
| --  | --         | --   | --    | --      | --   | 

```
CREATE TABLE prompts  (
  project_id INTEGER FORIEGN KEY REFERENCES projects(id),
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  notes TEXT,
  starred INT DEFAULT 0,
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Completions Table

| id  | prompt_id | name | model | completion | finish_reason | temperature | max_tokens | other_parameters | notes | starred | time |
| --- | --------- | ---- | ----- | ---------- | ------------- | ----------- | ---------- | ---------------- | ----- | ------- | ---- |
| --  | --        | --   | --    | --         | --            | --          | --         | --               | --    | --      | --   | 


```
CREATE TABLE completions  (
  prompt_id INTEGER FORIEGN KEY REFERENCES prompts(id),
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  model TEXT NOT NULL,
  completion TEXT,
  finish_reason TEXT,
  temperature REAL NOT NULL,
  max_tokens INTEGER NOT NULL,
  other_parameters TEXT NOT NULL,
  notes TEXT,
  starred INT DEFAULT 0,
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
