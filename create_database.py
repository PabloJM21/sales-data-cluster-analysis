import json
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import pandas as pd

def create_database():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS etl_db")


# Database connection details
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",        # Replace with your MySQL server host
            user="root",
            database="etl_db"        # Replace with your MySQL database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Create tables for ETL process
def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS category")
    cursor.execute("DROP TABLE IF EXISTS data_type")
    cursor.execute("DROP TABLE IF EXISTS seasonally_adj")
    # SQL to create tables
    create_seasonally_adj_table = """
    CREATE TABLE seasonally_adj (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seasonally_adj VARCHAR(3) NOT NULL
    );
    """
    
    create_data_type_table = """
    CREATE TABLE data_type (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data_type_code VARCHAR(10) NOT NULL,
        seasonally_adj_id INT,
        FOREIGN KEY (seasonally_adj_id) REFERENCES seasonally_adj(id)
    );
    """
    
    create_category_table = """
    CREATE TABLE category (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category_code VARCHAR(10) NOT NULL,
        data_type_id INT,
        cell_value FLOAT,
        time DATE,
        time_slot_id INT,
        FOREIGN KEY (data_type_id) REFERENCES data_type(id)
    );
    """
    
    # Execute table creation
    cursor.execute(create_seasonally_adj_table)
    cursor.execute(create_data_type_table)
    cursor.execute(create_category_table)
    connection.commit()
    print("Tables created successfully")






# Load the raw data from the JSON file
with open('data/raw_data.json') as f:
    raw_data = json.load(f)




def insert_seasonally_adj(cursor, seasonally_adj):
    #print(f"Inserting seasonally_adj: {seasonally_adj}")
    cursor.execute("SELECT id FROM seasonally_adj WHERE seasonally_adj = %s", (seasonally_adj,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO seasonally_adj (seasonally_adj) VALUES (%s)", (seasonally_adj,))
        return cursor.lastrowid




# Function to insert data type and return the ID
def insert_data_type(cursor, data_type_code, seasonally_adj_id):
    cursor.execute("SELECT id FROM data_type WHERE data_type_code = %s AND seasonally_adj_id = %s", (data_type_code, seasonally_adj_id))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO data_type (data_type_code, seasonally_adj_id) VALUES (%s, %s)", 
            (data_type_code, seasonally_adj_id)
        )
        return cursor.lastrowid

def insert_data(connection):
    cursor = connection.cursor()
    
    for row in raw_data[1:]:
        data_type_code, seasonally_adj, category_code, cell_value, _, time, _ = row
        seasonally_adj_id = insert_seasonally_adj(cursor, seasonally_adj)
        data_type_id = insert_data_type(cursor, data_type_code, seasonally_adj_id)

        # Insert the category data with its associated values
        cursor.execute(
            "INSERT INTO category (category_code, cell_value, time, data_type_id) VALUES (%s, %s, %s, %s)",
            (category_code, float(cell_value), datetime.strptime(time, '%Y-%m'), data_type_id)
        )
    
    # Commit the transaction after inserting all data
    connection.commit()
    cursor.close()

# Query the data (example query)
def query_data(connection):
    cursor = connection.cursor()
    query = """
    SELECT sa.seasonally_adj, dt.data_type_code, c.category_code, c.cell_value, c.time
    FROM category c
    JOIN data_type dt ON c.data_type_id = dt.id
    JOIN seasonally_adj sa ON dt.seasonally_adj_id = sa.id
    WHERE sa.seasonally_adj = 'yes' AND dt.data_type_code LIKE 'MPC%'
    ORDER BY c.time;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result  # Return the extracted data

def transform_data(data):
    # Convert the data into a DataFrame for further manipulation
    df = pd.DataFrame(data, columns=["seasonally_adj", "data_type_code", "category_code", "cell_value", "time"])
    df['time'] = pd.to_datetime(df['time'])  # Ensure time is in datetime format
    transformed_df = df.pivot_table(index='time', columns='category_code', values='cell_value', aggfunc='mean')
    transformed_df.sort_index(inplace=True)
    return transformed_df



def load_to_csv(df, file_name='transformed_data.csv'):
    df.to_csv(file_name)
    print(f"Data loaded to {file_name} successfully.")



# Main function to run the script
def main():
    create_database()
    connection = create_connection()
    if connection:
        create_tables(connection)
        insert_data(connection)
        data = query_data(connection)
        transformed_data = transform_data(data)
        load_to_csv(transformed_data)
        connection.close()

if __name__ == "__main__":
    main()

