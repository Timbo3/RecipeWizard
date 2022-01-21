
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
    sqlquery = "select display_name from ingredient ORDER BY CHAR_LENGTH(recipe_ids) DESC"
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
        cursor.execute("select recipe_ids from ingredient where display_name = '"+UsersIngredientList[counter]+"'")        
        recipeidlist = sum((recipeidlist, cursor.fetchone()), ())
        counter+=1
    cursor.close()
    recipeidlist = ''.join(recipeidlist)   
    recipeidlist=recipeidlist.replace("</id>","")
    recipeidlist = list(recipeidlist.split("<id>")) 
    recipeidlist.pop(0)
    runtime = round(time.time() - start_time, 2)
    print ("Getting list of recipe ID's from database for users ingredients took ", runtime," seconds to run")
    start_time = time.time()  
    CleanedandSortedRecipeIDList = [item for items, c in Counter(recipeidlist).most_common()
    for item in [items] * c]
    my_dict = {i:CleanedandSortedRecipeIDList.count(i) for i in CleanedandSortedRecipeIDList}
    CleanedandSortedRecipeIDList = list(my_dict.items())
    CleanedandSortedRecipeIDListLength = len(CleanedandSortedRecipeIDList)
    if CleanedandSortedRecipeIDListLength>500:
        CleanedandSortedRecipeIDList= CleanedandSortedRecipeIDList[0:500]       
    start_time = time.time()
    counter = 0
    CleanedandSortedRecipeIDListString=""
    while counter<len(CleanedandSortedRecipeIDList):
        CleanedandSortedRecipeIDListString= CleanedandSortedRecipeIDListString+CleanedandSortedRecipeIDList[counter][0]+","
        counter = counter+1
    CleanedandSortedRecipeIDListString = CleanedandSortedRecipeIDListString[:-1]
    runtime = round(time.time() - start_time, 2)
    print ("Sorting the recipe ID list by frequency, removing duplicates, limiting to 500 ID's, converting to a string took ", runtime," seconds to run")
    sqlquery = "select id,name,different_ingredients,ingredient_list,servings,method,picture_url from recipe where id IN ("+CleanedandSortedRecipeIDListString+") AND (recipe.different_ingredients <="+MaximumIngredientsInRecipes+")"
    cursor = db.cursor()
    cursor.execute(sqlquery)        
    RecipeResultList = cursor.fetchall()
    runtime = round(time.time() - start_time, 2)
    print ("Getting recipe information from database with the recipe ID list took ", runtime," seconds to run")
    cursor.close()
    start_time = time.time()
    RecipeResultList = [list(elem) for elem in RecipeResultList]
    counter=0
    usersingredientfrequency =""
    while counter<len(RecipeResultList):
        recipeid = str(RecipeResultList[counter][0])
        counter2=0
        while counter2<len(CleanedandSortedRecipeIDList):
            if str(CleanedandSortedRecipeIDList[counter2][0])==recipeid:
                usersingredientfrequency = CleanedandSortedRecipeIDList[counter2][1]
                break
            counter2=counter2+1
        RecipeResultList[counter].insert(1,usersingredientfrequency)
        counter = counter+1
    RecipeResultList=sorted(RecipeResultList,key=lambda x: (x[1],x[7],-x[3]), reverse=True)
    runtime = round(time.time() - start_time, 2)
    print ("Inserting Users ingredient frequency into recipe results and sorting took ", runtime," seconds to run")
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
          Ingredient_Matches: str
          Title: str
          Ingredient_Count: str
          Ingredients: str
          Servings: str
          Method: str
          Picture_URL: str


     db_tuple_with_recipe_results = FindRecipesByIngredientMatches(user_ingredient_list, maximum_ingredients_for_recipes)
     recipes = [Recipe(ID=ID, Ingredient_Matches=Ingredient_Matches, Title=Title, Ingredient_Count=Ingredient_Count, Ingredients=Ingredients, Servings=Servings, Method=Method, Picture_URL=Picture_URL) 
     for ID, Ingredient_Matches, Title, Ingredient_Count,Ingredients,Servings, Method, Picture_URL in db_tuple_with_recipe_results]
     return {"Recipes": recipes}




    






    


            






