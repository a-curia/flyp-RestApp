
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\gheorgheadrian.curia\\source\\repos\\FlaskREST-API\\FlaskREST-API\\FlaskREST_API\\database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False