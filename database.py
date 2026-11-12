import sqlite3
from pathlib import Path
from contextlib import closing

DB_PATH = Path(__file__).resolve().parent / "caloriewise.db"


def initialize_database():
    """create the database table if it does not exist"""
    
    with closing(sqlite3.connect(DB_PATH)) as connection:
        
        connection.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                
                age INTEGER NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                
                sex TEXT NOT NULL,
                activity TEXT NOT NULL,
                goal TEXT NOT NULL,
                rmr REAL NOT NULL,
                tdee REAL NOT NULL,
                target REAL NOT NULL,
                
                activity_factor REAL NOT NULL,
                goal_factor REAL NOT NULL,
                
                protein REAL,
                carbs REAL,
                fat REAL
            )
                           """)
        
        #checking which columns already exist
        existing_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(calculations)")
        }
        
        
        #adding missing amcronutrient columns
        for column in ("protein","carbs","fat"):
            if column not in existing_columns:
                connection.execute(f"ALTER TABLE calculations ADD COLUMN {column} REAL")
        
        
        connection.commit()
        
        
        
        
def save_calculation(calculation):
    """save a complete calorie and macro calculations """
    
    
    # define the database columsn
    columns = [
        "age", "weight", "height",
        "sex", "activity", "goal",
        "rmr", "tdee", "target",
        "activity_factor", "goal_factor",
        "protein", "carbs", "fat"
    ]
    
    
    #extract values from the calculation dictionary
    values = [calculation[column] for column in columns]
    
    with closing(sqlite3.connect(DB_PATH)) as connection:
        
        cursor = connection.execute("""
            INSERT INTO calculations (
                age, weight, height,
                sex, activity, goal,
                rmr, tdee, target,
                activity_factor, goal_factor,
                protein, carbs, fat
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)
        
        connection.commit()
        
        #return the unique ID of the save record
        return cursor.lastrowid
    
    
    
def get_calculations():
    """retrive all saved calculations, newest first"""
    
    with closing(sqlite3.connect(DB_PATH)) as connection:
        
        #allow access to column by name
        connection.row_factory = sqlite3.Row
        
        #retrive calculations in descending ID order
        cursor = connection.execute("""
                    SELECT * 
                    FROM calculations
                    ORDER BY id DESC
                                    """)
        #convert database rows into Python dictionaries
        records = [
            dict(row) for row in cursor.fetchall()
        ]
    return records



def delete_calculation(record_id):
    """delete a saved calculation by its unique ID"""
    
    with closing(sqlite3.connect(DB_PATH)) as connection:
        
        cursor = connection.execute(
            "DELETE FROM calculations WHERE id = ?", (record_id,)
        )
        connection.commit()
        
        #true if a record was deleted, false otherwise
        return cursor.rowcount >0