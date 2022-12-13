import json

import requests

if __name__ == "__main__":
    url = "https://restcountries.com/v3.1/all"

    response = requests.get(url)
    data = response.json()

    countries_data = []
    for i, raw in enumerate(data):
        countries_data.append(
            dict(
                id=i + 1,
                name=raw["name"]["common"],
                code=raw["cca3"],
            )
        )

    with open("countries.json", 'w') as f:
        f.write(json.dumps(countries_data))
