# Empire Penguin

## Badges
![Website](https://img.shields.io/website?down_color=red&down_message=offline&up_color=blue&up_message=online&url=https%3A%2F%2FPenguinempire.pythonanywhere.com)

![GitHub last commit](https://img.shields.io/github/last-commit/Bhavik-Gilbert/Empire-Penguin)
![GitHub contributors](https://img.shields.io/github/contributors/Bhavik-Gilbert/Empire-Penguin)

![Lines of code](https://img.shields.io/tokei/lines/github/Bhavik-Gilbert/Empire-Penguin)
![GitHub repo size](https://img.shields.io/github/repo-size/Bhavik-Gilbert/Empire-Penguin)
![GitHub top language](https://img.shields.io/github/languages/top/Bhavik-Gilbert/Empire-Penguin)
![GitHub language count](https://img.shields.io/github/languages/count/Bhavik-Gilbert/Empire-Penguin)

## About
Social media application where users can post text and images while having fun interactions with virtual penguins throughout the site.

## Project structure
The project is called `clucker`.  It currently consists of a single app `microblogs` where all functionality resides.

## Deployed application
The deployed version of the application can be found at: https://PenguinEmpire.pythonanywhere.com

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

 
