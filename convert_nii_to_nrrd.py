import SimpleITK as sitk
from pathlib import Path

def convert_nii_to_nrrd():
    source = Path(r'./path/to/mask.nii.gz')
    dest = Path(r'./path/to/mask.nrrd')

    input_image = sitk.ReadImage(source)
    sitk.WriteImage(input_image, dest)


if __name__ == "__main__":
    convert_nii_to_nrrd()