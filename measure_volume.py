import nibabel as nib
import numpy as np

def calculate_volume(mask_file):
    mask_img = nib.load(mask_file)
    mask_data = mask_img.get_fdata()

    voxel_dims = mask_img.header.get_zooms()
    voxel_volume = np.prod(voxel_dims)
    
    segmented_voxels = np.sum(mask_data > 0)
    total_volume = segmented_voxels * voxel_volume

    return total_volume


if __name__ == "__main__":
    print("Brain volume:", calculate_volume("outputBrainExtractionMask.nii.gz"))