import pika, json

def upload(f, fs, channel, access):
    try:
        # write the video binary data into the db using gridfs
        # it returns a file id object
        fid = fs.put(f)
    except Exception as err: # server error in case of failure
        print(err)
        return "Internal Server Error", 500
    
    # message created as a Python Dictionary
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }
    
    try: # publishing the message 
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message), # serialize the data
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # if error, delete the file from the mongodb
        print(err)
        fs.delete(fid)
        return "internal server error", 500