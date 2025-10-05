import SimpleITK as sitk
import os
import shutil

'''
A python script for convert dicom files to nrrd file with sepreating contrast.
If your dicom files include 5 different contrast images, using this script, 
you will get 5 nrrd files with different contrast!


:Python version: v3.9.0
:Dependency: pip install SimpleITK

:Author: Linkun Gao

'''


def dcmseries_divider(filepath, output_dir):
    datapath = filepath
    allFilesPath = []
    max = 0
    contrstIdx = 0

    dcms_name = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(datapath)

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        instanceNum = int(dicom.GetMetaData('0020|0012'))
        if max < instanceNum:
            max = instanceNum

    for i in range(max):
        allFilesPath.append([])

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        instanceNum = int(dicom.GetMetaData('0020|0012')) - 1
        allFilesPath[instanceNum].append(dcm)

    copy_dcms_by_index(allFilesPath, output_dir)


def copy_dcms_by_index(allFilesPath, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for idx, paths in enumerate(allFilesPath):
        folder = os.path.join(output_dir, str(idx))
        os.makedirs(folder, exist_ok=True)
        for src in paths:
            shutil.copy(src, folder)


filepath = "/Your/dicom/files/path"
output_dir = "/Your/dicom/files/output"
dcmseries_divider(filepath, output_dir)
