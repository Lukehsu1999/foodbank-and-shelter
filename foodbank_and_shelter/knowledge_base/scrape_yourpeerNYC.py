from bs4 import BeautifulSoup
import requests

url = 'https://yourpeer.nyc/food'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all elements with the class 'location_name'
location_elements = soup.find_all('div', class_='location_name')

# Extract and print the text from those elements
for element in location_elements:
    location_name = element.get_text(strip=True)
    print(location_name)