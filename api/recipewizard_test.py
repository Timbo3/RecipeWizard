from main_program import FindRecipesByIngredientMatches
from main_program import GetValidIngredientList
from main_program import app
import requests


def test_get_valid_ingredient_api_response() -> None:
    response = requests.get('http://192.168.0.18:8000/valid_ingredient_list/')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body["Ingredients"][0] == ['olive oil']
    assert response_body["Ingredients"][3] == ['black pepper']

def test_check_recipe_result_api_response() -> None:
    response = requests.get('http://192.168.0.18:8000/search_recipes_by_ingredients/tuna,bacon/10')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body['Recipes'][0]['Title']  == 'Petit pois à la Francais'
    assert response_body['Recipes'][0]['Ingredient_Matches']  == '2'
    assert response_body['Recipes'][0]['Servings'] == 'Serves 1-2'
    assert response_body['Recipes'][0]['Picture_URL'] == ''





