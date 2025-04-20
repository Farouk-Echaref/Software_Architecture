import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

# from docs: Manage MongoDB connections for our flask app
# Connect to MongoDB databases running on the host machine (outside Minikube)
# 'videos' and 'mp3s' are two separate databases used for storing video and audio file metadata
# 'host.minikube.internal' allows services inside Minikube to access the host's MongoDB server
mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")


# Initialize GridFS instances for storing large files (like videos and MP3s) in MongoDB
# GridFS allows storing files that exceed the BSON-document size limit (16MB)
# fs_videos will store video files in the 'videos' database
# fs_mp3s will store MP3 files in the 'mp3s' database
fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

# rabbitmq will be deployed as a StatefulSet 
# make the connection synchronous with rabbitmq
# Establish a blocking connection to the RabbitMQ message broker running at hostname 'rabbitmq'
# This assumes a RabbitMQ service is reachable in the same network (e.g., within the Kubernetes cluster or Docker network)
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

# Open a channel through which messages can be published and consumed
channel = connection.channel()

# Login Route:
# it's going to communicate with our auth service to log the user in and assign a token to that user

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    
    if not err:
        return token
    else:
        return err
    
# Upload route
# the route to be used to upload our video that we want to convert
@server.route("/upload", methods=["POST"])
def upload():
    # access is the decoded token claims as a json string that contains our payload with our claims
    access, err = validate.token(request)
    
    # deserialize the Json string to a python object (dictionary)
    access = json.loads(access)
    
    # check the user privileges (admin in the payload), if it's true we'll give the user access to all of the endpoints
    if access["admin"]: # resolves to true or false
        # we will only allow the upload of exactly one file per request
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file required", 400 # bad request http code
        
        # retrieve the file
        for key, file in request.files.items():
            # params: the actual file, the gridfs instance for the videos, rabbitmq channel, and the access token
            err = util.upload(file, fs_videos, channel, access)
            
            if err:
                return err
        
        return "Success!", 200
    else:
        return "Not Authorized", 401 # Unauthorized http code
    
# download endpoint which is going to be used to download the MP3 that was created from the converted video

@server.route("/download", methods=["GET"])
def download():
    pass