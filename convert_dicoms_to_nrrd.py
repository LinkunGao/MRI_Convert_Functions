import SimpleITK as sitk
import os

'''
A python script for convert dicom files to nrrd file with sepreating contrast.
If your dicom files include 5 different contrast images, using this script, 
you will get 5 nrrd files with different contrast!


:Python version: v3.9.0
:Dependency: pip install SimpleITK

:Author: Linkun Gao

'''


def dcm_series_to_nrrd(dcm_folder_path, output_dir):
    # Assign DCM paths with different contrasts to separate lists.
    all_files_path = _divide_dcms_to_different_contrasts(dcm_folder_path)
    # Convert each contrast dcms to a nrrd file.
    _convert_dicoms_contrast_to_nrrd(all_files_path, output_dir)


def _divide_dcms_to_different_contrasts(dcm_folder_path):
    """

    :param dcm_folder_path: dicoms folder path, may include multiple contrast dicom files
    :return: each contrast dicom file is divided into different lists
    """
    all_files_path = []
    max_instance_num = 0

    dcms_name = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(dcm_folder_path)

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        instance_num = int(dicom.GetMetaData('0020|0012'))
        if max_instance_num < instance_num:
            max_instance_num = instance_num

    for i in range(max_instance_num):
        all_files_path.append([])

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        instance_num = int(dicom.GetMetaData('0020|0012')) - 1
        all_files_path[instance_num].append(dcm)

    return all_files_path


def _convert_dicoms_contrast_to_nrrd(all_files_path, output_dir):
    """

    :param all_files_path: all contrast dicom files are divided into different lists
    :param output_dir: save nrrd files path
    :return:
    """
    os.makedirs(output_dir, exist_ok=True)
    contrast_idx = 0
    dcm_reader = sitk.ImageSeriesReader()

    for dcm_files_path in all_files_path:
        name = "new_" + str(contrast_idx)
        output_path = os.path.join(output_dir, f'{name}.nrrd')
        contrast_idx += 1

        _convert(dcm_reader, dcm_files_path, output_path)


def _convert(dcm_reader, dcm_files_path, output_path):
    """
    :param dcm_reader: SimpleITK Image Reader
    :param dcm_files_path: one contrast dicom files
    :param output_path: nrrd file path
    :return:
    """
    dcm_reader.SetFileNames(dcm_files_path)
    dcm_series = dcm_reader.Execute()
    sitk.WriteImage(dcm_series, output_path)


dcm_folder_path = "/Your/dicom/files/path"
output_dir = "./test"
dcm_series_to_nrrd(dcm_folder_path, output_dir)
