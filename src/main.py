import subprocess
import SimpleITK as sitk
import os
from measure_volume import calculate_volume
from overlays import *

def main():
    curr_dir = os.getcwd()

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(os.path.join(curr_dir, "77654033_19950903/77654033/19950903/CT2"))
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    sitk.WriteImage(image, os.path.join(curr_dir, "CT2.nii.gz"))

    command = "/test-assignment/install/bin/antsBrainExtraction.sh -d 3 -a CT2.nii.gz -e templates/T_template0.nii.gz  -m templates/T_template0_BrainCerebellumProbabilityMask.nii.gz -o output"
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
    curr_dir = os.getcwd()
    parent_dir = os.path.dirname(curr_dir)
    os.path.join(parent_dir, "77654033_19950903/77654033/19950903/CT2")
    main()
