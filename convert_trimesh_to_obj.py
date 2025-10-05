import morphic
import trimesh

def convert_trimesh_to_obj():
    mesh = morphic.Mesh(r"Z:\sandbox\afu254\Duke\mesh\14_fitted_skin.mesh")
    surface = mesh.get_surfaces(res=8)
    tri_mesh = trimesh.Trimesh(surface[0], surface[1])
    tri_mesh.export(r"./test/mesh14.obj")

if __name__ == '__main__':
    convert_trimesh_to_obj()