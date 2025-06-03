import requests

def get_ip_geolocation():
    try:
        # Get the public IP address and geolocation information
        public_ip = requests.get('https://api.ipify.org').text
        response = requests.get(f'https://ipinfo.io/{public_ip}/json')
        response.raise_for_status()
        data = response.json()
        location = data.get('loc', '0,0').split(',')
        return location[0], location[1]
    except requests.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None, None

def reverse_geocode(latitude, longitude):
    try:
        # Add User-Agent to the request header
        headers = {'User-Agent': 'MyGeocodingApp/1.0 (myemail@example.com)'}
        reverse_geocode_url = f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1'
        address_response = requests.get(reverse_geocode_url, headers=headers)
        
        # Check for HTTP errors
        address_response.raise_for_status()
        address_data = address_response.json()
        address = address_data.get('address', {})
        city = address.get('city', 'N/A')
        state = address.get('state', 'N/A')
        country = address.get('country', 'N/A')
        return f"{city}, {state}, {country}"
    except requests.RequestException as e:
        print(f"Error fetching address: {e}")
        return "Address not found"

def location():
    latitude, longitude = get_ip_geolocation()
    if latitude and longitude:
        return reverse_geocode(latitude, longitude)
    return "Location not found"

#print(location())
