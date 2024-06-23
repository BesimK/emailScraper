import pandas as pd


def get_neighborhoods(city):
    try:
        # Read the Excel file and load the sheet named after the city
        df = pd.read_excel('data/neighborhoods.xlsx', sheet_name=city)

        # Extract neighborhoods from the column
        neighborhoods = df['Neighborhood'].tolist()

        if not neighborhoods:
            print(f'No neighborhoods found for {city}.')
            return []

        return neighborhoods
    except Exception as e:
        print(f'Error reading neighborhoods for {city}: {e}')
        return []
