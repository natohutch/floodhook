from azure.storage.blob import BlobServiceClient
import os, uuid
print(BlobServiceClient)
"""
connstr = "#####"

container_name = "rainfields3"

blob_service_client = BlobServiceClient.from_connection_string(connstr)

# Create a local directory to hold blob data
local_path = "./tmp"

blob_file_name = "IDR03AR.RF3.20220718103000.nc"
blobl_file_path = "/blobServices/default/containers/rainfields3/blobs/"

blob_client = blob_service_client.get_container_client(container= container_name) 

with open("./tmp/"+blob_file_name, "wb") as download_file:
 download_file.write(blob_client.download_blob(blob_file_name).readall())
"""