# Catalog Project

This catalog project consist of classes at a fitness facility. Within each class(the category), There will be a list of
class names(items) which will display a description of the class chosen.

## How the project is designed

1. The **home page**  shows a list of all of the class types as well as the latest classes added to their assigned
class category.

2. Each **class**(category) will have a link that directs to a list of all of the classes in the category

3. Each **class**(item) will have a link to the description of the the class chosen

4. If a user **is authenticated** and logged in, then they will be able to do CRUD(Create, Read, Update, and Delete) operations
to the class Categories as well as the class items

5. There will also be **API endpoints** for each of the categories and class items