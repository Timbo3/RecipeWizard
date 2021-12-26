import {Given, Then, When} from "cypress-cucumber-preprocessor/steps";

Given("I navigate to the home page", ()=> {
    cy.visit("/");
});

When("the home page has loaded", () => {
    cy.get(".search-form").should("be.visible");
});

Then("I see the home page", () => {
    cy.get(".style_logo_text__389O4").should("be.visible");
});