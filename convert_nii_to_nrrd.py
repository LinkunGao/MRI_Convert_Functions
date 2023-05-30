import SimpleITK as sitk


def convert_nii_to_nrrd():
    source = [r'./import/img_inv_contrast_0-1.nii.gz', r'./import/img_inv_contrast_0-2.nii.gz',
              r'./import/img_inv_contrast_0-3.nii.gz', r'./import/img_inv_contrast_0-4.nii.gz']
    dest = [r'./export/r1.nrrd',r'./export/r2.nrrd',r'./export/r3.nrrd',r'./export/r4.nrrd']

    pre = r'H:\docker\import_nrrd\26\new_0.nrrd'
    pre_image = sitk.ReadImage(pre)
    for i in range(len(source)):

        input_image = sitk.ReadImage(source[i])
        input_image.CopyInformation(pre_image)
        sitk.WriteImage(input_image, dest[i])


if __name__ == "__main__":
    convert_nii_to_nrrd()
