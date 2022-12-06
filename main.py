from azure.storage.blob import BlobServiceClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os, json, re, requests
from datetime import datetime
from pytz import timezone

last_file = ""

connstr = os.environ["AZURE_BLOB_CONNSTR"]
blob_service_client = BlobServiceClient.from_connection_string(connstr)
container_name = "rainfields3"
blob_client = blob_service_client.get_container_client(container=container_name)

local_path = "./tmp"
if not os.path.isdir(local_path):
    os.mkdir(local_path)

engine = create_engine(f"postgresql://postgres@postgres?host=/var/run/postgresql/", future=True)

app = Flask(__name__)
CORS(app)

@app.route("/7Wekkt9Hp2kI9LX4pZ0LzxRcebTdiReYI5VibwEv2OI3BoXSYYLiSJPCaD5X9UB1", methods=["POST"])
def hook():
    global last_file
    global blob_client
    utc = timezone("utc")
    syd = timezone("Australia/Sydney")

    json = request.get_json()
    file_name = json["file-name"]

    if (file_name != last_file):
        last_file = file_name
        blob_file_name = re.search("/blobs/(.*)$", file_name).group(1)
        timestamp_text = re.search("RF3\.(.*)\.nc$", blob_file_name).group(1)
        timestamp_utc = utc.localize(datetime.strptime(timestamp_text, "%Y%m%d%H%M%S"))
        timestamp_syd = timestamp_utc.astimezone(syd)
        timestamp_text_syd = datetime.strftime(timestamp_syd, "%Y%m%dT%H%M")
        
        print(timestamp_text_syd)
        
        with open("./tmp/current.nc", "wb") as download_file:
          download_file.write(blob_client.download_blob(blob_file_name).readall())
        
        os.system("raster2pgsql tmp/current.nc temporary_raster -d | psql -U postgres")

        with engine.begin() as conn:
            conn.execute(text("""
            INSERT INTO rainfall_raster (stamp, rast) VALUES (:stamp, (SELECT st_transform(st_setsrid(rast, 100001), 4326) FROM temporary_raster))
            """), {"stamp": timestamp_text_syd})
            requests.request("GET", "http://172.17.0.1:8080/newfile")

        print("\n\n")

    return file_name

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=80)

#'/blobServices/default/containers/rainfields3/blobs/IDR03AR.RF3.20220721020500.nc'
