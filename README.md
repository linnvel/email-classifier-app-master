# Email Classification Web Application

### Quick start
To run the web application:

```bash
docker-compose up --build
```

Visit [http://0.0.0.0:5000/](http://0.0.0.0:5000/) in your browser.

To run unit tests:

```bash
cd flask/app/unittest
python test.py
```

Note that the successful email upload test need to use different files for each run; otherwise, the file will be duplicated. Alternatively, you can delete the file manually from the `dashboard` page in the website before testing.

The test user account is:

* username: `sherry`
* password: `123456`

The password of MySQL database is `1234`.

The Machine Learning model used in this project is SVM+TF-IDF. The model file is stored in `flask /app/static/model`. I also attach the python code of model training. If you want to train the model by yourself, make sure that you intall `termcolor` and `colorama` packages and run the following commands.

```base
cd flask
python train_ml.py
```
Also you need to specify your data path while running the code. More information about the data and models can be found in [this project](https://github.com/linnvel/text-classifier-master).
