from utils.get_neighborhoods import get_neighborhoods
from utils.scrape_google_maps import scrape_google_maps
from utils.save_to_excel import save_to_excel
from utils.extract_emails import extract_emails
from datetime import datetime


def main():
    global city, business_type
    city = input("Enter the city: ")
    business_type = input("Enter the business type: ")
    neighborhoods = get_neighborhoods(city)

    if not neighborhoods:
        return  # Exit if no neighborhoods found

    business_details = []
    for neighborhood in neighborhoods:
        details = scrape_google_maps(neighborhood, business_type)
        business_details.extend(details)

    first_list = name_generator()

    google_maps_results = scrape_google_maps(first_list, business_type)
    save_to_excel(business_details, google_maps_results)

    emails = extract_emails(first_list)
    second_list = name_generator(False)
    save_to_excel(emails, 'business_details_with_emails.xlsx')

    print("Scraping and email extraction completed.")


def name_generator(g=True):
    dates = datetime.today()
    date = dates.date()
    hours = dates.time().hour
    minutes = dates.time().minute
    result = f'List of {city} {business_type} ({date} {hours}:{minutes}).xlsx'
    if g:
        return result
    return f'Email {result}'


if __name__ == "__main__":
    main()
