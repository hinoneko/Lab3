import random
import math
import turtle
import keyboard
from queue import PriorityQueue
import copy

seed_value = 3221

# Клас вузла для зв'язаного списку
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


# Клас зв'язаного списку
class LinkedList:
    def __init__(self):
        self.head = None

    # Додає новий вузол до зв'язаного списку
    def add_node(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Ітератор для обходу зв'язаного списку
    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next


# Клас ребра для графу
class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight


# Клас графу
class Graph:
    def __init__(self):
        self.vertices = LinkedList()
        self.edges = LinkedList()

    # Додає вершину до графу
    def add_vertex(self, vertex):
        for v in self.vertices:
            if v == vertex:
                return
        self.vertices.add_node(vertex)

    # Додає ребро до графу
    def add_edge(self, src, dest, weight):
        self.add_vertex(src)
        self.add_vertex(dest)
        self.edges.add_node(Edge(src, dest, weight))

    # Повертає список унікальних ребер графу
    def get_edges(self):
        edges = []
        seen_edges = set()
        for edge in self.edges:
            if (edge.src, edge.dest) not in seen_edges and (edge.dest, edge.src) not in seen_edges:
                edges.append((edge.src, edge.dest, edge.weight))
                seen_edges.add((edge.src, edge.dest))
        return edges


# Генерує матрицю суміжності для неорієнтованого графу з випадковими вагами
def calc_undir(seed, variant):
    random.seed(seed)
    n = 10 + variant[3]
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.uniform(0, 2.0))
        matrix.append(row)
    k = 1.0 - variant[3] * 0.01 - variant[2] * 0.005 - 0.05
    for i in range(n):
        for j in range(n):
            matrix[i][j] *= k
            matrix[i][j] = 0 if matrix[i][j] < 1.0 else 1
    for i in range(n):
        for j in range(i + 1, n):
            matrix[j][i] = matrix[i][j]
    return matrix


# Створює матрицю B з випадковими значеннями
def create_matrix_B(n):
    matrix_B = []
    random.seed(3212)
    for i in range(n):
        m = []
        for j in range(n):
            m.append(random.uniform(0, 2.0))  # Випадкове значення для матриці B
        matrix_B.append(m)
    return matrix_B


# Створює матрицю C на основі матриць B та undir_matrix
def create_matrix_C(n, matrix_B, undir_matrix):
    matrix_C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix_C[i][j] = math.ceil(matrix_B[i][j] * 100 * undir_matrix[i][j])  # Обчислення значень матриці C
    return matrix_C


# Створює матрицю D, де кожен елемент 1, якщо відповідний елемент у матриці C не дорівнює 0
def create_matrix_D(n, matrix_C):
    matrix_D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix_D[i][j] = 1 if matrix_C[i][j] != 0 else 0  # Перетворення значень матриці C в бінарну форму
    return matrix_D


# Створює матрицю H, що вказує на асиметричні елементи в матриці D
def create_matrix_H(n, matrix_D):
    matrix_H = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix_D[i][j] != matrix_D[j][i]:
                matrix_H[i][j] = 1  # Відзначення асиметричних елементів
    return matrix_H


# Створює верхню трикутну матрицю Tr
def create_matrix_Tr(n):
    matrix_Tr = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            matrix_Tr[i][j] = 1  # Відзначення верхніх трикутних елементів
    return matrix_Tr


# Створює матрицю W, об'єднуючи матриці D, H, Tr і C
def create_matrix_W(n, matrix_D, matrix_H, matrix_Tr, matrix_C):
    matrix_W = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            matrix_W[i][j] = (matrix_D[i][j] + matrix_H[i][j] * matrix_Tr[i][j]) * matrix_C[i][j]
            matrix_W[j][i] = matrix_W[i][j]  # Симетричне заповнення матриці W
    return matrix_W


# Розраховує позиції точок на колі для розміщення вершин графу
def get_points_on_circle(radius, num_points, width, height):
    points = []
    angle_increment = 360 / num_points
    for i in range(num_points):
        angle = math.radians(i * angle_increment)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append({'x': x + width / 2, 'y': y + height / 2})
    return points


# Малює коло у вказаній позиції з заданим кольором
def circle(x, y, color):
    t.pencolor(color)
    t.penup()
    t.goto(x, y - vertices_radius)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(vertices_radius)
    t.end_fill()


# Виводить текст всередині кола у вказаній позиції
def circle_text(x, y, text):
    t.penup()
    t.goto(x, y - 10)
    t.pendown()
    t.color(text_color)
    t.write(text, align="center", font=("Arial", 18, "normal"))


# Малює лінію між двома точками з заданим кольором і вагою
def line(first_point_x, first_point_y, second_point_x, second_point_y, color, weight, weight_color):
    t.pencolor(color)
    t.penup()
    t.goto(first_point_x, first_point_y)
    t.pendown()
    t.goto(second_point_x, second_point_y)
    draw_weight(first_point_x, first_point_y, second_point_x, second_point_y, weight, weight_color)


# Малює вагу ребра в середині лінії
def draw_weight(x1, y1, x2, y2, weight, weight_color):
    mid_x = x1 + (x2 - x1) * 0.50
    mid_y = y1 + (y2 - y1) * 0.50
    t.penup()
    t.goto(mid_x, mid_y)
    t.pendown()
    t.color(weight_color)
    t.write(str(weight), align="center", font=("Arial", 12, "normal"))


