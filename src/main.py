import subprocess
import SimpleITK as sitk
import os
from measure_volume import calculate_volume
from overlays import *
from flask import Flask, request, redirect, jsonify
from minio import Minio
import boto3
from botocore.client import Config
import tarfile
import sys
import shutil

app = Flask(__name__)

ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")

#minio_client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)
#if not minio_client.bucket_exists(BUCKET_NAME):
#   minio_client.make_bucket(BUCKET_NAME)

s3 = boto3.client('s3',
                 endpoint_url="http://minio:9000",
                 aws_access_key_id=ACCESS_KEY,
                 aws_secret_access_key=SECRET_KEY)

@app.route("/", methods=["GET", "POST"])
def upload_data():
    if request.method == "POST":
    
        file_path = request.form.get("file_path")

        #size = os.fstat(file.fileno()).st_size
        
        #minio_client.put_object(
        #        BUCKET_NAME, file.filename, file, size)

        s3.upload_file(file_path, BUCKET_NAME, os.path.basename(file_path))

        return redirect(request.url)
    
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>UPLOAD</title>
        </head>
        <body>
          <h1>Upload File</h1>
          <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
          </form>
        </body>
        </html>
        """

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    object_name = request.args.get('object_name')
        
    if not object_name:
        return jsonify({'error': 'Missing object_name parameter'}), 400

    file_path = os.path.join('/test-assignment', object_name) 

    #response = minio_client.get_object(BUCKET_NAME, object_name)
    #with open(file_path, "wb") as f:
    #    f.write(response.read())

    s3.download_file(BUCKET_NAME, object_name, file_path)
    try:
       segment(file_path)
    except Exception as e:
       return jsonify({'error':  {str(e)}}), 500
        
    return redirect(request.url)
    

def segment(file_path):
    with tarfile.open(file_path, "r:bz2") as tar:
        tar.extractall(path="/test-assignment/77654033_19950903")
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(os.path.join("/test-assignment", "77654033_19950903/77654033/19950903/CT2"))
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    sitk.WriteImage(image, os.path.join("CT2.nii.gz"))

    command = "/test-assignment/install/bin/antsBrainExtraction.sh -d 3 -a CT2.nii.gz -e templates/T_template0.nii.gz  -m templates/T_template0_BrainCerebellumProbabilityMask.nii.gz -o output"
    subprocess.run(command, shell=True)

    mask_path = 'outputBrainExtractionMask.nii.gz'
    with open("brain-volume.txt", 'w') as f:
        f.write(str(calculate_volume(mask_path)))
    
    image_path = 'outputBrainExtractionBrain.nii.gz'
    output_directory = 'png_overlays'
    image, _ = load_nifti(image_path)
    mask, _ = load_nifti(mask_path)
    slices = get_slices(image, mask)
    overlays = overlay_slices(slices)
    save_overlays(overlays, output_directory)
    
    files_to_zip = ['brain-volume.txt', 'outputBrainExtractionMask.nii.gz']
    directory_to_zip = 'png_overlays'
    zip_filename = 'outputs'
    temp_dir = 'temp_zip_dir'
    os.makedirs(temp_dir, exist_ok=True)
    for file in files_to_zip:
        shutil.copy(file, temp_dir)

    shutil.copytree(directory_to_zip, os.path.join(temp_dir, directory_to_zip))
    shutil.make_archive(zip_filename, 'zip', temp_dir)

    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
