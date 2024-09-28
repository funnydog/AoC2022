#!/usr/bin/env python3
import math
import sys

class Vector(object):
    def __init__(self, x: int, y: int, z: int, w: int) -> None:
        self.v = [x, y, z, w]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Vector):
            return NotImplemented
        return all(self.v[i] == o.v[i] for i in range(4))

    def __add__(self, o: object) -> object:
        if isinstance(o, Vector):
            return Vector(*map(lambda a, b: a + b, self.v, o.v))
        else:
            return NotImplemented

    def __sub__(self, o: object) -> object:
        if isinstance(o, Vector):
            return Vector(*map(lambda a, b: a - b, self.v, o.v))
        else:
            return NotImplemented

    def __neg__(self) -> "Vector":
        return Vector(*map(lambda a: -a, self.v))

    def __repr__(self) -> str:
        return "(" + ",".join(map(str, self.v)) + ")"

class Matrix(object):
    def __init__(self, iv = None):
        if iv is None:
            iv = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        self.m = iv

    def __matmul__(self, o: object) -> "Matrix":
        if not isinstance(o, Matrix):
            return NotImplemented

        m: list[list[int]] = []
        for i in range(4):
            row: list[int] = []
            for j in range(4):
                s = 0
                for k in range(4):
                    s += self.m[i][k] * o.m[k][j]
                row.append(s)
            m.append(row)
        return Matrix(m)

    def __mul__(self, o: object) -> Vector:
        if not isinstance(o, Vector):
            return NotImplemented
        rv = Vector(0, 0, 0, 0)
        for i in range(4):
            s = 0
            for j in range(4):
                s += self.m[i][j] * o.v[j]
            rv.v[i] = s
        return rv

    def __str__(self) -> str:
        return "\n".join("".join("{:4d}".format(x) for x in row) for row in self.m)

