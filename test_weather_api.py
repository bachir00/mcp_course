"""
Test script pour explorer l'API weather.gov
Ce script teste différentes façons d'obtenir des données météo
"""
import asyncio
import httpx
import json
from datetime import datetime

# Configuration de base
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-test/1.0"

async def test_api_call(url: str, description: str = ""):
    """Fonction helper pour tester les appels API"""
    print(f"\n{'='*60}")
    print(f"🔍 TEST: {description}")
    print(f"📡 URL: {url}")
    print(f"{'='*60}")
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Réponse reçue: {len(str(data))} caractères")
                
                # Afficher la structure JSON de manière lisible
                print(f"🔍 Structure de la réponse:")
                print(json.dumps(data, indent=2)[:1000] + "..." if len(str(data)) > 1000 else json.dumps(data, indent=2))
                
                return data
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                print(f"📄 Réponse: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None

async def explore_weather_api():
    """Explore l'API weather.gov pour comprendre son fonctionnement"""
    
    print("🌦️  EXPLORATION DE L'API WEATHER.GOV")
    print("="*60)
    
    # Test 1: Obtenir des informations sur un point géographique
    # Coordonnées de New York City comme exemple
    latitude = 40.7128
    longitude = -74.0060
    
    points_data = await test_api_call(
        f"{NWS_API_BASE}/points/{latitude},{longitude}",
        f"Informations du point géographique (NYC: {latitude}, {longitude})"
    )
    
    if not points_data:
        print("❌ Impossible de continuer sans les données du point")
        return
    
    # Extraire les URLs importantes
    properties = points_data.get("properties", {})
    forecast_url = properties.get("forecast")
    forecast_hourly_url = properties.get("forecastHourly")
    observation_stations_url = properties.get("observationStations")
    
    print(f"\n🔗 URLs importantes extraites:")
    print(f"   📅 Forecast: {forecast_url}")
    print(f"   🕐 Forecast Hourly: {forecast_hourly_url}")
    print(f"   🏗️  Observation Stations: {observation_stations_url}")
    
    # Test 2: Obtenir les prévisions météo
    if forecast_url:
        forecast_data = await test_api_call(
            forecast_url,
            "Prévisions météo (7 jours)"
        )
    
    # Test 3: Obtenir les prévisions horaires
    if forecast_hourly_url:
        hourly_data = await test_api_call(
            forecast_hourly_url,
            "Prévisions horaires"
        )
    
    # Test 4: Obtenir les stations d'observation
    if observation_stations_url:
        stations_data = await test_api_call(
            observation_stations_url,
            "Stations d'observation météo"
        )
        
        # Test 5: Obtenir les observations actuelles
        if stations_data and stations_data.get("features"):
            station_id = stations_data["features"][0]["properties"]["stationIdentifier"]
            observations_url = f"{NWS_API_BASE}/stations/{station_id}/observations/latest"
            
            await test_api_call(
                observations_url,
                f"Observations actuelles de la station {station_id}"
            )
    
    # Test 6: Tester les alertes météo pour New York
    alerts_data = await test_api_call(
        f"{NWS_API_BASE}/alerts/active/area/NY",
        "Alertes météo actives pour New York State"
    )
    
    # Test 7: Explorer d'autres endpoints
    print(f"\n🔍 EXPLORATION D'AUTRES ENDPOINTS:")
    
    # Test des zones
    zones_data = await test_api_call(
        f"{NWS_API_BASE}/zones/forecast/NYZ072",
        "Zone de prévision NYC"
    )
    
    # Résumé des découvertes
    print(f"\n{'='*60}")
    print("📋 RÉSUMÉ DES DÉCOUVERTES:")
    print("="*60)
    print("1. Pour obtenir la météo d'un lieu:")
    print("   a) Utilisez /points/{lat},{lon} pour obtenir les URLs de prévision")
    print("   b) Utilisez l'URL 'forecast' pour les prévisions 7 jours")
    print("   c) Utilisez l'URL 'forecastHourly' pour les prévisions horaires")
    print("   d) Utilisez 'observationStations' puis /stations/{id}/observations/latest pour les conditions actuelles")
    print("\n2. Pour les alertes:")
    print("   - Utilisez /alerts/active/area/{state} pour les alertes par état")
    print("\n3. Headers requis:")
    print("   - User-Agent: obligatoire")
    print("   - Accept: application/geo+json recommandé")

async def test_specific_locations():
    """Teste plusieurs lieux spécifiques"""
    
    locations = [
        {"name": "Paris (approximatif)", "lat": 48.8566, "lon": 2.3522},
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
        {"name": "Miami", "lat": 25.7617, "lon": -80.1918}
    ]
    
    print(f"\n🌍 TEST DE PLUSIEURS LOCATIONS:")
    print("="*60)
    
    for location in locations:
        print(f"\n📍 Testant: {location['name']}")
        
        points_data = await test_api_call(
            f"{NWS_API_BASE}/points/{location['lat']},{location['lon']}",
            f"Point pour {location['name']}"
        )
        
        if points_data:
            properties = points_data.get("properties", {})
            rel_location = properties.get("relativeLocation", {}).get("properties", {})
            
            print(f"   🏙️  Ville détectée: {rel_location.get('city', 'N/A')}")
            print(f"   🗺️  État: {rel_location.get('state', 'N/A')}")
            print(f"   ✅ Forecast URL disponible: {'Oui' if properties.get('forecast') else 'Non'}")
        else:
            print(f"   ❌ Pas de données disponibles pour {location['name']}")

async def main():
    """Fonction principale"""
    print(f"🚀 Démarrage de l'exploration de l'API Weather.gov")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    await explore_weather_api()
    await test_specific_locations()
    
    print(f"\n✅ Exploration terminée!")
    print(f"💡 Consultez les résultats ci-dessus pour comprendre comment utiliser l'API")

if __name__ == "__main__":
    asyncio.run(main())