from datetime import datetime

import pandas as pd


def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


def name_generator(city, business_type):
    dates = datetime.today()
    # date = dates.date()
    # hours = dates.time().hour
    # minutes = dates.time().minute
    return f'List_of_{city}_{business_type}.xlsx'

