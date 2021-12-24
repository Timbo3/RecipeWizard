
import mysql.connector
from itertools import chain
from database_connnection_details import config

db = mysql.connector.connect(**config)
cursor = db.cursor()

counter=13657
while counter<57027:
    recipe_id = str(counter)
    cursor.execute("select name from ingredient where recipe_ids like '%,"+recipe_id+",%'")        
    ingredient_list = cursor.fetchall()
    ingredient_list = ','.join(map(str,chain.from_iterable(ingredient_list)))
    recipe_table_update_sql = "update recipe set ingredient_list='"+ingredient_list+"' where id="+recipe_id+""
    cursor.execute(recipe_table_update_sql)
    db.commit()
    counter+=1
cursor.close()
print (recipe_id)