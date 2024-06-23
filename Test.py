from utils import helpers
from utils.get_neighborhoods import get_neighborhoods
from utils.scrape_google_maps import scrape_google_maps
from utils.helpers import save_to_excel


def main():
    city = "İstanbul"
    business_type = "Avukat"
    neighborhoods = get_neighborhoods(city)

    if not neighborhoods:
        print("No neighborhoods found. Please fill excel file")
        return  # Exit if no neighborhoods found

    business_details = []
    for neighborhood in neighborhoods:
        details = scrape_google_maps(neighborhood, business_type)
        business_details.extend(details)

    result_list = helpers.name_generator(city, business_type)
    save_to_excel(business_details, result_list)
    print("Scraping and email extraction completed.")


if __name__ == "__main__":
    main()
