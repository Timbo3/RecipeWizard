from typing import List, TypeVar
import mysql.connector
from collections import Counter
import time
from database_connnection_details import config



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
    if CleanedandSortedRecipeIDListLength>100:
        print ("Shortening List to 100 items..")
        CleanedandSortedRecipeIDList= CleanedandSortedRecipeIDList[0:100]       
    print ("Length of recipe id list is ",len(CleanedandSortedRecipeIDList))
    print ("Sorting recipe id list, removing duplicates, limiting to 100 id's the took ", time.time() - start_time," seconds to run")

    start_time = time.time()
    CleanedandSortedRecipeIDList= ','.join(CleanedandSortedRecipeIDList)
    sqlquery = "select id,name,ingredient_list,source_url,picture_url from recipe where id IN ("+CleanedandSortedRecipeIDList+") AND (recipe.different_ingredients <="+MaximumIngredientsInRecipes+")"
    CleanedandSortedRecipeIDListWithoutSpeechMarks = CleanedandSortedRecipeIDList.replace("'","")
    sqlquery = sqlquery + " ORDER BY FIND_IN_SET(id,'"+CleanedandSortedRecipeIDListWithoutSpeechMarks+"'), popularity DESC"
    print ("Querying database recipe table for recipes..")
    # print ("SQL Query is ", sqlquery)
    cursor = db.cursor()
    cursor.execute(sqlquery)        
    print ("Loading results from database into list.")
    RecipeResultList = cursor.fetchall()
    print ("Querying the database with the recipe id list took ", time.time() - start_time," seconds to run")
    cursor.close()
    # print (RecipeResultList)
    return (RecipeResultList)