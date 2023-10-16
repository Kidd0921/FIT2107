# # # importing the requests library
# # import requests
# # from unittest.mock import Mock

# # # # api-endpoint
# # # URL = "http://118.138.246.158/api/v1/location"
# # # URL2 = "http://118.138.246.158/api/v1/weather"

# # # # location given here
# # # location = "3800"
# # # l1 = "ab9f494f-f8a0-4c24-bd2e-2497b99f2258"
# # # date = "2021-08-01"

# # # # defining a params dict for the parameters to be sent to the API
# # # PARAMS = {'postcode': location}
# # # PARAMS1 = {'location': l1, 'date': date}

# # # # sending get request and saving the response as response object
# # # r = requests.get(url=URL, params=PARAMS)
# # # r1 = requests.get(url=URL2, params=PARAMS1)

# # # # extracting data in json format
# # # data = r.json()
# # # d1 = r1.json()

# # # print(d1['sunHours'], d1['sunset'])
# # # print("a")
# # # print("a")


# # def get_location_data(post_code, requests, url):
# #     search_params = {'postcode': post_code}
# #     search_request = requests.get(url, search_params)
# #     return search_request.json()

# # def test_get_location_data():
# #     #define inputs
# #     postcode = "1234"
# #     search_params = {'postcode': postcode}
# #     url = "URL HERE"

# #     #mock and mock return value
# #     requests = Mock()
# #     b = Mock()
# #     b.json.return_value = "Here"
# #     requests.get.return_value = b

# #     print(get_location_data(postcode, requests, url))

# #     requests.get.assert_called_once_with(url, search_params)


# # test_get_location_data()

# # # def get_weather_data(self, location_id, date, requests):
# # #     search_params = {'location': location_id, 'date': date}
# # #     search_request = requests.get(url=self.WEATHER_URL, params=search_params)
# # #     self.weather = search_request.json()

# from datetime import datetime
# def validate(date_text):
#     try:
#         if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
#             raise ValueError
#         return True
#     except ValueError:
#         return False

# print(validate("aaaa-12-12"))