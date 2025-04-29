import requests
import folium

def fetch_treatment_data():
    # Updated NFZ API URL and parameters
    api_url = "https://api.nfz.gov.pl/app-itl-api/queues"
    params = {
        "page": 1,
        "limit": 10,
        "format": "json",
        "case": 2,  # Urgent mode
        "province": "07",  # Mazowieckie province
        "benefit": "KOLONOSKOPIA",  # Treatment type
        "locality": "SIEDLCE"  # City
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Nieudane pobranie danych: {e}")
        return None

def process_data(data):
    # Extract relevant information from the API response
    locations = []

    for item in data.get("data", []):
        location = {
            "name": item.get("attributes", {}).get("provider", "Błąd pobrania nazwy"),
            "lat": item.get("attributes", {}).get("latitude", {}),
            "lon": item.get("attributes", {}).get("longitude", {}),
            "date": item.get("attributes",{}).get("dates","Błąd pobrania klucza (dates)").get("date", "Błąd pobrania konkretnej daty (dates)")
        }
        if location["lat"] and location["lon"]:  # Ensure coordinates are available
            locations.append(location)

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