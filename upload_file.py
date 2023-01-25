import base64
import os
from pickle import TRUE

UPLOAD_DIRECTORY = "/Users/kimbi/Documents/Specialization Project/CP_Files/uploads/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

#This function saves the uploaded file to the upload directory
def save_file(name, content):
    """
    Input: File name, File content
    Output: Decoded and saved file in upload directory
    """
    for file_name in os.listdir(UPLOAD_DIRECTORY):
        file = UPLOAD_DIRECTORY + file_name
        if os.path.isfile(file):
            os.remove(file)

    # Decode and store a file uploaded with Plotly Dash.
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

#This function checks is the file is uploaded successfully and returns a message
def check_uploaded_file(uploaded_filename):
    """
    Input: Uploaded filename
    Output: Message whether the file upload was successful or not
    """
    if os.path.exists(os.path.join(UPLOAD_DIRECTORY, uploaded_filename)):
        return "File uploaded successfully: ",uploaded_filename
    else:
        return "No files uploaded."