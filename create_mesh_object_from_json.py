from pathlib import Path
from skimage.measure import marching_cubes
import json
import numpy as np


if __name__ == '__main__':
    source = Path(r'./path/to/mask.json')
    dest = Path(r'./path/to/mesh.obj')

    with open(source) as user_file:
        file_contents = user_file.read()
        parsed_json = json.loads(file_contents)

    images = []
    width = parsed_json[0]["width"]
    height = parsed_json[0]["height"]
    depth = len(parsed_json)
    for i in range(len(parsed_json)):
        data = parsed_json[i]["data"]
        if len(data) == 0:
            data = [0] * width * height * 4
        images.append(data)
    pixels = np.array(images, dtype=np.uint8).reshape((depth, height, width, 4))

    # Take the average of the RGB values and use the Alpha value as the transparency
    merged_pixels = np.mean(pixels[:, :, :, :3], axis=3)
    merged_pixels[merged_pixels > 0] = 255
    arr = np.transpose(merged_pixels, (2, 1, 0))
    spacing = parsed_json[0]["voxelSpacing"]
    origin = parsed_json[0]["spaceOrigin"]

    verts, faces, normals, values = marching_cubes(arr)
    # voxel grid coordinates to world coordinates: verts * voxel_size + origin
    verts = verts * spacing + origin
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


