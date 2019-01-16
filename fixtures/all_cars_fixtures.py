get_all_cars_query = '''query {
    cars {
        name
        colour
        model
    }
}
'''

get_all_cars_query_response = {
    "data": {
        "cars": [
            {
                "name": "BMW",
                "colour": "black",
                "model": "BMW"
            }
        ]
    }
}
