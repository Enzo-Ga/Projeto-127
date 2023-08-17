from bs4 import BeautifulSoup
import requests
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

def scrape():
    response = requests.get(START_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    bright_star_table = soup.find("table", class_="wikitable")

    table_body = bright_star_table.find("tbody")

    table_rows = table_body.find_all("tr")

    scraped_data = []

    for row in table_rows[1:]:  # Pular a linha de cabeçalho
        table_cols = row.find_all("td")
        temp_list = []

        for col_data in table_cols:
            data = col_data.get_text().strip()
            temp_list.append(data)

        scraped_data.append(temp_list)

    return scraped_data

scraped_data = scrape()

stars_data = []

for data_row in scraped_data:
    Star_names = data_row[1]
    Distance = data_row[3]
    Mass = data_row[5]
    Radius = data_row[6]
    Lum = data_row[7]

    required_data = [Star_names, Distance, Mass, Radius, Lum]
    stars_data.append(required_data)

headers = ["Star_names", "Distance", "Mass", "Radius", "Luminosity"]

star_df_1 = pd.DataFrame(stars_data, columns=headers)

star_df_1.to_csv("scraped_data.csv", index=True, index_label="id")
