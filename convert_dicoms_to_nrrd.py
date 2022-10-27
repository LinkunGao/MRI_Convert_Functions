import SimpleITK as sitk

'''
A python script for convert dicom files to nrrd file with sepreating contrast.
If your dicom files include 5 different contrast images, using this script, 
you will get 5 nrrd files with different contrast!


:Python version: v3.9.0
:Dependency: pip install SimpleITK

:Author: Linkun Gao

'''

def dcmseries2nrrd(filepath):
    datapath = filepath
    allFilesPath = []
    max = 0
    contrstIdx = 0

    dcms_name = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(datapath)

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        instanceNum = int(dicom.GetMetaData('0020|0012'))
        if max < instanceNum:
            max= instanceNum

    for i in range(max):
        allFilesPath.append([])

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        instanceNum = int(dicom.GetMetaData('0020|0012'))-1
        allFilesPath[instanceNum].append(dcm)

    dcms_read = sitk.ImageSeriesReader()

    for list in allFilesPath:
        dcms_read.SetFileNames(list)
        dcms_series = dcms_read.Execute()
        name = "new_" + str(contrstIdx)
        contrstIdx+= 1
        sitk.WriteImage(dcms_series, name + '.nrrd')

filepath = "/Your/dicom/files/path"
dcmseries2nrrd(filepath)
