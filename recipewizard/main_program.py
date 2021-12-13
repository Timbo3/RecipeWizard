
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from recipe_list import FindRecipesByIngredientMatches
from ingredient_information import GetValidIngredientList
from typing import List
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"]
)

@app.get("/valid_ingredient_list/")
def search_by_ingredients_api_request():
     return {"Ingredients": GetValidIngredientList()}

@app.get("/search_recipes_by_ingredients/{user_ingredient_list}/{maximum_ingredients_for_recipes}")
def search_by_ingredients_api_request(user_ingredient_list:str = Path(None, description = "Comma seperated list of valid ingredient names"), 
maximum_ingredients_for_recipes:str = Path(None, description = "Integer value for maximum number of ingredients in recipe results")):

     class Recipe(BaseModel):
          ID: str
          Title: str
          Ingredients: str
          URL: str
          Picture_URL: str

     db_tuple_with_recipe_results = FindRecipesByIngredientMatches(user_ingredient_list, maximum_ingredients_for_recipes)
     recipes = [Recipe(ID=ID, Title=Title, Ingredients=Ingredients, URL=URL, Picture_URL=Picture_URL) 
     for ID, Title, Ingredients,URL,Picture_URL in db_tuple_with_recipe_results]
     return {"Recipes": recipes}




    






    


            






