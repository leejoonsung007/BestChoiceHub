# Schools-Repo

week4

<<<<<<< HEAD
## 1. SETTING ENV VARIABLE
=======
#### 1. SETTING ENV VARIABLE
>>>>>>> 4853b580635f4484dc2c44eace9ee95867dbb26f

`(venv) LeejoonsungdeMacBook-Pro: sudo vim ./~bashrc`

AND COPY THEM INTO YOUR COMPUTER ENV

`export PATH="$PATH:$HOME/.rvm/bin"`

<<<<<<< HEAD
`export MAIL_USERNAME="schoolselectionie@gmail.com"`

=======
>>>>>>> 4853b580635f4484dc2c44eace9ee95867dbb26f
`export MAIL_PASSWORD="ABC12345!"`

`export FLASKY_ADMIN="schoolselectionie@gmail.com"`

`export DEV_DATABASE_URL="mysql+pymysql://root:1234@localhost/mysql"`

`export MODERATOR="leejoonsung007@gmail.com"`

`export GOOGLE_OAUTH_CLIENT_ID="429221528820-0876ccgupb8rjtpl0730h2koa6vrklq7.apps.googleusercontent.com"`

`export GOOGLE_OAUTH_CLIENT_SECRET="q3vtKBcD8MPvT6R8TN3d0J6s"`

`export FACEBOOK_OAUTH_CLIENT_ID="171456803533554"`

`export FACEBOOK_OAUTH_CLIENT_SECRET="f549e71623d6c266bbce9a78a54b62b0"`

### NOTE: YOU MUST CREATE A DATABASE NAMED mysql FRIST, THE ACCOUNT OF IT IS ROOT AND PASSWORD IS 1234
<<<<<<< HEAD

## 2. INSTALL LIBRARIES

`(venv) LeejoonsungdeMacBook-Pro:   cd Code`

`(venv) LeejoonsungdeMacBook-Pro:   cd requirement`

`(venv) LeejoonsungdeMacBook-Pro:   pip install -r requirements.txt`


## 3. DATABASE MIGRATION
=======

#### 2. INSTALL LIBRARIES

`(venv) LeejoonsungdeMacBook-Pro:   cd Code`

`(venv) LeejoonsungdeMacBook-Pro:   cd requirement`

`(venv) LeejoonsungdeMacBook-Pro:   pip install -r requirements.txt`


#### 3. DATABASE MIGRATION
>>>>>>> 4853b580635f4484dc2c44eace9ee95867dbb26f

mac

run in Terminal

`(venv) LeejoonsungdeMacBook-Pro:   export FLASK_APP=run.py`

`(venv) LeejoonsungdeMacBook-Pro:   flask db upgrade`



windows

run in Terminal

`(venv) LeejoonsungdeMacBook-Pro:   set FLASK_APP=run.py`

`(venv) LeejoonsungdeMacBook-Pro:   flask db upgrade`

<<<<<<< HEAD
## 4. RUN
=======
#### 4. RUN
>>>>>>> 4853b580635f4484dc2c44eace9ee95867dbb26f

`(venv) LeejoonsungdeMacBook-Pro: flask run`

### Note: Before the webiste is deplyed, the website link should be http://localhost:5000/, not http://127.0.0.1:5000/. Otherwise, facebook cannot login normally 

