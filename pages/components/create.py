def create_new_db(db):
    
    cursor = db.cursor()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        notes TEXT,
        starred INT DEFAULT 0,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        project_id INTEGER FORIEGN KEY REFERENCES projects(id),
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        notes TEXT,
        starred INT DEFAULT 0,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS completions (
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
    """)
    db.commit()
