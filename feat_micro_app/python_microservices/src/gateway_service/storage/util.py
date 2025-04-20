import pika, json

def upload(f, fs, channel, access):
    try:
        # write the video binary data into the db using gridfs
        # it returns a file id object
        fid = fs.put(f)
    except Exception as err: # server error in case of failure
        print(err)
        return "Internal Server Error", 500
    
    