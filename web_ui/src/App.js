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


  const customStyles = {
    option: (provided, state) => ({
      padding: 6,
      borderBottom: '1px dotted grey',
    }),
    control: () => ({
      padding:5,
      border: '1px solid grey',
      minHeight:100
    }),
    singleValue: (provided, state) => {

    }
  }


  const Recipe_result = ({recipeID,ingredientMatches,title,ingredientCount,ingredients,servings,method,image}) => {

    let ingredientsForPopup = ingredients.replace(/<ingredient>/g, '<li>')
    ingredientsForPopup = ingredientsForPopup.replace(/<\/ingredient>/g, '</li>')
    ingredients = ingredients.replace(/<ingredient>/g, '')
    ingredients = ingredients.replace(/<\/ingredient>/g, '. ')

    method = method.replace(/step/g, '')
    for (var i = 0; i < 30; i++) { 
       method = method.replace("<"+i+">", "<p><b>"+i+". </b>")
       method = method.replace("<\/"+i+">", "</p>")
     }


    return(

        <Card className={style.recipe} >                 
            <Card.Body>
                <Card.Title >{title} ({ingredientMatches}/{ingredientCount})</Card.Title>
                <Card.Img className={style.recipe_picture} src={image}  />
                <Card.Text><b>Ingredients: </b>({servings}) <i>{ingredients.replace(/<li>/g, '')}</i></Card.Text>
                <Button  id={recipeID} onClick={ShowRecipePopup}>View Recipe</Button>
            </Card.Body> 

            <div id={"recipePopupForRecipeID"+recipeID} className={style.modal}>
              <div className={style.modalcontent}>
              <span id={recipeID} className={style.close} onClick={CloseRecipePopup}>&times;</span>
             <p className={style.recipe_popup_title}><b>{title}</b></p>
             <img className={style.recipe_picture} src={image} onError={(event) => event.target.style.display = 'none'}/>
            
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
        <div className={style.help_text} id={"helptext"}  >
          Search through thousands of recipes using ingredient combinations. Use up leftover ingredients and get recipe ideas.
        </div>
        <Form  className = "search-form"  >  

        <Select           
          options={options} 
          filterOption={createFilter({ignoreAccents: false})}
          components={{ DropdownIndicator:() => null, IndicatorSeparator:() => null }}
          isMulti className = {style.IngredientsSelector} 
          onChange ={updateUsersSelectedIngredients} 
          isClearable={false}
          styles={customStyles}
          autoFocus={true}
          placeholder={<div className={style.select_placeholder}>Start typing some ingredient names</div>}  
          />

          <div className={style.MaxIngredientsSelectorContainer}>
            <label htmlFor="maximum_ingredients" className={style.recipe_complexity_text}>Recipe Complexity:</label>
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
      ingredientMatches= {recipe['Ingredient_Matches']} 
      title = {recipe['Title']} 
      ingredientCount = {recipe['Ingredient_Count']}
      string ingredients = {recipe['Ingredients']}
      servings = {recipe['Servings']} 
      method = {recipe['Method']} 
      image = {recipe['Picture_URL']} />))}
    </section>
  </div>
  );
          
}

export default App;
