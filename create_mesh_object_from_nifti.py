from pathlib import Path
from skimage.measure import marching_cubes
import nibabel as nib
import time


def convert_nii_to_mesh(source='./path/to/mask.nii.gz', dest='./path/to/mesh.obj'):

    source = Path(source)
    dest = Path(dest)

    img = nib.load(source)
    spacing = img.header.get_zooms()
    arr = img.get_fdata()

    verts, faces, normals, values = marching_cubes(arr)
    # voxel grid coordinates to world coordinates: verts * voxel_size + origin
    verts = verts * spacing + img.affine[0:3, -1]
    # without spacing
    # verts = verts + img.affine[0:3, -1]
    faces = faces + 1

    for idx, normal in enumerate(normals):
        normal = [-n for n in normal]
        normals[idx] = normal

    with open(dest, 'w') as out_file:
        for item in verts:
            out_file.write("v {0} {1} {2}\n".format(item[0], item[1], item[2]))
        for item in normals:
            out_file.write("vn {0} {1} {2}\n".format(item[0], item[1], item[2]))
        for item in faces:
            out_file.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0], item[1], item[2]))
    out_file.close()



if __name__ == '__main__':
    convert_nii_to_mesh()
