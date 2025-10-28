class point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def readfaces(faces):
    usable_faces = []
    for face in faces:
        usable_vertex = []
        for vertex in face:
            split_vertex = vertex.split("/")
            usable_vertex.append(int(split_vertex[0])) # must be int cuz we index list with this
        usable_faces.append(usable_vertex)
    return usable_faces

def readvertex(vertexes):
    usable_vertexes = []
    for vertex in vertexes:
        point = point3d(float(vertex[0]), float(vertex[1]), float(vertex[2]))
        usable_vertexes.append(point)
    return usable_vertexes

def readobj(path):
    v, f = [], []
    with open(path, 'r') as file:
        data = file.readlines()
        for line in data:
            if line.startswith('v '):
                v.append(line[1:-1].split()) #[1:-1].split() cleans up the line so its easier to manipulate
            elif line.startswith('f '):
                f.append(line[1:-1].split())
    return readvertex(v), readfaces(f)