import os
import re

def MeshImporter(polymesh_dir_path, return_edges=True):
    """
    Import mesh data from OpenFOAM's polymesh directory.

    Parameters:
    - polymesh_dir_path (str): Path to the polymesh directory.
    - return_edges (bool, optional): If True, the function returns edges along with other mesh data. Default is True.

    Returns:
    Tuple: Tuple containing mesh data, including owner, neighbour, points, faces, and edges (if return_edges is True).

    Example:
    owner, neighbour, points, faces, edges = MeshImporter("/path/to/polymesh")
    """

    # Define file paths
    owner_path = os.path.join(polymesh_dir_path, "owner")
    neighbour_path = os.path.join(polymesh_dir_path, "neighbour")
    points_path = os.path.join(polymesh_dir_path, "points")
    faces_path = os.path.join(polymesh_dir_path, "faces")

    # Read owner file
    with open(owner_path, 'r') as file:
        content = file.read()
        match = re.search(r'\d\s*\(([\s\d]+)\)', content)
        numbers_block = match.group(1)
        owner = [int(num) for num in numbers_block.split()]

    # Read neighbour file
    with open(neighbour_path, 'r') as file:
        content = file.read()
        match = re.search(r'\d\s*\(([\s\d]+)\)', content)
        numbers_block = match.group(1)
        neighbour = [int(num) for num in numbers_block.split()]

    # Read points file
    with open(points_path, 'r') as file:
        content = file.read()
        match = re.findall(r'\(([-+]?\d*?\.?\d*?e?[-+]?\d*)\s([-+]?\d*?\.?\d*?e?[-+]?\d*)\s([-+]?\d*?\.?\d*?e?[-+]?\d*)\)', content)
        points = list(map(lambda x: (float(x[0]), float(x[1]), float(x[2])), match))

    # Read faces file
    with open(faces_path, 'r') as file:
        content = file.read()
        match = re.findall(r'\(\d* \d* \d* \d*\)', content)
        faces = list(map(lambda x: tuple(x.replace("(", "").replace(")", "").strip().split(" ")), match))

    if return_edges:
        # Extract edges from faces
        edges_raw = []
        for face in faces:
            for j in range(1, len(face)):
                edges_raw.append((int(face[j-1]), int(face[j])))
            edges_raw.append((int(face[-1]), int(face[0])))
        set_edges = set(tuple(sorted(edge)) for edge in edges_raw)
        edges = list(set_edges)

        return owner, neighbour, points, faces, edges
    else:
        return owner, neighbour, points, faces