from os import cpu_count, spawnl, stat_result
import holidays
from datetime import datetime
from datetime import timedelta

import requests


class Calculator():
    # api-endpoint
    LOCATION_URL = "http://118.138.246.158/api/v1/location"
    WEATHER_URL = "http://118.138.246.158/api/v1/weather"
    POWER_CONFIGURATIONS = {"1": 2, "2": 3.6, "3": 7.2, "4": 11, "5": 22, "6": 36, "7": 90, "8": 350}
    COST = {"1": 5, "2": 7.5, "3": 10, "4": 12.5, "5": 15, "6": 20, "7": 30, "8": 50}

    # you can choose to initialise variables here, if needed.
    def __init__(self):
        self.location = None
        self.weather = None
        self.start_date_time = None
        self.end_date_time = None
        self.initial = None
        self.final = None
        self.capacity = None
        self.power = None
        self.location_requests = requests
        self.weather_requests = requests

    def slash_date_to_datetime_format(self, date_time_str):
        return datetime.strptime(date_time_str, "%d/%m/%Y %H:%M")

    def datetime_to_dash_format(self, datetime):
        string = str(datetime.year)
        if datetime.month < 10:
            string += "-0"
        else:
            string += "-"
        string += str(datetime.month)

        if datetime.day < 10:
            string += "-0"
        else:
            string += "-"
        string += str(datetime.day)

        return string

    def colon_time_to_datetime_format(self, time_str):
        return datetime.strptime(time_str, "%H:%M:%S")

    def is_holiday(self, date, year):
        state = self.location[0]['state']
        if state == 'NSW':
            return date in holidays.AU(prov="NSW", years=year)
        elif state == 'NT':
            return date in holidays.AU(prov="NT", years=year)
        elif state == 'QLD':
            return date in holidays.AU(prov="QLD", years=year)
        elif state == 'SA':
            return date in holidays.AU(prov="SA", years=year)
        elif state == 'TAS':
            return date in holidays.AU(prov="TAS", years=year)
        elif state == 'VIC':
            return date in holidays.AU(prov="VIC", years=year)
        elif state == 'WA':
            return date in holidays.AU(prov="WA", years=year)

    def is_weekday(self, datetime):
        if 0 <= datetime.weekday() <= 4:
            return True
        return False

    def is_peak(self, hour):
        if 6 <= hour < 18:
            return True
        elif 0 <= hour < 6 or 18 <= hour <= 24:
            return False

    def net_energy_per_hour(self, charge_energy, solar_energy):
        if solar_energy >= charge_energy:
            return 0
        else:
            return charge_energy - solar_energy

    def get_str_dates_of_charging_session(self, start_date, number_of_days):
        start_date_time = datetime.strptime(start_date, "%d/%m/%Y")
        dates = [start_date]
        for _ in range(number_of_days):
            current_date = start_date_time + timedelta(days=1)
            dates.append(str(current_date.day) + "/" + str(current_date.month) + "/" + str(current_date.year))
        return dates

    def get_str_times_of_charging_session(self, start_time, number_of_days):
        times = [start_time]
        for _ in range(number_of_days):
            times.append("00:00")
        return times

    def cost_calculation(self, start_date, start_time, charger_config, post_code, duration):

        number_of_days = self.get_number_of_days(start_date, start_time, duration)

        # setting up var for processing
        start_date_time, end_date_time = self.dates_of_charging_session(start_date, start_time, duration)
        dates_of_charging_session = self.get_str_dates_of_charging_session(start_date, number_of_days)
        times_of_charging_session = self.get_str_times_of_charging_session(start_time, number_of_days)
        total_cost = 0

        # for each day in the date array
        for i in range(number_of_days + 1):

            # getting values for the current day
            current_date = dates_of_charging_session[i]
            current_time = times_of_charging_session[i]
            current_date_time = self.slash_date_to_datetime_format(current_date + " " + current_time)
            dates = self.get_reference_date(current_date, current_time)

            average_cost = 0

            # for each date calculated
            for date in dates:

                # getting variables for processing
                self.get_location_data(post_code, self.location_requests, self.LOCATION_URL)
                self.get_weather_data(self.location[0]['id'], self.datetime_to_dash_format(current_date_time),
                                      self.weather_requests, self.WEATHER_URL)
                si = self.get_sun_hour()
                dl = self.get_day_light_length()
                cc_arr = self.get_cloud_cover()
                sunrise = self.colon_time_to_datetime_format(self.weather['sunrise'])
                sunset = self.colon_time_to_datetime_format(self.weather['sunset'])

                cost = 0
                energy_needed_in_one_hour = self.POWER_CONFIGURATIONS[charger_config]
                base_price = self.COST[charger_config] / 100
                current_hour = current_date_time.hour
                current_minute = current_date_time.minute

                # checking to see if the current date is the final day of charging
                # then deciding the max final hour that can be charged until
                if current_date_time.date() == end_date_time.date():
                    end_hour = end_date_time.hour
                else:
                    end_hour = 23

                # while not charged
                while current_hour <= end_hour:

                    # getting charging time and solar duration for each hour
                    charging_time = 0
                    solar_duration = 0

                    # if this is not the last hour of charging
                    if current_hour < end_hour:

                        # getting minutes charged this hour
                        charging_time = 60 - current_minute

                        # if this is before sunrise
                        if current_hour < sunrise.hour:
                            # then no solar
                            solar_duration = 0
                        # elif current hour is sunrise
                        elif current_hour == sunrise.hour:
                            # getting solar duration
                            # if current minute is before sunrise
                            if current_minute < sunrise.minute:
                                solar_duration = 60 - sunrise.minute
                            # if current minute is after or during sunrise
                            else:
                                solar_duration = 60 - current_minute
                        # if current hour is near sunset
                        else:

                            # if current hour before sunset
                            if current_hour < sunset.hour:
                                # solar duration is the number of minutes charged this hour
                                solar_duration = 60 - current_minute
                            # elif the current hour is sunset
                            elif current_hour == sunset.hour:

                                # if before sunset
                                if current_minute < sunset.minute:
                                    # solar is the sunset minute this hour - current minute
                                    solar_duration = sunset.minute - current_minute
                                # if during or after sunset, then solar is 0
                                else:
                                    solar_duration = 0
                            # else, if after sunset then no solar duration
                            else:
                                solar_duration = 0
                    # if this is the last hour of charging
                    else:
                        # charging time is dependent on the last minute of charge, not 60 mins (normal hour)
                        charging_time = end_date_time.minute - current_minute

                        # if current hour is before sunrise
                        if current_hour < sunrise.hour:

                            # no solar duration
                            solar_duration = 0

                        # elif current hour is sunrise
                        elif current_hour == sunrise.hour:

                            # if end charging minute is before sunrise
                            if current_minute <= end_date_time.minute <= sunrise.minute:

                                # no sun
                                solar_duration = 0

                            # if end charging minute is after sunrise
                            elif current_minute <= sunrise.minute <= end_date_time.minute:

                                # sun = the end minute - sunrise
                                solar_duration = end_date_time.minute - sunrise.minute

                            # if both end charging time and current time is after sunrise
                            elif sunrise.minute <= current_minute <= end_date_time.minute:

                                # sun = end minute - current minute
                                solar_duration = end_date_time.minute - current_minute

                        # else if the time is near sunset
                        else:

                            # if current hour is before sunset
                            if current_hour < sunset.hour:

                                # amount of sun = end minute - current minute
                                solar_duration = end_date_time.minute - current_minute

                            # if the current hour is sunset
                            elif current_hour == sunset.hour:

                                # if end minute is before sunset
                                if current_minute <= end_date_time.minute <= sunset.minute:

                                    # solar = the end minute - current minute
                                    solar_duration = end_date_time.minute - current_minute

                                # if end minute is after sunset
                                elif current_minute <= sunset.minute <= end_date_time.minute:

                                    # solar = sunset minute - current minute
                                    solar_duration = sunset.minute - current_minute

                                # if current minute and end minute is after sunset
                                elif sunset.minute <= current_minute <= end_date_time.minute:
                                    # no sun
                                    solar_duration = 0
                            # if current hour is after sunset
                            else:
                                # no sun
                                solar_duration = 0

                    # if the current hour is between sunrise and sunset, calc the energy generated
                    # else, solar energy is 0
                    if sunrise.hour <= current_hour <= sunset.hour:
                        solar_generated = si * solar_duration / 60 / dl * (
                                1 - cc_arr[current_hour] / 100) * 50 * 0.2
                    else:
                        solar_generated = 0

                    # calculating net energy and culculating cost saved due to solar
                    net_energy = self.net_energy_per_hour(energy_needed_in_one_hour * charging_time / 60,
                                                          solar_generated)
                    cost_per_hour = base_price * net_energy

                    # mutlipliers for special days and time
                    if self.is_holiday(start_date, current_date_time.year) or self.is_weekday(start_date_time):
                        cost_per_hour *= 1.1
                    if not self.is_peak(current_hour):
                        cost_per_hour *= 0.5

                    # adding cost per hour to cost and ressetting vars for next iter
                    current_minute = 0
                    current_hour += 1
                    cost += cost_per_hour
                # avg = cost/len
                average_cost += cost
            total_cost += average_cost
        return round(total_cost, 2)

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity, charger_configuration):
        self.initial = initial_state
        self.final = final_state
        self.capacity = capacity
        # self.power = power
        time = (final_state - initial_state) / 100 * capacity / self.POWER_CONFIGURATIONS[charger_configuration]
        hour = int(time)
        minute = int((time * 60) % 60)
        second = int((time * 3600) % 60)
        return [hour, minute, second]

    def time_calculation_in_hour(self, initial_state, final_state, capacity, charger_configuration):
        self.initial = initial_state
        self.final = final_state
        self.capacity = capacity
        # self.power = power
        time = (final_state - initial_state) / 100 * capacity / self.POWER_CONFIGURATIONS[charger_configuration]
        return time

    def date_after_charging(self, start_date: str, start_time: str, duration):
        datetime_str = start_date + " " + start_time
        start_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")
        end_datetime = start_datetime + timedelta(hours=duration[0], minutes=duration[1], seconds=duration[2])
        self.end_date_time = end_datetime
        self.start_date_time = start_datetime
        return end_datetime

    def dates_of_charging_session(self, start_date: str, start_time: str, duration):
        start_datetime = datetime.strptime(start_date + " " + start_time, "%d/%m/%Y %H:%M")
        end_datetime = start_datetime + timedelta(hours=duration[0], minutes=duration[1], seconds=duration[2])
        return start_datetime, end_datetime

    '''
    API METHODS TO GET THESE:
    1. solar insolation
    2. daylight length
    3. cloud cover
    '''

    def get_location_data(self, post_code, requests, url):
        search_params = {'postcode': post_code}
        search_request = requests.get(url, search_params)
        self.location = search_request.json()

    def get_weather_data(self, location_id, date, requests, url):
        search_params = {'location': location_id, 'date': date}
        search_request = requests.get(url, search_params)
        self.weather = search_request.json()

    # to be acquired through API
    def get_sun_hour(self):
        return self.weather['sunHours']

    # to be acquired through API
    def get_day_light_length(self):
        sunrise = self.weather['sunrise']
        sunset = self.weather['sunset']
        hours1, minutes1, seconds1 = sunrise.split(":")
        hours2, minutes2, seconds2 = sunset.split(":")
        hours1 = int(hours1) + int(minutes1) / 60 + int(seconds1) / 3600
        hours2 = int(hours2) + int(minutes2) / 60 + int(seconds2) / 3600
        dl = hours2 - hours1
        return round(dl, 2)

    # to be acquired through API
    def get_cloud_cover(self):
        cloud_cover = []

        # for each hour
        for i in range(len(self.weather['hourlyWeatherHistory'])):
            cloud_cover.append(self.weather['hourlyWeatherHistory'][i]['cloudCoverPct'])

        return cloud_cover

    def get_number_of_days(self, start_date, start_time, duration):
        a, b = self.dates_of_charging_session(start_date, start_time, duration)
        diff = b.date() - a.date()
        return diff.days

    def get_reference_date(self, start_date: str, start_time: str):
        dates = []
        start_date_time = self.slash_date_to_datetime_format(start_date + " " + start_time)
        present = datetime.today() - timedelta(days=2)
        isFuture = False

        if start_date_time > present:
            isFuture = True

        if isFuture:
            for i in range(3):
                previous_year = present.year - (i + 1)
                previous_date = str(start_date_time.day) + "/" + str(start_date_time.month) + "/" + str(previous_year)
                dates.append([previous_date, start_time])
        else:
            dates.append([start_date, start_time])

        return dates