# Малює петлю (циклічне ребро) у заданій позиції
def own_line(x, y, angle, color, is_arrow):
    t.pencolor(color)
    t.up()
    t.goto(x, y)
    t.down()
    t.setheading(angle - 90)
    t.circle(35, 310)
    if is_arrow:
        t.stamp()
    else:
        t.setheading(0)


# Малює весь граф, використовуючи позиції вершин та матрицю суміжності
def draw_graph(vertices, current_matrix, line_color):
    visited_edges = set()  # Відстеження відвіданих ребер
    for i, row in enumerate(current_matrix):
        for j, value in enumerate(row):
            if value == 0 or (j, i) in visited_edges:
                continue

            startPointX = vertices[i]['x']
            startPointY = vertices[i]['y']
            endPointX = vertices[j]['x']
            endPointY = vertices[j]['y']

            if i == j:
                angle = (360 / len(vertices)) * i
                own_line(startPointX, startPointY, angle, line_color, False)
            else:
                line(startPointX, startPointY, endPointX, endPointY, line_color, value, weight_color)

            visited_edges.add((i, j))  # Додавання ребра до відвіданих


# Малює MST крок за кроком
def draw_graph_step(vertices, edges, step, color):
    if step < len(edges):
        u, v, w = edges[step]
        startPointX = vertices[u]['x']
        startPointY = vertices[u]['y']
        endPointX = vertices[v]['x']
        endPointY = vertices[v]['y']
        line(startPointX, startPointY, endPointX, endPointY, color, w, mst_weight_color)
        circle(vertices[u]['x'], vertices[u]['y'], mst_color)
        circle_text(startPointX, startPointY, str(u + 1))
        circle(vertices[v]['x'], vertices[v]['y'], mst_color)
        circle_text(endPointX, endPointY, str(v + 1))
        step += 1
    return step


# Малює вершини графу
def draw_vertices(vertices):
    for index, point in enumerate(vertices):
        circle(point['x'], point['y'], vertice_color)
        circle_text(point['x'], point['y'], str(index + 1))


# Реалізація алгоритму Пріма для пошуку MST
def prim(graph):
    n = len(list(graph.vertices))
    selected = [False] * n
    pq = PriorityQueue()
    pq.put((0, 0, 0))
    result = []
    total_cost = 0
    skipped_edges = []

    while not pq.empty():
        weight, u, v = pq.get()
        if selected[v]:
            skipped_edges.append((u, v, weight))
            continue

        selected[v] = True
        if u != v:
            result.append((u, v, weight))
            total_cost += weight
            print(f"\nEdge ({u + 1}, {v + 1}), weight {weight} \nAdded \nNot forming a cycle \nEdge number: {len(result)}")

        for edge in graph.edges:
            if edge.src == v and not selected[edge.dest]:
                pq.put((edge.weight, v, edge.dest))

    vertices_in_mst = sorted({u + 1 for u, v, w in result} | {v + 1 for u, v, w in result})
    print(f"\nVertices in MST: {vertices_in_mst}")
    print("\nEdges in MST:")
    for edge in result:
        u, v, w = edge
        print(f"({u + 1}, {v + 1}), weight {w}")

    print("\nSkipped Edges (not in MST):")
    for edge in skipped_edges:
        u, v, w = edge
        print(f"({u + 1}, {v + 1}), weight {w} -> forms a cycle or already selected")

    print(f"\nTotal weight of MST: {total_cost}")

    return result, skipped_edges, total_cost


variant = {
    1: 3,
    2: 2,
    3: 2,
    4: 1,
}

random.seed(seed_value)
nJoin = seed_value

window_width = 900
window_height = 900
vertices_radius = 30
position_radius = 350
line_thickness1 = 2
line_thickness2 = 4
text_color = 'white'
weight_color = 'red'
line_color = 'black'
mst_color = 'dark blue'
mst_weight_color = 'dark blue'
vertice_color = '#2b4535'
vertices = get_points_on_circle(position_radius, 10 + variant[3], window_width, window_height)

Undir = calc_undir(nJoin, variant)
n = 10 + variant[3]
matrix_B = create_matrix_B(n)
matrix_C = create_matrix_C(n, matrix_B, Undir)
matrix_D = create_matrix_D(n, matrix_C)
matrix_H = create_matrix_H(n, matrix_D)
matrix_Tr = create_matrix_Tr(n)
W = create_matrix_W(n, matrix_D, matrix_H, matrix_Tr, matrix_C)

original_W = copy.deepcopy(W)

print('\nAdjacency matrix:')
for row in Undir:
    print(row)

print('\nAdjacency matrix (weights):')
for row in W:
    print(row)

graph = Graph()
for i in range(n):
    for j in range(n):
        if W[i][j] != 0:
            graph.add_edge(i, j, W[i][j])

# Обчислення MST і його ваги
mst_edges, skipped_edges, total_weight = prim(graph)

turtle.setup(width=window_width, height=window_height)
turtle.setworldcoordinates(0, 0, window_width, window_height)

t = turtle.Turtle()
t.width(line_thickness1)
t.speed(0)

draw_graph(vertices, W, line_color)
draw_vertices(vertices)

step_mst = 0

# Функція для відображення наступного кроку побудови MST
def draw_step_mst():
    t.width(line_thickness2)
    global step_mst
    step_mst = draw_graph_step(vertices, mst_edges, step_mst, mst_color)

keyboard.add_hotkey('m', draw_step_mst)
print("\nPress 'm' to draw the next step of the MST edges.")

turtle.mainloop()
