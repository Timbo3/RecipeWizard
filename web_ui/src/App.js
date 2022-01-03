import React, {useEffect, useState} from "react";
import {Card,Button,Form} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import style from './style.module.css';
import Select, { createFilter, } from 'react-select';


function App() {

  const [valid_ingredient_list, setIngredients] = useState([]);
  let ingredients_query_string_for_api = '';
  let [users_selected_ingredients_array, updateUsersSelectedIngredients] = useState([]);
  const [recipe_results_from_api, setRecipes] = useState([]);
  let users_maximum_ingredients =15

  useEffect(() => {getvalidingredientapiresponse();}, []);
  const getvalidingredientapiresponse = async () => {
    var apiresponse = await fetch(`http://192.168.0.18:8000/valid_ingredient_list/`)
    const validingredientapiresponse = await apiresponse.json();
    setIngredients(validingredientapiresponse.Ingredients);
  }
  var options = valid_ingredient_list.map(option => ({value: option,label: option}));

  useEffect(() => {
    if (users_selected_ingredients_array != 0) {
      ingredients_query_string_for_api = (users_selected_ingredients_array.map(e => e.value).join(','))
      getrecipeapiresponse();
    }
  }, [users_selected_ingredients_array]);

  const updateUsersMaximumIngredientsSetting = e => {
    if (users_selected_ingredients_array != 0) {
      users_maximum_ingredients = e.target.value
      console.log('max ingredients set to '+users_maximum_ingredients)
      ingredients_query_string_for_api = (users_selected_ingredients_array.map(e => e.value).join(','))
      getrecipeapiresponse(); 
    }
  }

  const getrecipeapiresponse = async () => {
    var url = 'http://192.168.0.18:8000/search_recipes_by_ingredients/'+ingredients_query_string_for_api+"/"+users_maximum_ingredients
    var apiresponse = await fetch(url)
    const data = await apiresponse.json();
    setRecipes(data.Recipes);  
  }

  const ShowRecipePopup = e => {
    var modal = document.getElementById("recipePopupForRecipeID"+e.target.id);   
    modal.style.display = "block"; 
  }

  const CloseRecipePopup = e => {
    var modal = document.getElementById("recipePopupForRecipeID"+e.target.id);
    modal.style.display = "none";
  }


  const Recipe_result = ({recipeID,title,ingredients,servings,method,image}) => {

    let ingredientsForPopup = ingredients.replace(/<ingredient>/g, '<li>')
    ingredientsForPopup = ingredientsForPopup.replace(/<\/ingredient>/g, '</li>')
    ingredients = ingredients.replace(/<ingredient>/g, '')
    ingredients = ingredients.replace(/<\/ingredient>/g, '. ')

    method = method.replace(/step/g, '')
    for (var i = 0; i < 20; i++) {
      var regexfindvalue = new RegExp("<[" + i + "]>", "g")
      var regexreplacevalue = "<p><b>"+i+". </b>" 
      method = method.replace(regexfindvalue, regexreplacevalue)
      regexfindvalue = new RegExp("<\/[" + i + "]>", "g")
      regexreplacevalue = "</p>" 
      method = method.replace(regexfindvalue, regexreplacevalue)
    }

    return(

        <Card className={style.recipe} >                 
            <Card.Body>
                <Card.Title >{title}</Card.Title>
                <Card.Img className={style.recipe_picture} src={image}/>
                <Card.Text><b>Ingredients: </b>({servings}) <i>{ingredients.replace(/<li>/g, '')}</i></Card.Text>
                <Button  id={recipeID} onClick={ShowRecipePopup}>View Recipe</Button>
            </Card.Body> 

            <div id={"recipePopupForRecipeID"+recipeID} className={style.modal}>
              <div className={style.modalcontent}>
              <span id={recipeID} className={style.close} onClick={CloseRecipePopup}>&times;</span>
             <p className={style.recipe_popup_title}><b>{title}</b></p>
             <img className={style.recipe_picture} src={image}/>
            
             <p><b>Ingredients </b>({servings})</p>
             <div dangerouslySetInnerHTML={{ __html: ingredientsForPopup }}></div><p>&nbsp;</p>
             <p><b>Method: </b></p>
             {/* <div>{method}</div> */}
             <div dangerouslySetInnerHTML={{ __html: method }}></div>
             </div>
             </div>

        </Card>

    )
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
            <label htmlFor="maximum_ingredients" className={style.help_text}>Recipe Complexity:</label>
            <input 
            id="maximum_ingredients"
            type="range" 
            className = {style.MaxIngredientsSelector} 
            defaultValue={15}
            min="1" max="25"
            onChange ={updateUsersMaximumIngredientsSetting}>
            </input>
          </div>
        </Form>
    </section>
    
    <section className = {style.Recipes_Area}> 
      {recipe_results_from_api.map((recipe,index) => (<Recipe_result
      key = {recipe['ID']} 
      recipeID= {recipe['ID']} 
      title = {recipe['Title']} 
      string ingredients = {recipe['Ingredients']}
      servings = {recipe['Servings']} 
      method = {recipe['Method']} 
      image = {recipe['Picture_URL']} />))}
    </section>
  </div>
  );
          
}

export default App;
