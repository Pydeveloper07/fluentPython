# dict Comprehensions
def build_dict():
    DIAL_CODES = [
        (99, 'Uzbekistan'),
        (94, 'USA'),
        (86, 'China'),
        (91, 'India'),
        (62, 'Indonesia')
    ]

    country_code = {country: code for code, country in DIAL_CODES}
    print(country_code)


if __name__ == "__main__":
    build_dict()
