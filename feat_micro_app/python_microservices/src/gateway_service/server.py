import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

# make the connection synchronous with rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))