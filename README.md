# Final Year Project ![GitHub language count](https://img.shields.io/github/languages/count/anshulhedau10/fyp?color=green)

## Title: Predicting high risk COVID-19 patients.
- Made by `Ganesh K. Yenurkar`, `Anshul Hedau`, `Prajwal Hatwar`, `Shreyas Rajurkar`, `Juli Khobragade`.

- The objective of this project is to predict if a COVID-19 patient will have a high risk of death in near future.
- Two machine learning models were used i.e., Random Forest Classifier and XG Boost which takes initial health parameters of the patient as input and gives a boolean result whether patient is at high risk or not.
- The project is a web app built using python flask and gunicorn.

## Screenshots

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot1.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot2.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot3.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot4.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot5.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot6.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot7.jpg?raw=true)

![alt text](https://github.com/anshulhedau10/fyp/blob/main/static/images/Screenshot8.jpg?raw=true)

# How to run this app on your local machine:
**Prerequisites:**
- Python >=3.9.6
- Git >=2.33.1.windows.1

1. **PROJECT SETUP**  
    If you don’t have this project.
    - Go to the desired location where you want to save the project.
    ```
    cd <your_desired_path>
    ```
    - Clone the project from the repo.
    ```
    git clone https://www.github.com/anshulhedau10/fyp
    cd fyp/
    ```

    If you have this project already.
    - Go to the project’s location.
    ```
    cd <your_project’s_path>
    ```
    - Pull the project from the repo.
    ```
    git pull origin
    ```

2. **PYTHON VIRTUAL ENVIRONMENT SETUP**  
    - Create a python virtual environment.
    ```
    python -m venv venv
    ```
    - Activate the virtual environment.
    ```
    source venv/scripts/activate
    ```

    You need to activate the virtual environment every time you wish to run the app.

3. **INSTALL DEPENDENCIES**  
    ```
    pip install -r requirements.txt
    ```

4. **RUN THE APP**  
    Run this command to run the app.
    ```
    python app.py
    ```

