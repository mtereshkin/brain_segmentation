import subprocess
import SimpleITK as sitk
import os
from measure_volume import calculate_volume
from overlays import *
from flask import Flask, request, jsonify
from minio import Minio
import tempfile
import zipfile
import shutil

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")

client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)

@app.route('/upload-data', methods=['POST'])
def upload_data():
    file = request.files['file']
    
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)
    
    minio_client.fput_object(bucket_name, file.filename, file_path)
    os.remove(file_path)

    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    object_name = request.args.get('object_name')
        
    if not object_name:
        return jsonify({'error': 'Missing object_name parameter'}), 400
        

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, object_name)
        
 
    minio_client.fget_object(bucket_name, object_name, zip_path)
        

    extract_path = os.path.join(temp_dir, 'extracted')
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        

    main(extract_path)
        
    return jsonify({'message': 'Data fetched and processed successfully', 'output_path': extract_path}), 200
    


@app.route('/upload-results', methods=['POST'])
def upload_results():

    output_path = request.json.get('output_path')
        
    if not output_path:
        return jsonify({'error': 'Missing output_path parameter'}), 400
        
    output_zip_path = os.path.join(tempfile.mkdtemp(), 'output.zip')
    shutil.make_archive(output_zip_path.replace('.zip', ''), 'zip', output_path)
        
    output_zip_name = f'processed_output.zip'
    with open(output_zip_path, 'rb') as f:
        minio_client.put_object(bucket_name, output_zip_name, f, os.path.getsize(output_zip_path))
        
    return jsonify({'message': 'Results uploaded successfully'}), 200

def main(data_dir):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(os.path.join(data_dir, "77654033_19950903/77654033/19950903/CT2"))
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    sitk.WriteImage(image, os.path.join(curr_dir, "CT2.nii.gz"))

    command = "antsBrainExtraction.sh -d 3 -a CT2.nii.gz -e templates/T_template0.nii.gz  -m templates/T_template0_BrainCerebellumProbabilityMask.nii.gz -o output"
    subprocess.run(command, shell=True)

    mask_path = 'outputBrainExtractionMask.nii.gz'
    print("Brain volume:", calculate_volume(mask_path))
    
    image_path = 'outputBrainExtractionBrain.nii.gz'
    output_directory = 'png_overlays'
    image, _ = load_nifti(image_path)
    mask, _ = load_nifti(mask_path)
    slices = get_slices(image, mask)
    overlays = overlay_slices(slices)
    save_overlays(overlays, output_directory)

if __name__ == "__main__":
    app.run()
