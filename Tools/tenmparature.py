import requests
from bs4 import BeautifulSoup

def temparature():
    # Headers to mimic a browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    
    # Make a GET request to fetch the city weather page
    city_response = requests.get("https://www.accuweather.com/en/in/kolkata/206690/weather-forecast/206690", headers=headers)
    
    if city_response.status_code == 200:
        city_soup = BeautifulSoup(city_response.content, 'html.parser')
        
        # Extract temperature and weather description
        temperature_tag = city_soup.find(class_='temp')
        weather_desc_tag = city_soup.find(class_='phrase')
        
        if temperature_tag and weather_desc_tag:
            temperature = temperature_tag.text.strip()
            weather_description = weather_desc_tag.text.strip()
            
            return(f"Temperature is {temperature} and Weather is {weather_description}")
        else:
            print("Could not find temperature or weather description on the page.")
    else:
        print(f"Failed to fetch city weather page: {city_response.status_code}")

if __name__ == "__main__":
    print(temparature())