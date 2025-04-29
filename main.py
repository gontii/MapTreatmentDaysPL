import requests
import folium

def fetch_treatment_data():
    # Updated NFZ API URL and parameters
    api_url = "https://api.nfz.gov.pl/app-itl-api/queues"
    params = {
        "page": 1,
        "limit": 10,
        "format": "json",
        "case": 1,  # Urgent mode
        "province": "07",  # Mazowieckie province
        "locality": "Siedlce"  # City
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Nieudane pobranie danych: {e}")
        return None

def process_data(data):
    # Extract relevant information (mocked for now)
    locations = [
        {"name": "Clinic A", "lat": 52.167, "lon": 22.290, "date": "2025-05-10"},
        {"name": "Clinic B", "lat": 52.162, "lon": 22.280, "date": "2025-05-12"}
    ]
    return locations

def create_map(locations):
    # Create a map centered around Siedlce
    map_center = [52.167, 22.290]
    treatment_map = folium.Map(location=map_center, zoom_start=13)

    for loc in locations:
        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            popup=f"{loc['name']}\nFirst available date: {loc['date']}",
        ).add_to(treatment_map)

    treatment_map.save("treatment_map.html")

if __name__ == "__main__":
    data = fetch_treatment_data()
    if data:
        locations = process_data(data)
        create_map(locations)
        print("Map has been created and saved as treatment_map.html")