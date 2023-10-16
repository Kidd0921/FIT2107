import datetime

from calculator import Calculator
import unittest
from mock import Mock


# class used to test calculator.py file
class TestCalculator(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_init(self):
        '''
        Testing done for the constructor of the calculator class. Done to make sure all instance vars 
        Are initialized correctly
        Test cases are:
        Test 1: test to see if location is initialized correctly
        Test 2: test to see if weather is initialized correctly
        Test 3: test to see if start_date_time is initialized correctly
        Test 4: test to see if end_date_time is initialized correctly
        Test 5: test to see if initial charge is initialized correctly
        Test 6: test to see if final charge is initialized correctly
        Test 7: test to see if capacity is initialized correctly
        Test 8: test to see if power is initialized correctly
        '''
        calculator = Calculator()

        # Test 1: test to see if location is initialized correctly
        self.assertEqual(calculator.location, None)

        # Test 2: test to see if weather is initialized correctly
        self.assertEqual(calculator.weather, None)

        # Test 3: test to see if start_date_time is initialized correctly
        self.assertEqual(calculator.start_date_time, None)

        # Test 4: test to see if end_date_time is initialized correctly
        self.assertEqual(calculator.end_date_time, None)

        # Test 5: test to see if initial charge is initialized correctly
        self.assertEqual(calculator.initial, None)

        # Test 6: test to see if final charge is initialized correctly
        self.assertEqual(calculator.final, None)

        # Test 7: test to see if capacity is initialized correctly
        self.assertEqual(calculator.capacity, None)

        # Test 8: test to see if power is initialized correctly
        self.assertEqual(calculator.power, None)

    def test_slash_date_to_datetime_format(self):
        '''
        Testing done for helper method to convert input date format to datetime format. Test cases are:
        Test 1: conversion of string date and time to datetime format
        '''

        # Test 1: conversion of string date and time to datetime format
        # covert date string to datetime format
        date = datetime.datetime(2021, 5, 17, 20, 30)
        self.assertEqual(self.calculator.slash_date_to_datetime_format("17/05/2021 20:30"), date)

    def test_datetime_to_dash_format(self):
        '''
        Testing done for helper method to convert date in datetime format to dash format. Test cases are:
        Test 1: conversion of string date to datetime format, where month and day input are < 10
        Test 2: conversion of string date to datetime format, where month and day input are > 10
        '''
        # Test 1: conversion of string date to datetime format, where month and day input are < 10
        date1 = datetime.datetime(2021, 5, 8)
        self.assertEqual(self.calculator.datetime_to_dash_format(date1), "2021-05-08")

        # Test 2: conversion of string date to datetime format, where month and day input are > 10
        date2 = datetime.datetime(2021, 11, 17)
        self.assertEqual(self.calculator.datetime_to_dash_format(date2), "2021-11-17")

    def test_colon_time_to_datetime_format(self):
        '''
        Testing done for helper method to convert input time format to datetime format. Test cases are:
        Test 1: conversion of string time to datetime format
        '''
        # Test 1: conversion of string time to datetime format
        time = datetime.time(20, 30, 15)
        self.assertEqual(self.calculator.colon_time_to_datetime_format("20:30:15").time(), time)

    def test_is_holiday(self):
        '''
        Testing done for helper method to check whether date entered is a public holiday or not. Test cases are:
        Test 1: When date entered is a holiday in NSW
        Test 2: When date entered is a holiday in NT
        Test 3: When date entered is a holiday in QLD
        Test 4: When date entered is a holiday in SA
        Test 5: When date entered is a holiday in TAS
        Test 6: When date entered is a holiday in VIC
        Test 7: When date entered is a holiday in WA
        '''

        # Test 1: When date entered is a holiday in NSW
        self.calculator.location = [{'state': 'NSW'}]
        self.assertTrue(self.calculator.is_holiday('26-01-2020', 2020))

        # Test 2: When date entered is a holiday in NT
        self.calculator.location = [{'state': 'NT'}]
        self.assertTrue(self.calculator.is_holiday('01-01-2019', 2019))

        # Test 3: When date entered is a holiday in QLD
        self.calculator.location = [{'state': 'QLD'}]
        self.assertTrue(self.calculator.is_holiday('25-04-2021', 2021))

        # Test 4: When date entered is a holiday in SA
        self.calculator.location = [{'state': 'SA'}]
        self.assertTrue(self.calculator.is_holiday('30-03-2018', 2018))

        # Test 5: When date entered is a holiday in TAS
        self.calculator.location = [{'state': 'TAS'}]
        self.assertTrue(self.calculator.is_holiday('13-03-2017', 2017))

        # Test 6: When date entered is a holiday in VIC
        self.calculator.location = [{'state': 'VIC'}]
        self.assertTrue(self.calculator.is_holiday('27-12-2016', 2016))

        # Test 7: When date entered is a holiday in WA
        self.calculator.location = [{'state': 'WA'}]
        self.assertTrue(self.calculator.is_holiday('26-01-2015', 2015))

        # Test 8: When location entered is not a state in australia
        self.calculator.location = [{'state': 'AA'}]
        self.assertEqual(self.calculator.is_holiday('26-01-2015', 2015), None)

    def test_is_weekday(self):
        '''
        Testing done for helper method that checks if date entered is a weekday. Test cases are:
        Test 1: when date entered is a Monday (Weekday lower bound)
        Test 2: when date entered is a Friday (Weekday upper bound)
        Test 3: when date entered is a Saturday (Weekend lower bound)
        Test 4: when date entered is a Sunday (Weekend upper bound)
        '''

        # Test 1: when date entered is a Monday (Weekday lower bound)
        self.assertTrue(self.calculator.is_weekday(datetime.datetime(2021, 9, 6)))

        # Test 2: when date entered is a Friday (Weekday upper bound)
        self.assertTrue(self.calculator.is_weekday(datetime.datetime(2021, 9, 24)))

        # Test 3: when date entered is a Saturday (Weekend lower bound)
        self.assertFalse(self.calculator.is_weekday(datetime.datetime(2021, 9, 18)))

        # Test 4: when date entered is a Sunday (Weekend upper bound)
        self.assertFalse(self.calculator.is_weekday(datetime.datetime(2021, 9, 5)))

    def test_is_peak(self):
        '''
        Test done for helper method that checks if time entered is a peak time. Test cases are:
        Test 1: when time entered is a peak lower bound
        Test 2: when date entered is a peak upper bound
        Test 3: when date entered is a before-peak lower bound
        Test 4: when date entered is a before-peak upper bound
        Test 5: when date entered is a after-peak lower bound
        Test 6: when date entered is a after-peak upper bound
        '''
        # Test 1: when time entered is a peak lower bound
        self.assertTrue(self.calculator.is_peak(6))

        # Test 2: when date entered is a peak upper bound
        self.assertTrue(self.calculator.is_peak(17))

        # Test 3: when date entered is a before-peak lower bound
        self.assertFalse(self.calculator.is_peak(0))

        # Test 4: when date entered is a before-peak upper bound
        self.assertFalse(self.calculator.is_peak(5))

        # Test 5: when date entered is a after-peak lower bound
        self.assertFalse(self.calculator.is_peak(18))

        # Test 6: when date entered is a after-peak upper bound
        self.assertFalse(self.calculator.is_peak(24))

    def test_net_energy_per_hour(self):
        '''
        Test done for method that calculates the net solar energy produced an hour. Test cases are:
        Test 1: when solar energy > charge_energy
        Test 2: when solar energy = charge_energy
        Test 3: when solar energy < charge_energy
        '''
        # Calculations - Random testing
        # Test 1: when solar energy > charge_energy
        self.assertEqual(self.calculator.net_energy_per_hour(50, 100), 0)

        # Test 2: when solar energy = charge_energy
        self.assertEqual(self.calculator.net_energy_per_hour(60, 60), 0)

        # Test 3: when solar energy < charge_energy
        self.assertEqual(self.calculator.net_energy_per_hour(70, 40), 30)

    def test_get_str_dates_of_charging_session(self):
        dates = ["25/10/2021", "26/10/2021"]
        self.assertEqual(self.calculator.get_str_dates_of_charging_session("25/10/2021", 1), dates)

    def test_get_str_times_of_charging_session(self):
        times = ["15:00", "00:00"]
        self.assertEqual(self.calculator.get_str_times_of_charging_session("15:00", 1), times)

    def test_cost(self):
        '''
        test done for main cost calculation method in calculator. Test cases are:
        Test 1: when charging happens before sunrise
        '''
        self.calculator.weather_requests = Mock()
        ret = Mock()
        ret.json.return_value = {'sunHours': 5.2, 'sunrise': '06:30:00', 'sunset': '19:30:00',
                                 'hourlyWeatherHistory': [{'hour': 0, 'cloudCoverPct': 100},
                                                          {'hour': 1, 'cloudCoverPct': 94},
                                                          {'hour': 2, 'cloudCoverPct': 87},
                                                          {'hour': 3, 'cloudCoverPct': 81},
                                                          {'hour': 4, 'cloudCoverPct': 79},
                                                          {'hour': 5, 'cloudCoverPct': 78},
                                                          {'hour': 6, 'cloudCoverPct': 76},
                                                          {'hour': 7, 'cloudCoverPct': 78},
                                                          {'hour': 8, 'cloudCoverPct': 80},
                                                          {'hour': 9, 'cloudCoverPct': 82},
                                                          {'hour': 10, 'cloudCoverPct': 67},
                                                          {'hour': 11, 'cloudCoverPct': 51},
                                                          {'hour': 12, 'cloudCoverPct': 35},
                                                          {'hour': 13, 'cloudCoverPct': 30},
                                                          {'hour': 14, 'cloudCoverPct': 24},
                                                          {'hour': 15, 'cloudCoverPct': 18},
                                                          {'hour': 16, 'cloudCoverPct': 18},
                                                          {'hour': 17, 'cloudCoverPct': 19},
                                                          {'hour': 18, 'cloudCoverPct': 19},
                                                          {'hour': 19, 'cloudCoverPct': 16},
                                                          {'hour': 20, 'cloudCoverPct': 13},
                                                          {'hour': 21, 'cloudCoverPct': 10},
                                                          {'hour': 22, 'cloudCoverPct': 8},
                                                          {'hour': 23, 'cloudCoverPct': 7}]}

        self.calculator.weather_requests.get.return_value = ret

        # Test 1: when charge until before sunrise hour
        date = "13/11/2020"
        time = "05:00"
        config = "1"
        postcode = "3800"
        duration = [0, 30, 0]
        result = 0.03
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 2: when charging happens before sunrise until during sunrise hour, where end min after sunrise, Future dates
        date = "13/11/2021"
        time = "05:00"
        config = "2"
        postcode = "3800"
        duration = [1, 31, 0]
        result = 0.82
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 3: when charging happens before sunrise until during sunrise hour, where end min before sunrise, public holiday
        date = "1/1/2020"
        time = "05:00"
        config = "3"
        postcode = "3800"
        duration = [1, 29, 0]
        result = 0.78
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 4: when charging happens before sunrise until during sunrise hour, where end and current min after sunrise
        date = "13/11/2020"
        time = "06:45"
        config = "4"
        postcode = "3800"
        duration = [0, 10, 0]
        result = 0.23
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 5: when charging happens until before sunset hour
        date = "13/11/2020"
        time = "05:00"
        config = "5"
        postcode = "3800"
        duration = [4, 0, 0]
        result = 12.35
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 6: when charging happens until during sunset hour, where end min after sunset, weekend
        date = "14/11/2020"
        time = "18:00"
        config = "6"
        postcode = "3800"
        duration = [1, 31, 0]
        result = 4.97
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 7: when charging happens until during sunset hour, end min before sunset
        date = "13/11/2020"
        time = "18:00"
        config = "7"
        postcode = "3800"
        duration = [1, 29, 0]
        result = 21.22
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 8: when charging happens until during sunset hour, end and current min after sunset, weekend
        date = "5/6/2021"
        time = "19:45"
        config = "8"
        postcode = "3800"
        duration = [0, 10, 0]
        result = 14.58
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 9: when charging happens until after sunset
        date = "13/11/2020"
        time = "18:00"
        config = "1"
        postcode = "3800"
        duration = [3, 0, 0]
        result = 0.06
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 10: when charging happens until during sunrise
        date = "13/11/2020"
        time = "5:00"
        config = "2"
        postcode = "3800"
        duration = [1, 30, 0]
        result = 0.3
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 11: when charging happens until during sunset, Future dates
        date = "4/8/2022"
        time = "18:00"
        config = "3"
        postcode = "3800"
        duration = [1, 30, 0]
        result = 0.97
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

        # Test 12: when charging happens overnight
        date = "13/11/2020"
        time = "23:59"
        config = "4"
        postcode = "3800"
        duration = [1, 0, 0]
        result = 0.74
        self.assertEqual(self.calculator.cost_calculation(date, time, config, postcode, duration), result)

    def test_time_calculation(self):
        '''
        Test done for main time calculation method in calculator. Test cases are:
        Test 1: Test done with sample user inputs to see if time calculation matches the specifications
        '''
        # Calculations - Random testing
        # Test 1: Test done with sample user inputs to see if time calculation matches the specifications
        initial_state = 5
        final_state = 90
        capacity = 120
        power_config = '6'
        self.assertEqual(self.calculator.time_calculation(initial_state, final_state, capacity, power_config),
                         [2, 50, 0])

    def test_time_calculation_in_hour(self):
        '''
        Testing done for helper method to return the amount of charging time in hours. Test cases are:
        Test 1: Test done with sample user inputs to see if time calculation matches the specifications
        '''
        # Test 1: Test done with sample user inputs to see if time calculation matches the specifications
        initial_state = 3
        final_state = 80
        capacity = 100
        power_config = '5'
        self.assertEqual(self.calculator.time_calculation_in_hour(initial_state, final_state, capacity, power_config),
                         3.5)

    def test_date_after_charging(self):
        '''
        Testing done for helper method to return the date after charging. Test cases are:
        Test 1: When charging is done across 2 days
        '''

        # Test 1: When charging is done across 2 days
        start_date = "06/06/2021"
        start_time = "23:49"
        duration = [2, 50, 0]
        end_date_time = datetime.datetime.strptime("07/06/2021 02:39", "%d/%m/%Y %H:%M")
        self.assertEqual(self.calculator.date_after_charging(start_date, start_time, duration), end_date_time)

    def test_dates_of_charging_session(self):
        '''
        Testing done for helper method to return the dates that the charging lasts for. Test cases are:
        Test 1: Testing for when charging is done in one day
        Test 2: Testing for when charging is done overnight
        '''
        # Calculations - Random testing
        # Test 1: Testing for when charging is done in one day
        start_date = "13/08/2021"
        start_time = "15:49"
        duration = [1, 30, 0]
        start_date_time = datetime.datetime.strptime("13/08/2021 15:49", "%d/%m/%Y %H:%M")
        end_date_time = datetime.datetime.strptime("13/08/2021 17:19", "%d/%m/%Y %H:%M")
        self.assertEqual(self.calculator.dates_of_charging_session(start_date, start_time, duration),
                         (start_date_time, end_date_time))

        # Test 2: Testing for when charging is done overnight
        start_date = "06/06/2021"
        start_time = "23:49"
        duration = [2, 50, 0]
        start_date_time = datetime.datetime.strptime("06/06/2021 23:49", "%d/%m/%Y %H:%M")
        end_date_time = datetime.datetime.strptime("07/06/2021 02:39", "%d/%m/%Y %H:%M")
        self.assertEqual(self.calculator.dates_of_charging_session(start_date, start_time, duration),
                         (start_date_time, end_date_time))

    def test_get_location_data(self):
        '''
        Testing done for helper method to return the location data using API. Test cases are:
        Test 1: Testing for retrieval of data from a mock location API object to see if our code calls the API correctly
        '''

        # Retrieve Data - Random Testing, Mocking
        postcode = "3800"
        search_params = {'postcode': postcode}
        url = "http://118.138.246.158/api/v1/location"

        # mock requests and mock return value
        requests = Mock()
        ret = Mock()
        ret.json.return_value = "RETURN VALUE"

        requests.get.return_value = ret

        # Test 1: Testing for retrieval of data from a mock location API object to see if our code calls the API correctly
        self.calculator.get_location_data(postcode, requests, url)
        requests.get.assert_called_once_with(url, search_params)

    def test_get_weather_data(self):
        '''
        Testing done for helper method to return the weather data using API. Test cases are:
        Test 1: Testing for retrieval of data from a mock weather API object to see if our code calls the API correctly
        '''

        # Retrieve Data - Random Testing, Mocking
        location_id = "ab9f494f-f8a0-4c24-bd2e-2497b99f2258"
        date = "2021-08-01"
        search_params = {'location': location_id, 'date': date}
        url = "http://118.138.246.158/api/v1/weather"

        # mock requests and mock return value
        requests = Mock()
        ret = Mock()
        ret.json.return_value = "RETURN VALUE"

        requests.get.return_value = ret

        # Test 1: Testing for retrieval of data from a mock weather API object to see if our code calls the API correctly
        self.calculator.get_weather_data(location_id, date, requests, url)
        requests.get.assert_called_once_with(url, search_params)

    def test_get_sun_hour(self):
        '''
        Testing done for helper method to return amount of sunHours in a day. Test cases are:
        Test 1: Testing retrieval of sunHours from the calculator's weather attribute, which is retrieved from a weather API
        '''
        # Test 1: Testing retrieval of sunHours from the calculator's weather attribute, which is retrieved from a weather API
        self.calculator.weather = {'sunrise': '07:20:00', 'sunset': '17:32:00', 'sunHours': 3.2}
        self.assertEqual(self.calculator.get_sun_hour(), 3.2)

    def test_get_day_light_length(self):
        '''
        Testing done for helper method to return the duration of daylight in a day. Test cases are:
        Test 1: Testing retrieval of daylight length from the calculator's weather attribute, which is retrieved from a weather API
        '''

        # Test 1: Testing retrieval of daylight length from the calculator's weather attribute, which is retrieved from a weather API
        self.calculator.weather = {'sunrise': '07:20:00', 'sunset': '17:32:00', 'sunHours': 3.2}
        self.assertEqual(self.calculator.get_day_light_length(), 10.2)

    def test_get_cloud_cover(self):
        '''
        Testing done for helper method to return the hourly cloud cover in a day. Test cases are:
        Test 1: Testing retrieval of hourly cloud cover from the calculator's weather attribute, which is retrieved from a weather API
        '''

        self.calculator.weather = {
            'hourlyWeatherHistory': [{'hour': 0, 'cloudCoverPct': 100}, {'hour': 1, 'cloudCoverPct': 94},
                                     {'hour': 2, 'cloudCoverPct': 87}, {'hour': 3, 'cloudCoverPct': 81},
                                     {'hour': 4, 'cloudCoverPct': 79}, {'hour': 5, 'cloudCoverPct': 78},
                                     {'hour': 6, 'cloudCoverPct': 76}, {'hour': 7, 'cloudCoverPct': 78},
                                     {'hour': 8, 'cloudCoverPct': 80}, {'hour': 9, 'cloudCoverPct': 82},
                                     {'hour': 10, 'cloudCoverPct': 67}, {'hour': 11, 'cloudCoverPct': 51},
                                     {'hour': 12, 'cloudCoverPct': 35}, {'hour': 13, 'cloudCoverPct': 30},
                                     {'hour': 14, 'cloudCoverPct': 24}, {'hour': 15, 'cloudCoverPct': 18},
                                     {'hour': 16, 'cloudCoverPct': 18}, {'hour': 17, 'cloudCoverPct': 19},
                                     {'hour': 18, 'cloudCoverPct': 19}, {'hour': 19, 'cloudCoverPct': 16},
                                     {'hour': 20, 'cloudCoverPct': 13}, {'hour': 21, 'cloudCoverPct': 10},
                                     {'hour': 22, 'cloudCoverPct': 8}, {'hour': 23, 'cloudCoverPct': 7}]}
        cloud_cover_arr = [100, 94, 87, 81, 79, 78, 76, 78, 80, 82, 67, 51, 35, 30, 24, 18, 18, 19, 19, 16, 13, 10, 8,
                           7]

        # Test 1: Testing retrieval of hourly cloud cover from the calculator's weather attribute, which is retrieved from a weather API
        self.assertEqual(self.calculator.get_cloud_cover(), cloud_cover_arr)

    def test_get_number_of_days(self):
        '''
        Testing done for helper method to return the number of days the charging lasts for. Test cases are:
        Test 1: When charging only lasts a day
        Test 2: When charging lasts 2 days
        Test 3: When chargnig lasts 2 months and 63 days
        Test 4: When charging lasts more than a year
        '''
        # Calculations - Random testing
        # Test 1: When charging only lasts a day
        self.assertEqual(self.calculator.get_number_of_days("13/11/2020", "16:48", [2, 47, 32]), 0)

        # Test 2: When charging lasts 2 days
        self.assertEqual(self.calculator.get_number_of_days("22/09/2021", "23:24", [1, 30, 0]), 1)
        # Test 3: When chargnig lasts 2 months and 63 days
        self.assertEqual(self.calculator.get_number_of_days("22/02/2021", "23:24", [1480, 24, 0]), 62)

        # Test 4: When charging lasts more than a year
        self.assertEqual(self.calculator.get_number_of_days("24/05/2021", "11:33", [9720, 12, 0]), 405)

    def test_get_reference_date(self):
        '''
        Testing done for helper method to return the reference dates when the user enteres a future date. Test cases are:
        Test 1: When date entered is in the future
        Test 2: When date entered is in the past
        '''
        # Calculations - Random testing
        # Test 1: When date entered is in the future
        date1 = [['15/11/2020', '10:23'], ['15/11/2019', '10:23'], ['15/11/2018', '10:23']]
        self.assertEqual(self.calculator.get_reference_date("15/11/2021", "10:23"), date1)
        # Test 2: When date entered is in the past
        date2 = [['14/6/2021', '20:22']]
        self.assertEqual(self.calculator.get_reference_date("14/6/2021", "20:22"), date2)


# you may create test suite if needed
if __name__ == "__main__":
    unittest.main()
    # a = TestCalculator()
    # a.test_cost()
