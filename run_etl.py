# Main function to run the script
from etl_functions import extract_data, transform_load_data

def main():
    with open('data/raw_data.json') as f:
        raw_data = json.load(f)
    df=extract_data(raw_data)
    transform_load_data(df)


if __name__ == "__main__":
    main()
