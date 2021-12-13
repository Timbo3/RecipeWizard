from typing import List, TypeVar
import mysql.connector
from database_connnection_details import config
from collections import Counter
import time

def GetValidIngredientList():

    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    start_time = time.time()
    sqlquery = "select name from ingredient"
    cursor.execute(sqlquery)        
    ListOfValidIngredientNames = cursor.fetchall()
    print ("Getting list of all different ingredients from database took ", time.time() - start_time," seconds to run")
    return (ListOfValidIngredientNames)