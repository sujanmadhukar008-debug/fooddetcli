import requests

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
        return {}

product = get_food("4890008100309")
product = get_food("4890008100309")

if product:
    name = product.get("product_name", "Unknown")
    grade = product.get("nutriscore_grade", "?").upper()
    ingredients = product.get("ingredients_text", "Not available")
    calories = product.get("nutriments", {}).get("energy-kcal_100g", "?")
    sugars = product.get("nutriments", {}).get("sugars_100g", "?")

    print(f"\n Product: {name}")
    print(f" Nutri-score: {grade}")
    print(f" Calories: {calories} kcal per 100g")
    print(f" Sugars: {sugars}g per 100g")
    print(f"\n Ingredients: {ingredients}")
