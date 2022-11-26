import base64
import os
from pickle import TRUE

UPLOAD_DIRECTORY = "crystal-plasticity-toolbox/uploads/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def save_file(name, content):
    for file_name in os.listdir(UPLOAD_DIRECTORY):
        file = UPLOAD_DIRECTORY + file_name
        if os.path.isfile(file):
            os.remove(file)

    # Decode and store a file uploaded with Plotly Dash.
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def check_uploaded_file(uploaded_filename):
    if os.path.exists(os.path.join(UPLOAD_DIRECTORY, uploaded_filename)):
        return "File uploaded successfully: ",uploaded_filename
    else:
        return "No files uploaded."
