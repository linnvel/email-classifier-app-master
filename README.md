# Email Classification Web Application

## Introduction

This project is a practice of web application through Python Flask framework and MySQL database. Both web server-side code and front-end UI code are implemented, as well as a few examples of server-side unit tests.

The function of the web includes:

1. User sign up, sign in, log out. Note that username is unique.
2. View user profile and change username/password.
3. Upload email file for prediction.
4. Run the classification model and return result to be displayed on the web interface.
5. Recover username/password through the user’s registered email.
6. Automatically sign out the user once the login session is timed out.

## Quick start
To run the web application:

```bash
docker-compose up --build
```

Visit [http://0.0.0.0:5000/](http://0.0.0.0:5000/) in your browser.

After the web is running, you can run unit tests by:

```bash
cd flask/app/unittest
python test.py
```

Note that the successful email upload test need to use different files for each run; otherwise, the file will be duplicated. Alternatively, you can delete the file manually from the `dashboard` page in the website before testing.

The Machine Learning model used in this project is SVM+TF-IDF. The model file is stored in `flask /app/static/model`. I also attach the python code of model training. If you want to train the model by yourself, make sure that you intall `termcolor` and `colorama` packages and run the following commands.

```base
cd flask
python train_ml.py
```
Also you need to specify your data path while running the code. More information about the data and models can be found in [this project](https://github.com/linnvel/text-classifier-master).
