RecipeWizard helps you use up leftover ingredients in your fridge/cupboards by searching through thousands of recipes based on the ingredients you enter. I created it as a project to learn more about several tools and programming languages inclusing Python, TDD, JMeter, JavaScript, HTML, CSS and React.

There are two components ;

1.) An API written with Python & FastAPI as an interface to a MySQL database (live example/documentation here; http://80.195.31.145:8000/docs) 

2.) A web based UI created with React/JavaScript/HTML/CSS that connects to the API (live example here ; http://80.195.31.145/)

The examples above are both currently running on a Raspberry Pi 4. This API has been load tested with this setup and is performant with 10 concurrent users creating load at a reasonable speed. The API was created using a TDD approach with PyTest.
