import requests
import json
from twilio.rest import Client
new_api = "1e19dc1a018906da0b8efe40b28304ad"

TEST_LAT = 53.349804
TEST_LONG = -6.260310

API_KEY = "2cc6c395a267574d040b98f7007418f0"
MY_LAT = 9.583555
MY_LONG = 6.546316
ENDPOINT= "https://api.openweathermap.org/data/2.5/forecast"

ACCOUNT_SID = "ACd5bb800bc1639d0f4c61c57d83310403"
AUTH_TOKEN = "4aa70083528afc79ac0615cb38b4bf71"
# ==============Parameters for API
parameter = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":API_KEY
}
# ==============Fetching weather Data for the next 12 hours (after every 3hours) from openweathermap.org
response = requests.get(url=ENDPOINT, params=parameter)
response.raise_for_status()
data = response.json()
weather_data = data["list"][:4]

# =================Creating A json file for fetched Data
with open("new_data.json", "w") as data_file:
    json.dump(weather_data, data_file, indent=4)


will_it_rain = False
condition_code_list = []
# -------------------Crating a list for weather condition code fo rthe next 12 hours ------------------#
for data in weather_data:
    index = weather_data.index(data)
    condition_code = weather_data[index]["weather"][0]["id"]
    condition_code_list.append(condition_code)
    # According tho the weather data documentation, weather codes below 700 means are codes for rain, snow etc
    if condition_code < 700:
        will_it_rain = True

if will_it_rain:
    # ------------------------------USING TWILIO API TO SEND SMS TO PHONE NUMBER WHEN THE "will_it_rain" variable is True-------------------------#
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(body=" Hey There, It's Going to 🌦️Rain Today. Remember to bring an ☔umbrella",from_="+15673523597",
    to='+2348062292004'
    )
    print(message.status)
