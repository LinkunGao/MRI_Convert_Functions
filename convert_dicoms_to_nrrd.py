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
    preSlicePos = 0
    count = 0
    contrstIdx = 0

    dcms_name = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(datapath)

    for dcm in dcms_name:
        dicom = sitk.ReadImage(dcm)
        slicePos = dicom.GetMetaData('0020|1041')
        if slicePos != preSlicePos and preSlicePos != 0:
            break
        if slicePos != preSlicePos and preSlicePos == 0:
            preSlicePos = slicePos
        allFilesPath.append([])

    for dcm in dcms_name:
        if count > len(allFilesPath) - 1:
            count = 0
        allFilesPath[count].append(dcm)
        count += 1
    dcms_read = sitk.ImageSeriesReader()

    for list in allFilesPath:
        dcms_read.SetFileNames(list)
        dcms_series = dcms_read.Execute()
        name = "new_" + str(contrstIdx)
        contrstIdx+= 1
        sitk.WriteImage(dcms_series, name + '.nrrd')


filepath = "/Your/dicom/files/path"
dcmseries2nrrd(filepath)
