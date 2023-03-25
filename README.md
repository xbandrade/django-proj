# Django Recipes

🗒️ [README pt-BR](https://github.com/xbandrade/django-recipes/blob/main/README-pt-BR.md)

➡️ Deploy: https://recipes-django.onrender.com

➡️ A recipe website built with Django and Django REST frameworks.

❕Home Page
- The home page displays the most recent published recipes.
- The search bar can be used to find specific food categories, recipe names or tags. 
- Click on `See More...` to see details about a specific recipe.

❕Dashboard
- When you are logged in, you can create new recipes and send a request for an admin to publish it. 
- While it's unpublished, you can edit the recipe details from the user's dashboard.

❕REST API v1
- This API lets you retrieve data for all the recipes on the home page using the URL `/recipes/api/v1`.
- Details about a recipe can be accessed using its id with the URL `/recipes/api/v1/<int:id>`.
  
❕REST API v2
- This API allows you to retrieve data for a specific recipe tag using the URL `/recipes/api/v2/tag/<int:id>`.
- You can use JWT Authentication to log in to API v2 by creating and verifying a token at the URL `/recipes/api/token`.
- Once authenticated, you can use the URL `/recipes/api/v2` to create, read, update, and delete recipes using the appropriate HTTP method.

➡️ Functional tests using `Selenium` are located in the `/tests` directory, and Django unit tests are stored within the `/tests` directory of each individual app folder.
