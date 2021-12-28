from main_program import FindRecipesByIngredientMatches
from main_program import GetValidIngredientList
from main_program import app
import requests


def test_get_valid_ingredient_api_response() -> None:
    response = requests.get('http://192.168.0.18:8000/valid_ingredient_list/')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body["Ingredients"][0] == ['butter']
    assert response_body["Ingredients"][9] == ['onions']

def test_check_recipe_result_api_response() -> None:
    response = requests.get('http://192.168.0.18:8000/search_recipes_by_ingredients/parsley,bacon/10')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body['Recipes'][1]['Title']  == 'Savoy cabbage and smoked bacon soup'
    assert response_body['Recipes'][1]['Ingredients'] == '<ingredient>1 tbsp olive oil</ingredient><ingredient>1 clove garlic, chopped</ingredient><ingredient>2 baby leeks, finely chopped</ingredient><ingredient>3 rashers bacon, finely chopped</ingredient><ingredient>½ Savoy cabbage, shredded</ingredient><ingredient>500ml/18fl oz hot chicken stock</ingredient><ingredient>2 tbsp fresh parsley, finely chopped</ingredient><ingredient>2 tbsp olive oil</ingredient><ingredient>salt and freshly ground black pepper</ingredient>'
    assert response_body['Recipes'][1]['Servings'] == 'Serves 1'
    assert response_body['Recipes'][1]['Method'] == '<step1>To make the soup, heat the olive oil in a saucepan over a medium heat. Add the garlic and leeks and fry 2-3 minutes.</step1><step2>Add the chopped bacon and continue to fry for another 3-4 minutes to brown the bacon.</step2><step3>Add the cabbage and fry, stirring regularly, for 2-3 minutes, until soft.</step3><step4>Add the chicken stock and bring to the boil, then reduce the heat and simmer for 10 minutes.</step4><step5>Use a hand-blender to liquidise the soup and season, to taste, with salt and freshly ground black pepper.</step5><step6>To make the parsley oil, place the chopped parsley and the olive oil in a bowl and season, to taste, with salt and freshly ground black pepper.</step6><step7>To serve, pour the soup into a warm bowl and drizzle with the parsley oil.</step7>'
    assert response_body['Recipes'][1]['Picture_URL'] == ''





