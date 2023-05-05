import pika,json

def upload(f,fs,channel,access):
    try:
        file_id = fs.put(f, filename=f.filename)
    except Exception as e:
        return str(e), 500
    
    message = {
        "video_file_id": str(file_id),
        "mp3_file_id": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(exchange='', routing_key='video', body=json.dumps(message))
    except Exception as e:
        return str(e), 500
    
        