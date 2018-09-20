# Flask MVC MongoDB: Implementation Example

This application is an example of implementing the flask framework with the MVC project pattern and MongoDB database. The idea behind this project is to serve as a base model, including most of the major components of a web application, such as:

* MVC pattern
* MongoDB as Database
* Login
* Route with access level 
* User CRUD
* FlaskForm with MongoDB unique email verification
* Breadcrumb
* Minimal Seo
* Flask Assets
* Forgot password Page with Flask Mail

## Project Structure

Based on the MVC design pattern, the following hierarchy of folders was used:

```
 config.py
 index.py
▾ app/
    __init__.py
    ▾ controllers/
        users.py
        __init__.py
    ▾ forms/
        user.py
    ▾ models/
        base.py
        user.py
    ▾ static/
        ▾ css/
        ▾ fonts/
        ▾ gen/
        ▾ imgs/
        ▾ js/
    ▾ templates/
        error.html
        login.html
        layout.html
        ▾ includes/
            messages.html
            seo.html
        ▾ users/
            add.html
            change_password.html
            home.html
            index.html

```

## Getting Started

Initially I recommend you use 'conda' and create a new environment for this project using python 3.6.

### Prerequisites

To install all of the python libraries that were used in this project, run:

```
 pip install -r requirements.txt
```

### Config.py

This file is where we find the main settings of the project, such as:

* Application settings (Name, Description, Author, ...)
* DEBUG status
* MongoDb settings 
* Secret key
* Mail settings
* Access Levels

### To run:

```
 python index.py run
```

## Authors

* [**Tiago Franco**](https://github.com/tiagofranco21)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

