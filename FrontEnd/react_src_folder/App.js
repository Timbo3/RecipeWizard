import React, {useEffect, useState} from "react";
import Recipe from './Results';
import 'bootstrap/dist/css/bootstrap.min.css'
import {Form} from 'react-bootstrap'
import style from './style.module.css';
import Select, { createFilter, } from 'react-select';


function App() {

  const [valid_ingredient_list, setIngredients] = useState([]);
  let ingredients_query_string_for_api = '';
  let users_maximum_ingredients = 12;
  let [users_selected_ingredients_array, updateUsersSelectedIngredients] = useState([]);
  const [recipe_results_from_api, setRecipes] = useState([]);


  useEffect(() => {
    getvalidingredientapiresponse();
  }, []);

  const getvalidingredientapiresponse = async () => {
    var apiresponse = await fetch(`http://192.168.0.24:8000/valid_ingredient_list/`)
    const validingredientapiresponse = await apiresponse.json();
    setIngredients(validingredientapiresponse.Ingredients);
  }

  useEffect(() => {
    if (users_selected_ingredients_array != 0) {
      ingredients_query_string_for_api = (users_selected_ingredients_array.map(e => e.value).join(','))
      getrecipeapiresponse();
    }
  }, [users_selected_ingredients_array]);


  var options = valid_ingredient_list.map(option => ({value: option,label: option}));

  const updateUsersMaximumIngredientsSetting = e => {
    if (users_selected_ingredients_array != 0) {
      users_maximum_ingredients = (e.target.value); 
      ingredients_query_string_for_api = (users_selected_ingredients_array.map(e => e.value).join(','))
      getrecipeapiresponse(); 
    }
  }

  const getrecipeapiresponse = async () => {
    var url = 'http://192.168.0.24:8000/search_recipes_by_ingredients/'+ingredients_query_string_for_api+"/"+users_maximum_ingredients
    console.log('Attempting to get API response using URL '+url)
    var apiresponse = await fetch(url)
    const data = await apiresponse.json();
    setRecipes(data.Recipes);  
  }

  return (              
  <div className = "App">
    <section className = {style.Top_Bar}> 
        <div >
          <h1 className={style.logo_text}>Recipe<span className={style.wizard_logo_text}>Wizard</span ></h1>
        </div>
        <div className={style.help_text}>
          Search through thousands of recipes using ingredient combinations. Get recipe ideas, use up leftover ingredients. 
        </div>
        <Form className = "search-form">  
          <Select 
          options={options} 
          filterOption={createFilter({ignoreAccents: false})}
          isMulti className = {style.IngredientsSelector}    
          onChange ={updateUsersSelectedIngredients} 
          autoFocus={true}
          placeholder={<div>Start typing some ingredient names</div>}  
          /> 
          <div className={style.MaxIngredientsSelectorContainer}>
            <label htmlFor="maximum_ingredients" className={style.help_text}>Recipe Complexity</label>
            <input 
            id="maximum_ingredients"
            type="range" 
            className = {style.MaxIngredientsSelector} 
            defaultValue={15}
            min="1" max="100"
            onChange ={updateUsersMaximumIngredientsSetting}>
            </input>
          </div>
        </Form>
    </section>
    
    <section className = {style.Recipes_Area}> 
      {recipe_results_from_api.map(recipe => (<Recipe 
      key = {recipe['ID']} 
      title = {recipe['Title']} 
      ingredients = {recipe['Ingredients']} 
      url = {recipe['URL']} 
      image = {recipe['Picture_URL']} />))}
    </section>
  </div>
  );
        
}

export default App;
