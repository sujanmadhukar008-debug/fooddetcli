import requests
import time

def get_food(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    
    headers = {
        "User-Agent": "fooddetcli/1.0 (learning project)"
    }
    
    try:
        res = requests.get(url, timeout=5, headers=headers)
        
        if res.status_code != 200:
            print(f"API error: status {res.status_code}")
            return {}
        
        if not res.text:
            print("Empty response from API.")
            return {}
        
        data = res.json()
        
        if data.get("status") == 0:
            print("Product not found.")
            return {}
        
        return data.get("product", {})
    
    except requests.exceptions.ConnectionError:
        print("No internet connection.")
        time.sleep(1)
        return {}



