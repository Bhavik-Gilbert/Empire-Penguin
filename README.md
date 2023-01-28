# Empire Penguin

## Badges
![GitHub last commit](https://img.shields.io/github/last-commit/Bhavik-Gilbert/Empire-Penguin)
![GitHub contributors](https://img.shields.io/github/contributors/Bhavik-Gilbert/Empire-Penguin)
![Lines of code](https://img.shields.io/tokei/lines/github/Bhavik-Gilbert/Empire-Penguin)
![GitHub repo size](https://img.shields.io/github/repo-size/Bhavik-Gilbert/Empire-Penguin)    

![GitHub top language](https://img.shields.io/github/languages/top/Bhavik-Gilbert/Empire-Penguin)
![GitHub language count](https://img.shields.io/github/languages/count/Bhavik-Gilbert/Empire-Penguin)

## About
This project aims to produce an application that allows users to track their expenditures. The expenditure can belong to different categories. The user should be able to create, edit and delete these categories. When adding new spending, there should be a functionality to add a title, a short description, and an optional photo or file for the receipt. Moreover, the user should be able to set spending limits for each category as well as for the overall spending in a selected timeframe. When approaching and exceeding the set limits, the user should get a warning from the system. The app should motivate the user to stick to the set goals through gamification. Lastly, the user should be able to get reports and charts for their spending in a given timeframe.

## Project structure
The project is called `clucker`.  It currently consists of a single app `microblogs` where all functionality resides.

## Deployed application
This application has yet to be deployed

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Run all tests with:
```
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`

 
