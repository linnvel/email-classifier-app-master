from app import app, mysql, mail
import sys
from functools import wraps
from flask import render_template, flash, redirect, url_for, request, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, HiddenField, SubmitField
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
import pipeline
import pickle

# default model parameters
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
"it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
"should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
"hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
"mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
"wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]\
+ ['would','could','may','also', 'one', 'two', 'three','first', 'second' ,'third',
'someone', 'anyone', 'something', 'anything','subject', 'organization', 'lines',
'article', 'writes', 'wrote']

tokenize_regex1 = r"\w+|\$[\d\.]+"
tokenize_regex2 = r"[a-zA-Z_]+"

category = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
     'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
     'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
     'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
     'sci.space', 'soc.religion.christian', 'talk.politics.guns',
     'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']


# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')


# Register Form Class
class RegisterForm(Form):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.DataRequired()
    ])
    email = StringField('Email', [validators.Length(min=6, max=100)])
    first_name = StringField('First Name', [validators.Length(min=1, max=30)])
    mid_name = StringField('Middle Name (Optional)', [
        validators.optional(), validators.Length(min=1, max=30)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=30)])
    address = StringField('Mailing Address (Optional)', [
        validators.optional(), validators.length(max=100)])
    phone = StringField('Phone Numbers (Optional)',[
        validators.optional(), validators.length(max=30)])
    occupation = StringField('Occupation (Optional)',[
        validators.optional(), validators.length(max=30)])
    password = PasswordField('Password', [
        validators.DataRequired(),validators.Length(min=1),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        mid_name = form.mid_name.data
        last_name = form.last_name.data
        address = form.address.data
        phone = form.phone.data
        occupation = form.occupation.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Check username duplicate
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        # username exists
        if result >0:
            flash('The username is taken. Try another.','danger')
            cur.close()
            return render_template('register.html', form=form)

        # username doesn't exist
        else:
            cur.execute("INSERT INTO users(username, email, first_name, mid_name, last_name, phone, mail_address, occupation, pass_word) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (username, email, first_name, mid_name, last_name, phone, address, occupation, password))

            # Commit to DB
            mysql.connection.commit()

            flash('You are now registered and can log in', 'success')

            # Close connection
            cur.close()

            return redirect(url_for('index'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
    #     Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['pass_word']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['userid'] = data['id']
                session['permanent'] = True
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get emails
    # Show emails only uploaded by the user logged in
    result = cur.execute("SELECT * FROM emails WHERE upload_by = %s", [session['userid']])

    emails = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', emails=emails)
    else:
        msg = 'No Emails Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

    return render_template('dashboard.html', emails=emails)

# User Profile
@app.route('/user_profile/<string:username>/')
@is_logged_in
def user_profile(username):
    if session['username']!=username:
        username = session['username']
        #return redirect(url_for("user_profile",name=username))
    # Create cursor
    cur = mysql.connection.cursor()

    # Get user info
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

    data = cur.fetchone()
    cur.close()

    if result > 0:
        return render_template('userprofile.html', profile=data)
    else:
        msg = 'No Profiles Found'
        return render_template('userprofile.html', msg=msg)


# Change username
@app.route('/changeusername', methods=['GET', 'POST'])
@is_logged_in
def change_username():
    if request.method == 'POST':
    #     Get Form Fields
        username_new = request.form['username']
        if len(username_new)<4 or len(username_new)>25:
            error = 'Length of username should be between 4 and 25'
            return render_template('changeusername.html', error=error)

        if username_new == session['username']:
            error = 'Set a different username or return'
            return render_template('changeusername.html', error=error)

        # Create cursor
        cur = mysql.connection.cursor()

        # Check if the new username exists
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username_new])

        # username exists
        if result >0:
            error = 'The username is taken. Try another.'
            cur.close()
            return render_template('changeusername.html', error = error)

        # username doesn't exist
        else:
            cur.execute("UPDATE users SET username = %s WHERE username = %s",
                [username_new, session['username']])
            session['username'] = username_new

            # Commit to DB
            mysql.connection.commit()

            flash('Username changed successfully', 'success')

            # Close connection
            cur.close()

            return render_template('changeusername.html')
    return render_template('changeusername.html')


# Change Password Form Class
class ChangePasswordForm(Form):
    password_old = PasswordField('Current Password',
                                 validators=[validators.DataRequired()])
    password_new = PasswordField('New Password', validators=[
        validators.DataRequired(), validators.Length(min=1)])
    password_confirm = PasswordField('Repeat New Password',validators=[
        validators.DataRequired(),
        validators.EqualTo('password_new', message='Passwords do not match')
        ])

# Change Password
@app.route('/changepassword', methods=['GET', 'POST'])
@is_logged_in
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        password_old = form.password_old.data
        password_new = sha256_crypt.encrypt(str(form.password_new.data))

        # Check if new password is the same with current one
        if sha256_crypt.verify(password_old, password_new):
            flash('Current password and new password must be different', 'danger')
            return render_template('changepassword.html', form=form)

        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [session['username']])

        if result>0:
            # Get stored data
            data = cur.fetchone()
            password = data['pass_word']

            # Compare password
            if sha256_crypt.verify(password_old, password):
                result = cur.execute("update users set pass_word=%s where username=%s",
                                    (password_new, session['username']))
                mysql.connection.commit()

                session.clear()
                flash('Password has been changed. Please login again.', 'success')
                cur.close()
                return redirect(url_for('login'))
            else:
                flash('Current password is wrong', 'danger')
        else:
            print("error: more than one username")
        cur.close()
        return render_template('changepassword.html', form=form)
    return render_template('changepassword.html', form=form)


# Add Email File
@app.route('/addemail',methods=['POST','GET'])
@is_logged_in
def add_email():
    if request.method == 'POST':
        f = request.files['file']

        # check if user does not select file
        if f.filename =='':
            flash("Choose a file from you folder", 'danger')
            return render_template('add_email.html')

        # check file type
        is_txt = '.' not in f.filename or\
            ('.' in f.filename and f.filename.rsplit('.', 1)[1].lower()=='txt')
        if not is_txt:
            flash("Only txt file is supported", 'danger')
            return render_template('add_email.html')

        # check duplicate upload
        cur = mysql.connection.cursor()
        result = cur.execute("select * from emails where file_name=%s and upload_by=%s",
                            (secure_filename(f.filename), session['userid']))
        if result >0:
            flash("The file has existed",'danger')
            return redirect(url_for('dashboard'))

        basepath = os.path.dirname(__file__)
        upload_dir = os.path.join(basepath, 'static/uploads',str(session['userid']))
        print('\n\nadd path ', upload_dir)

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        f.save(os.path.join(upload_dir,secure_filename(f.filename)))

        # Execute
        cur.execute("INSERT INTO emails(file_name, upload_by) VALUES(%s, %s)",(secure_filename(f.filename), session['userid']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Email Loaded', 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_email.html')


# Delete Email File
@app.route('/delete_email/<string:id>', methods=['POST'])
@is_logged_in
def delete_email(id):
    # create cursor
    cur = mysql.connection.cursor()

    # get email file path from database
    result = cur.execute("SELECT * FROM emails WHERE id = %s", [id])
    email = cur.fetchone()

    # delete file in server
    basepath = os.path.dirname(__file__)
    path = os.path.join(basepath, 'static/uploads',str(email['upload_by']), email['file_name'])
    print('\n\ndelete path ', path)
    if os.path.exists(path):
        os.remove(path)

    # delete record in DB
    cur.execute("DELETE FROM emails WHERE id = %s", [id])

    # commit to DB
    mysql.connection.commit()

    #close connection
    cur.close()

    flash('Email Deleted', 'success')

    return redirect(url_for('dashboard'))

# Predict Email Class
@app.route('/predict_email/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def predict_email(id):
    # Step 1: get email file path from database
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM emails WHERE id = %s", [id])
    email = cur.fetchone()

    # Step 2: load email file
    basepath = os.path.dirname(__file__)
    path = os.path.join(basepath, 'static/uploads',str(email['upload_by']), email['file_name'])
    print('\n\npredict path ', path)
    if not os.path.exists(path):
        flash('Sorry we cannot find the file, please delete and upload again.','danger')
        return redirect(url_for('dashboard'))

    test_doc = pipeline.load_document(path = path, label = None)

    # Step 3: clean text data
    pipeline.clean_document(test_doc,
                            word_split_regex = tokenize_regex1,
                            stop_words = stop_words,
                            contraction_dict = 'default')

    # Step 4: load pipeline
    model_path = os.path.join(basepath, 'static/models','svm_model.sav')
    model = pickle.load(open(model_path, 'rb'))

    # Step 5: predict
    pred = model.predict([test_doc])
    label_pred = category[int(pred[0])]
    app.logger.info('\n\n\n'+label_pred+'\n\n\n')

    # Step 6: update database
    cur.execute("update emails set predicted_label=%s where id=%s", (label_pred,id))
    mysql.connection.commit()
    #Close connection
    cur.close()

    flash('Email Predicted', 'success')

    return redirect(url_for('dashboard'))

# Request Reset Form
class RequestResetForm(Form):
    email = StringField('Enter your email address', [validators.Length(min=6, max=100)])

# Send reset email
def send_reset_email(userid, email, username=None, type='password', expires_sec=1800):
    if type == 'password':
        s = Serializer(app.secret_key, expires_sec)
        token = s.dumps({'userid':userid}).decode('utf-8')

        msg = Message('Password Reset Request',
                      sender='noreply@singularity.com',
                      recipients=[email])
        msg.body = "To reset your password, visit the following link:\n"\
        f"{url_for('reset_password', token=token, _external=True)}\n\n"\
        "If you did not make this request then simply ignore this email "\
        "and no changes will be made.\n\nThanks,\nEmail Classification System"
    elif type == 'username':
        msg = Message('Username Reset Request',
                      sender='noreply@singularity.com',
                      recipients=[email])
        msg.body = f"Your username is\n\n{username}\n\n"\
        "You can login to change your username:\n"\
        f"{url_for('login', _external=True)}\n\n"\
        "If you did not make this request then simply ignore this email "\
        "and no changes will be made.\n\nThanks,\nEmail Classification System"
    else:
        raise ValueError("type should be `password` or `username`")
    mail.send(msg)


# Reset Password
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = RequestResetForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data

        # check if email is matched
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])
        if not result:
            flash("There is no account with that email. You must register first.", "danger")
        else:
            data = cur.fetchone()
            send_reset_email(data['id'], email, type='password')
            flash('An email has been sent with instructions to reset your password.', 'success')
            cur.close()
            session.clear()
            return redirect(url_for('login'))
        cur.close()
    return render_template('reset_request.html', form=form)

def verify_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            userid = s.loads(token)['userid']
        except:
            return None
        return userid

class ResetPasswordForm(Form):
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=1),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route("/reset_password/<token>", methods = ['GET','POST'])
def reset_password(token):
    userid = verify_reset_token(token)
    if userid is None:
        flash('That is an invalid or expired token', 'danger')
        return redirect(url_for('reset_password_request'))

    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("update users set pass_word=%s where id=%s", (password, userid))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# Forgot username
@app.route('/reset_username_request', methods=['GET', 'POST'])
def reset_username_request():
    form = RequestResetForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data

        # check if email is matched
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])
        if not result:
            flash("There is no account with that email. You must register first.", "danger")
        else:
            data = cur.fetchone()
            send_reset_email(data['id'], email, username=data['username'], type='username')
            flash('An email has been sent with your username.', 'success')
            cur.close()
            return redirect(url_for('login'))
        cur.close()
    return render_template('reset_request.html', form=form)
