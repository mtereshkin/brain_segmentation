import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import os

def load_nifti(file_path):
    nifti_img = nib.load(file_path)
    return nifti_img.get_fdata(), nifti_img.affine

def get_slices(image, mask):
    x, y, z = image.shape
    
    slices = {
        'sagittal': (image[x//2, :, :], mask[x//2, :, :]),
        'coronal': (image[:, y//2, :], mask[:, y//2, :]),
        'axial': (image[:, :, z//2], mask[:, :, z//2])
    }
    
    return slices

def overlay_slices(slices):
    overlays = {}
    for plane, (img_slice, mask_slice) in slices.items():
        overlay = np.zeros((*img_slice.shape, 3), dtype=np.uint8)
        overlay[..., 0] = img_slice 
        overlay[..., 1] = img_slice  
        overlay[..., 2] = img_slice
        
        overlay[mask_slice > 0, 0] = 255
        overlays[plane] = overlay
        
    return overlays

def save_overlays(overlays, output_dir):
    """Save overlays as PNG files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for plane, overlay in overlays.items():
        plt.imshow(overlay)
        plt.axis('off')
        output_path = os.path.join(output_dir, f"{plane}.png")
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
