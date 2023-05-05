# src/gateway/server.py
import os, json, pika
import gridfs # GridFS is a specification for storing and retrieving files that exceed the BSON-document size limit of 16 MB. 
from flask import Flask, request,
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config['MONGO_URI'] = "mongodb://host.minikube.internal:27017/videos"    
mongo = PyMongo(server)
db = mongo.db
fs = gridfs.GridFS(db)
channel = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")).channel()
channel.queue_declare(queue='video')


@server.route('/login', methods=['POST'])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err
    

@server.route('/upload', methods=['POST'])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly one file required", 400
        
        for _, file in request.files.items():
            err = util.upload(f, fs, channel, access)
            if err:
                return err
            
            return "uploading", 200
    else:
        return "not authorized", 401
    
@server.route('/download', methods=['GET'])
def download():
    pass


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)




            