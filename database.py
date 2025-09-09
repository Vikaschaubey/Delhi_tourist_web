import mysql.connector

def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="tour"
    )
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tourist")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",  # replace with your MySQL password
        database="tour"       # replace with your database name
    )
    return conn

# Function to create the table if it doesn't exist
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tourist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        place_name VARCHAR(255),
        eloc VARCHAR(255),
        latitude DOUBLE,
        longitude DOUBLE,
        manufacture_date DATE,
        built_by VARCHAR(255),
        nearest_metro VARCHAR(255)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    
    
def delete_by_eloc(eloc_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tourist WHERE eloc = %s", (eloc_value,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected 