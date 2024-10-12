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
