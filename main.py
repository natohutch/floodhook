from azure.storage.blob import BlobServiceClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os, json

print(BlobServiceClient)

connstr = os.environ["AZURE_BLOB_CONNSTR"]

engine = create_engine(f"postgresql://postgres@localhost:5432", future=True)

app = Flask(__name__)
CORS(app)

@app.route("/7Wekkt9Hp2kI9LX4pZ0LzxRcebTdiReYI5VibwEv2OI3BoXSYYLiSJPCaD5X9UB1")
def hook():
    with engine.connect() as conn:
        result = conn.execute(text("""
        SELECT 1,2,3
        """))
        return(result.all()[0][0])

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=80)

# container_name = "rainfields3"

# blob_service_client = BlobServiceClient.from_connection_string(connstr)

# # Create a local directory to hold blob data
# local_path = "./tmp"

# blob_file_name = "IDR03AR.RF3.20220718103000.nc"
# blobl_file_path = "/blobServices/default/containers/rainfields3/blobs/"

# blob_client = blob_service_client.get_container_client(container= container_name) 

# with open("./tmp/"+blob_file_name, "wb") as download_file:
#  download_file.write(blob_client.download_blob(blob_file_name).readall())