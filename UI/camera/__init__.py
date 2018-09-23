from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_cache import Cache

app  = Flask(__name__)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

app.config['GOOGLE_ID'] = "1036689765758-d695qg7ink176psvkqeqr6ol5caajmrf.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "HnOJcqz98SZibANFqX-LClIq"
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
app.debug = True
app.secret_key = '39380a3952f0ae125a699fd873560c51'



bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'red lighten-1'

from camera import routes