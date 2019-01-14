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


## Skills used for ths project

* Python 
* HTML
* CSS
* Bootstrap
* Flask Framework
* SQLAlchemy
* Oauth


## Dependencies

* [Vagrant](https://www.vagrantup.com/docs/virtualbox/)
* [VirtualBox](https://www.virtualbox.org)
* [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)

## Getting Started

 * Install Vagrant in VirtualBox
 * Clone the VagrantFile from Udacity Repo
 * Clone this repo into the ```catalog/``` directory in the Vagrantfile
 * Run ```vagrant up``` to get the machine running then run ```vagrant ssh``` to login to your virtual machine
 * pre populate the database by running ```python category.py```
 * Then run the application with ```python catalog.py``` command
 * goto http://localhost:5000/ to access the app
 
 
 ## JSON Endpoints
 
 All API endpoints are currently available to the public. Please reference back here for any changes.
 
 * api/v1/categories/JSON: returns a list of all the categories 
 * api/v1/categories/<int:category_id>/JSON: returns the information on the selected category
 * api/v1/categories/classes/JSON : returns a list of all the classes in the category
 
 
 ### Thank you for checking out this project!
 
  
 
 
 
 