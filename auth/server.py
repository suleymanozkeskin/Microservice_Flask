import time
from dotenv import load_dotenv
import jwt
import datetime
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from models import User, db
load_dotenv()

# config
database_url = (
    f"postgresql://{os.environ.get('DATABASE_USERNAME')}:{os.environ.get('DATABASE_PASSWORD')}"
    f"@{os.environ.get('DATABASE_HOSTNAME')}:{os.environ.get('DATABASE_PORT')}/{os.environ.get('DATABASE_NAME')}"
)

def connect_to_db():
    try:
        conn = psycopg2.connect(database_url)
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False

server = Flask(__name__)


# config 
server.config['SQLALCHEMY_DATABASE_URI'] = database_url
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(server)

# routes
@server.route("/")
def index():
    ## Add  little style to the index page so it's easier to read
    return """ 
    <style>
        body {
            font-family: JetBrains Mono, monospace;
            font-size: 1.5rem;
            padding: 2rem;
        }
    </style>
    <h1>System Design and Microservices with Flask, <br/> Python, Kubernetes and Docker</h1>
    <h2>Auth Service</h2>
    <p>Endpoints:</p>
    <ul>
        <li><a href="/register">/register</a></li>
        <li><a href="/login">/login</a></li>
        <li><a href="/validate">/validate</a></li>
    </ul>
    """

    
# register a user
@server.route("/register", methods=["POST"])
def register():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # check db for existing user
    user = User.query.filter_by(email=auth.username).first()
    if user:
        return "user already exists", 409

    # create new user
    new_user = User(email=auth.username, password=auth.password)
    db.session.add(new_user)
    db.session.commit()

    return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)

# login a user
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization  # Basic Auth header
    if not auth:
        return "missing credentials", 401

    # check db if user exists
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return "user does not exist", 404

    # check db for username and password
    user = User.query.filter_by(email=auth.username).first()

    if user:
        if auth.username != user.email or auth.password != user.password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401

# validate a user
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except:
        return "not authorized", 403

    return decoded, 200

# create JWT with HS256
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )



def main():
    while not connect_to_db():
        print("Waiting for database connection...")
        time.sleep(3)

    print("Database connected. Running app.")
    with server.app_context():
        db.create_all()
    server.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()