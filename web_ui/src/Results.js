import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import {Card,Button} from 'react-bootstrap'
import style from './style.module.css';

const Recipe = ({title,ingredients,url,image}) => {

    return(

        <Card className={style.recipe}>          
            <Card.Img className={style.recipe_picture} src={image}/>
            <Card.Body>
                <Card.Title>{title}</Card.Title>
                <Card.Text><b>Ingredients: </b><i>{ingredients}</i></Card.Text>
            </Card.Body> 
            <a href ={url} target="_blank" rel="noreferrer"> <Button className={style.view_recipe_button}>View Recipe</Button></a>          
        </Card>

    );


}

export default Recipe;
