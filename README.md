# Streaming-Database
Database retrieval application for a hypothetical streaming service.

# How To Run This Project On Your Machine (For VSCode + Windows)
1. Clone the repository. 
2. Make sure you downloaded Python. 
3. Enable/Download the Python extension. 

## Virtual Environment Setup
1. Create a virtual environment by running `python -m venv venv` (if this doesn't work, try with `python3` or `py` instead). If VSCode registers your virtual environment correctly, it will prompt you to 'use this virtual environment' and you are all set. 
2. If the prompt does not pop up, hit CTRL+Shift+P to open the VSCode Palette. Search for 'Python: Select Interpreter'. Choose 'Enter Interpreter Path'. Go to this project's directory, go to the venv directory, choose python.exe. 
3. Open a new terminal, and you should see a `(venv)` in green before your directory path. 

## Database Setup
1. Get the creds.json file from Google Drive. 
2. Get the env file from Google Drive. 
3. Add the creds.json file to this project directory. 
4. Run `$env:GOOGLE_APPLICATION_CREDENTIALS='creds.json'` so that it knows where to pull the Google credentials for Google Cloud. 
      - (For Mac users) Run `export VAR_NAME=value` instead. `$env` only works on Windows. 
5. Run all commands from env file. 
6. Get access from Kay to the Google Cloud terminal so you can view the database from your Google Cloud console. 

## Dependencies Setup
1. Run `pip install -r requirements.txt` to get all dependencies. 

## Sanity Check
1. If you've done everything until now with no errors, you should be able to run the server. 
2. On the terminal, run `python manage.py runserver`. It should have a link for you (localhost). 
3. The current path 'http:localhost:/' is an error, and it is fine. Once we settle who's doing what, we will migrate the welcome page to path '/'.
4. Change the path to 'http:localhost:/welcome' and you should see 5 rows of 'media'.
5. Change the path to 'http:localhost:/welcome/submit' and you should see a line with a button. 

# Current Project Information
1. The connection between Cloud MySQL and the project is in `welcome/__init__.py`.
2. The connection object (the engine) is in `welcome/db.py`. This object will be used for all future query requests from the database. 
3. `template` folders are for html files. 
4. `static` folders are for css files. 
5. Currently everything is in welcome directory. We might want to separate ourselves into 4 smaller directories, or we can all do it in one directory. 
6. There are a couple of mini examples I set up (which we will delete them once we get the hang of it), which retrieves all media, and inserts a constant media object. They are in the welcome directory. 

# Backend
## File description:
- `urls.py`: Holds all the major paths. Root starts with `/`.

- `welcome/views.py`: "view" functions of each url. Determines the response for each request from the user. Currently holds function to communicate with the database. We might want to separate the db query logic out into its own file, and this file only holds logic for 'GET', 'POST', 'DELETE' requests. 

- `welcome/urls.py`: Holds all the sub-paths with the root path 'welcome'.

- `welcome/models.py`: Holds all the models (the "table schema" to make quering easier). We should have a Model blueprint for every table we have. 

- `welcome/db.py`: The engine class object. We will use this object for all query requests. 

- `welcome/__init__.py`: Holds the connection between the project and the Cloud MySQL. 

- `welcome/templates`: Holds all HTML files. These HTML files are referenced in `view.py` in the `render()` function. (Each major component should have their own sub-directory, like how welcome has its own.)

- `welcome/static`: Holds all CSS files. These CSS files are referenced in HTML files. (Each major component should have their own sub-directory, like how welcome has its own.)
## SQL
Our main package used is `mysqlalchemy`. We can use raw SQL, ORM, prepared statements with this package. Not sure how stored procedures work yet. 
Reference: https://docs.sqlalchemy.org/en/14/orm/queryguide.html

# Frontend
## Styling
We will use Bootstrap for styling because all we need is just a link. If Samara has any other ideas then we can use it. We can also add CSS files for customized styling. 
Reference: https://getbootstrap.com/docs/4.5/components/alerts/

# Housekeeping
- Github branches
      -- To manage future merge conflicts and avoid crashing the main code, we should all work on our own branch. Do a `git pull origin main` before you code every time you work on the project to avoid any future merge conflicts. You can run the `git add`, `git commit` and `git push` as usual in your branch, and after that, on the Github website, open a pull request and merge it. This way helps keeping track of code history. 

- Python-self generated files
      -- Often times when we run Python, it will generate random files in our directory that keeps our code working but we have no idea what they does and 90% of the time they are machine-dependent. We don't want those files to create chaos, so before running `git add`, add those files (or directory) to the `.gitignore` file so that Git will not track them. (a good example is the `venv` folder)
      
- Packages
      -- If you are using new packages, add them to the `requirements.txt` file so that others who pulled your code, can just run `pip install -r requirements.txt` and get them.

