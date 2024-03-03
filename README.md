> *This is my implementation of a django-based to-do list, allowing you to add/remove/update different lists each containing some tasks in them.*

### STEPS TO USE THIS APP
1. #### Open a terminal window in the root directory
2. #### Enter the code below to create a python virtual environment :
    ```
    python -m venv venv
    ```
3. ####  Activate the environment with the command below :
    ```
    source venv/bin/activate
    ```
4. #### Install the required packages
    ```
    pip install -r requirements.txt
    ```
5. #### Run the server using the proper manage.py command :
    ```
    python manage.py runserver
    ```
6. #### You can now interact with the project through
    > *http://127.0.0.1:8000/todolist*

To run the project in a production environment, use the command below:
```djangourlpath
 python manage.py runserver --settings=TickApp.settings.production
```


