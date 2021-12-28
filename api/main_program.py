
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from database_connnection_details import config
import time
from collections import Counter

def GetValidIngredientList():

    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    start_time = time.time()
    sqlquery = "select name from ingredient"
    cursor.execute(sqlquery)        
    ListOfValidIngredientNames = cursor.fetchall()
    print ("Getting list of all different ingredients from database took ", time.time() - start_time," seconds to run")
    return (ListOfValidIngredientNames)



def FindRecipesByIngredientMatches(UsersIngredientList, MaximumIngredientsInRecipes):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    start_time = time.time()
    UsersIngredientList= UsersIngredientList.split(",")
    recipeidlist=()
    counter=0
    while counter<len(UsersIngredientList):
        cursor.execute("select recipe_ids from ingredient where name = '"+UsersIngredientList[counter]+"'")        
        recipeidlist = sum((recipeidlist, cursor.fetchone()), ())
        counter+=1
    cursor.close()
    recipeidlist = ','.join(recipeidlist)
    recipeidlist = list(recipeidlist.split(",")) 
    # print ("recipeidlist is ", recipeidlist)
    print ("Getting a list of recipe id's from database for users ingredients took ", time.time() - start_time," seconds to run")
    start_time = time.time()
    CleanedandSortedRecipeIDList = [item for items, c in Counter(recipeidlist).most_common()
    for item in [items] * c]
    CleanedandSortedRecipeIDList = list(dict.fromkeys(CleanedandSortedRecipeIDList))
    CleanedandSortedRecipeIDListLength = len(CleanedandSortedRecipeIDList)
    if CleanedandSortedRecipeIDListLength>500:
        print ("Shortening List to 500 items..")
        CleanedandSortedRecipeIDList= CleanedandSortedRecipeIDList[0:500]       
    print ("Length of recipe id list is ",len(CleanedandSortedRecipeIDList))
    print ("Sorting recipe id list, removing duplicates, limiting to 500 id's the took ", time.time() - start_time," seconds to run")
    start_time = time.time()
    CleanedandSortedRecipeIDList= ','.join(CleanedandSortedRecipeIDList)
    sqlquery = "select id,name,ingredient_list,servings,method,picture_url from recipe where id IN ("+CleanedandSortedRecipeIDList+") AND (recipe.different_ingredients <="+MaximumIngredientsInRecipes+")"
    CleanedandSortedRecipeIDListWithoutSpeechMarks = CleanedandSortedRecipeIDList.replace("'","")
    sqlquery = sqlquery + " ORDER BY FIND_IN_SET(id,'"+CleanedandSortedRecipeIDListWithoutSpeechMarks+"'), picture_url ASC"
    print ("Querying database recipe table for recipes..")
    #print ("SQL Query is ", sqlquery)
    cursor = db.cursor()
    cursor.execute(sqlquery)        
    print ("Loading results from database into list.")
    RecipeResultList = cursor.fetchall()
    print ("Querying the database with the recipe id list took ", time.time() - start_time," seconds to run")
    cursor.close()
    #print (RecipeResultList)
    return (RecipeResultList)


app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])



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
          Servings: str
          Method: str
          Picture_URL: str


     db_tuple_with_recipe_results = FindRecipesByIngredientMatches(user_ingredient_list, maximum_ingredients_for_recipes)
     recipes = [Recipe(ID=ID, Title=Title, Ingredients=Ingredients, Servings=Servings, Method=Method, Picture_URL=Picture_URL) 
     for ID, Title, Ingredients, Servings, Method, Picture_URL in db_tuple_with_recipe_results]
     return {"Recipes": recipes}




    






    


            






