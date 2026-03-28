import click
import requests
from fetch import get_food

@click.group()
def cli():
    pass

@cli.command()
@click.option("--barcode", prompt="Enter barcode", help="Product barcode number")
def search(barcode):
    click.echo("\nFetching food data...\n")
    product = get_food(barcode)

    if not product:
        click.secho("No product found.", fg="red")
        return

    name = product.get("product_name", "Unknown")
    grade = product.get("nutriscore_grade", "?").upper()
    calories = product.get("nutriments", {}).get("energy-kcal_100g", "?")
    sugars = product.get("nutriments", {}).get("sugars_100g", "?")
    ingredients = product.get("ingredients_text", "Not available")

    click.secho(f" {name}", bold=True)
    
    if grade in ["A", "B"]:
        click.secho(f" Nutri-score: {grade}", fg="green")
    elif grade == "C":
        click.secho(f" Nutri-score: {grade}", fg="yellow")
    else:
        click.secho(f" Nutri-score: {grade}", fg="red")

    click.echo(f" Calories: {calories} kcal per 100g")
    click.echo(f" Sugars: {sugars}g per 100g")
    click.echo(f"\n Ingredients: {ingredients}\n")


@cli.command()
@click.option("--name", prompt="Enter food name", help="Search by product name")
def find(name):
    click.echo(f"\nSearching for '{name}'...\n")
    
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&json=1&page_size=5"
    headers = {"User-Agent": "fooddetcli/1.0 (learning project)"}
    
    try:
        res = requests.get(url, timeout=10, headers=headers)
        
        if not res.text:
            click.secho("No response from API. Try again.", fg="yellow")
            return
            
        if res.status_code != 200:
            click.secho(f"API error: {res.status_code}", fg="red")
            return
            
        products = res.json().get("products", [])
        
        if not products:
            click.secho("No products found.", fg="red")
            return
        
        for i, p in enumerate(products, 1):
            pname = p.get("product_name", "Unknown")
            brand = p.get("brands", "Unknown brand")
            grade = p.get("nutriscore_grade", "?").upper()
            
            if grade in ["A", "B"]:
                color = "green"
            elif grade == "C":
                color = "yellow"
            else:
                color = "red"
            
            click.echo(f" {i}. {pname} — {brand}")
            click.secho(f"    Nutri-score: {grade}\n", fg=color)
    
    except Exception as e:
        click.secho(f"Something went wrong: {e}", fg="red")


@cli.command()
@click.option("--barcode1", prompt="Enter first barcode", help="First product barcode")
@click.option("--barcode2", prompt="Enter second barcode", help="Second product barcode")
def compare(barcode1, barcode2):
    click.echo("\nComparing products...\n")
    
    p1 = get_food(barcode1)
    p2 = get_food(barcode2)
    
    if not p1 or not p2:
        click.secho("Could not fetch one or both products.", fg="red")
        return
    
    def get_info(p):
        return {
            "name": p.get("product_name", "Unknown"),
            "grade": p.get("nutriscore_grade", "?").upper(),
            "calories": p.get("nutriments", {}).get("energy-kcal_100g", "?"),
            "sugars": p.get("nutriments", {}).get("sugars_100g", "?"),
            "fat": p.get("nutriments", {}).get("fat_100g", "?"),
        }
    
    a = get_info(p1)
    b = get_info(p2)
    
    click.echo(f" {'PRODUCT':<25} {'OPTION A':<20} {'OPTION B':<20}")
    click.echo(f" {'-'*65}")
    click.echo(f" {'Name':<25} {a['name'][:18]:<20} {b['name'][:18]:<20}")
    click.echo(f" {'Nutri-score':<25} {a['grade']:<20} {b['grade']:<20}")
    click.echo(f" {'Calories/100g':<25} {str(a['calories'])+'kcal':<20} {str(b['calories'])+'kcal':<20}")
    click.echo(f" {'Sugars/100g':<25} {str(a['sugars'])+'g':<20} {str(b['sugars'])+'g':<20}")
    click.echo(f" {'Fat/100g':<25} {str(a['fat'])+'g':<20} {str(b['fat'])+'g':<20}")
    
    grade_order = ["A", "B", "C", "D", "E"]
    a_rank = grade_order.index(a['grade']) if a['grade'] in grade_order else 99
    b_rank = grade_order.index(b['grade']) if b['grade'] in grade_order else 99
    
    click.echo(f"\n {'-'*65}")
    if a_rank < b_rank:
        click.secho(f" Winner: {a['name']} is healthier.", fg="green")
    elif b_rank < a_rank:
        click.secho(f" Winner: {b['name']} is healthier.", fg="green")
    else:
        click.secho(" Both products have the same nutri-score.", fg="yellow")


if __name__ == "__main__":
    cli()
