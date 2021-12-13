from recipe_list import FindRecipesByIngredientMatches
from main_program import app
import requests


def test_get_valid_ingredient_api_response() -> None:
    response = requests.get('http://192.168.0.24:8000/valid_ingredient_list/')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body["Ingredients"][0] == ['butter']
    assert response_body["Ingredients"][9] == ['onions']

def test_check_recipe_result_api_response() -> None:
    response = requests.get('http://192.168.0.24:8000/search_recipes_by_ingredients/gravy,tapenade/100')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body['Recipes'][0]['Title']  == 'Boned roast leg of lamb'
    assert response_body['Recipes'][0]['Ingredients'] == 'garlic, potatoes, honey, feta cheese, anchovies, beans, leg of lamb, gravy, tapenade'
    assert response_body['Recipes'][0]['URL'] == 'https://www.google.co.uk/search?q=Boned roast leg of lamb'
    assert response_body['Recipes'][0]['Picture_URL'] == 'http://res.cloudinary.com/uktv/image/upload/v1420626176/mfda7erqx2ll8pagddlh.jpg'