class Face(object):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.points: list[Vector] = [
            Vector(x, y, 0, 1),
            Vector(x+edge, y, 0, 1),
            Vector(x+edge, y+edge, 0, 1),
            Vector(x, y+edge, 0, 1)
        ]
        self.adj: dict[str, tuple[int,int]] = {}

    def to_map(self, x: int, y: int) -> tuple[int,int]:
        return self.x+x, self.y+y

    def __repr__(self) -> str:
        return f"Face<{self.x}, {self.y}>"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.read().splitlines()
    except Exception as e:
        print(f"cannot open {sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    BOARD, PATH = 0, 1
    state = BOARD
    board: list[str] = []
    path = ""
    width, height = 0, 0
    for line in lines:
        if state == BOARD:
            if not line:
                height = len(board)
                state = PATH
            else:
                if width < len(line):
                    width = len(line)
                board.append(line)
        else:
            path = line

    # fix the board by making every row the same width
    for i, row in enumerate(board):
        board[i] = row + " " * (width - len(row))

    # find the length of the edge of the cube
    area = 0
    for row in board:
        for c in row:
            if c != " ":
                area += 1
    edge = int(math.sqrt(area / 6))

    # detect the faces
    faces: list[Face] = []
    for y in range(0, height, edge):
        for x in range(0, width, edge):
            if board[y][x] != " ":
                faces.append(Face(x, y))

    # rotation maps
    cw  = {"U":"R","R":"D","D":"L","L":"U"} # clockwise
    ccw = {"U":"L","R":"U","D":"R","L":"D"} # counterclockwise
    rev = {"U":"D","R":"L","D":"U","L":"R"} # reverse
    movements = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}

    # find the adjacents of each face
    for face in faces:
        for d, (dx, dy) in movements.items():
            x, y = face.x, face.y
            while True:
                y = (y + dy * edge) % height
                x = (x + dx * edge) % width
                if board[y][x] != " ":
                    break
            for i, adj in enumerate(faces):
                if adj.x == x and adj.y == y:
                    # NOTE: go to the face without rotations
                    face.adj[d] = (i, 0)
                    break

    def move_cube(fi, x, y, d, count: int) -> tuple[int,int,int,str]:
        global edge, faces, board, movements

        for _ in range(count):
            # make the movement
            nf, nx, ny, nd = fi, x, y, d
            dx, dy = movements[d]
            nx += dx
            ny += dy

            # should we change the face?
            if nx < 0 or nx >= edge or ny < 0 or ny >= edge:
                nx %= edge
                ny %= edge
                nf, rot = faces[fi].adj[nd]
                for _ in range(rot):
                    nx, ny = edge-1 - ny, nx # coord rotation
                    nd = cw[nd]              # direction rotation

            # break if we hit a dash
            bx, by = faces[nf].to_map(nx, ny)
            if board[by][bx] == "#":
                break
            fi, x, y, d = nf, nx, ny, nd

        return fi, x, y, d

    def get_path_points(path: str) -> int:
        global faces

        # use the local face coordinates (face, x, y)
        fi, x, y, d  = 0, 0, 0, "R"
        path_start = 0
        for i, v in enumerate(path+"E"):
            if not v in "0123456789":
                # move
                count = int(path[path_start:i])
                fi, x, y, d = move_cube(fi, x, y, d, count)

                # rotate
                if v == "R":
                    d = cw[d]
                elif v == "L":
                    d = ccw[d]
                else:
                    break
                path_start = i + 1

        x, y = faces[fi].to_map(x, y)
        return (y + 1) * 1000 + (x + 1) * 4 + "RDLU".index(d)

    print("Part1:", get_path_points(path))

    def translation(v: Vector) -> Matrix:
        r = Matrix()
        for i in range(3):
            r.m[i][3] = v.v[i]
        return r

    def rotation(d: str) -> Matrix:
        r = Matrix()
        if d == "D":            # x axis
            r.m[1][1] = r.m[2][2] = 0
            r.m[1][2] = -1
            r.m[2][1] = 1
            return r
        elif d == "U":          # x axis
            r.m[1][1] = r.m[2][2] = 0
            r.m[1][2] = 1
            r.m[2][1] = -1
            return r
        elif d  == "R":         # y axis
            r.m[0][0] = r.m[2][2] = 0
            r.m[0][2] = -1
            r.m[2][0] = 1
            return r
        elif d  == "L":         # y axis
            r.m[0][0] = r.m[2][2] = 0
            r.m[0][2] = 1
            r.m[2][0] = -1
            return r
        else:
            raise NotImplementedError()

    def rotate_around(d: str, v: Vector) -> Matrix:
        return translation(v) @ rotation(d) @ translation(-v)

    def find_common_edges(faces: list[Face]) -> None:
        # reset the adjacent faces
        for face in faces:
            face.adj.clear()

        # for each couple of faces find the common edges
        for i, a in enumerate(faces):
            for j in range(i):
                b = faces[j]

                # check the edges
                for ei, (a0, a1) in enumerate(((0,1),(1,2),(2,3),(3,0))):
                    for ej, (b0, b1) in enumerate(((0,1),(1,2),(2,3),(3,0))):
                        if a.points[a0] == b.points[b1] and a.points[a1] == b.points[b0]:
                            rot_ba = (ei - ej + 2) % 4
                            rot_ab = (4 - rot_ba) % 4
                            a.adj["URDL"[ei]] = (j, rot_ab)
                            b.adj["URDL"[ej]] = (i, rot_ba)

    find_common_edges(faces)

    # topological sort on adjacent faces to find the order in which to
    # apply the rotations around the edges to fold the net of the cube
    order = []
    visited = [False] * len(faces)
    def dfs(i: int, d: str) -> None:
        global faces, visited, order
        visited[i] = True
        for nd, (ni, _) in faces[i].adj.items():
            if not visited[ni]:
                dfs(ni, rev[nd])
        order.append((d, i))
    dfs(0, "")

    # remove the first face
    order.pop()

    # Fold the net of cube
    processed = [False] * len(faces)
    for d, i in order:
        vector = faces[i].points["URDL".index(d)]

        # rotate the face and its children around the edge
        matrix = rotate_around(d, vector)
        rotated = [False] * len(faces)
        queue = [i]
        while queue:
            j = queue.pop()

            # rotate every point
            faces[j].points = [matrix * p for p in faces[j].points]
            rotated[j] = True

            # rotate any connected child face
            for nj, _ in faces[j].adj.values():
                if not rotated[nj] and processed[nj]:
                    queue.append(nj)

            # mark as processed
            processed[i] = True

    # with the cube now folded find again the common edges of the
    # faces
    find_common_edges(faces)

    print("Part2:", get_path_points(path))
