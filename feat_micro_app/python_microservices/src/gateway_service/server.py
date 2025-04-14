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