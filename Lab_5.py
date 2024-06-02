import random
import math
import turtle
import keyboard
import copy


# Функція для генерації напрямленої матриці
def calcAdir(seed, variant):
    random.seed(seed)
    n = 10 + variant[3]

    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.uniform(0, 2.0))
        matrix.append(row)
    k = 1.0 - variant[3] * 0.01 - variant[4] * 0.005 - 0.15

    for i in range(n):
        for j in range(n):
            matrix[i][j] *= k
            matrix[i][j] = math.floor(matrix[i][j])

    return matrix


# Функція для генерації ненапрямленої матриці
def calcUndir(matrix, N):
    undir = []
    for i in range(N):
        undir.append([])
        for j in range(N):
            undir[i].append(0)
    for i in range(N):
        for j in range(N):
            undir[i][j] = matrix[i][j] or matrix[j][i]
    return undir


# Функція для малювання кола
def circle(x, y, color):
    t.pencolor(color)
    t.penup()
    t.goto(x, y - vertices_radius)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(vertices_radius)
    t.end_fill()


# Функція для малювання тексту в колі
def circle_text(x, y, text):
    t.penup()
    t.goto(x, y - 10)
    t.pendown()
    t.color(text_color)
    t.write(text, align="center", font=("Arial", 18, "normal"))


# Функція для малювання лінії
def line(first_point_x, first_point_y, second_point_x, second_point_y, color, is_arrow=False):
    t.pencolor(color)
    t.penup()
    t.goto(first_point_x, first_point_y)
    t.pendown()
    if is_arrow:
        t.setheading(t.towards(second_point_x, second_point_y))
        t.forward(t.distance(second_point_x, second_point_y) - vertices_radius)
        t.stamp()
    t.goto(second_point_x, second_point_y)
    if is_arrow:
        t.setheading(0)


# Функція для малювання ламаної лінії
def broke_line(coeficient, startPointX, startPointY, endPointX, endPointY, color):
    middle_point = {'x': (startPointX + endPointX) / 2, 'y': (startPointY + endPointY) / 2}
    height = same_line_gap * coeficient

    deltaY = endPointY - startPointY
    deltaX = endPointX - startPointX
    if deltaY == 0 or deltaX == 0:
        base_k = 0.000001
    else:
        base_k = deltaY / deltaX

    k = -1 / base_k
    height_angle = math.atan(k)
    ax = math.cos(height_angle) * height
    ay = math.cos(math.pi / 2 - height_angle) * height

    x = ax + middle_point['x']
    y = ay + middle_point['y']

    divide_point = {'x': x, 'y': y}
    line(startPointX, startPointY, divide_point["x"], divide_point["y"], color)
    line(divide_point["x"], divide_point["y"], endPointX, endPointY, color, is_arrow=True)


# Функція для малювання петлі
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


# Функція для отримання точок на колі
def get_points_on_circle(radius, num_points, width, height):
    points = []
    angle_increment = 360 / num_points
    for i in range(num_points):
        angle = math.radians(i * angle_increment)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append({'x': x + width / 2, 'y': y + height / 2})
    return points


# Функція обходу в ширину
def bfs(graph, start, vertices):
    graph = [[1 if cell > 1 else cell for cell in row] for row in graph]
    visited = [False] * len(graph)
    queue = [start]
    visited[start] = True
    bfs_order = []
    bfs_tree_matrix = [[0]*len(graph) for _ in range(len(graph))]
    circle(vertices[start]['x'], vertices[start]['y'], 'dark red')
    circle_text(vertices[start]['x'], vertices[start]['y'], str(start + 1))
    while queue:
        vertex = queue.pop(0)
        bfs_order.append(vertex)
        for i in range(len(graph[vertex])):
            if graph[vertex][i] and not visited[i]:
                keyboard.wait('q')
                startPointX = vertices[vertex]['x']
                startPointY = vertices[vertex]['y']
                endPointX = vertices[i]['x']
                endPointY = vertices[i]['y']
                if graph[i][vertex]:
                    kef = 1
                    if graph[vertex][i] == 2:
                        kef = -1
                    graph[i][vertex] = 2
                    broke_line(kef, startPointX, startPointY, endPointX, endPointY, "dark red")
                else:
                    line(startPointX, startPointY, endPointX, endPointY, "dark red", is_arrow=True)
                queue.append(i)
                visited[i] = True
                circle(vertices[i]['x'], vertices[i]['y'], 'dark red')
                circle_text(startPointX, startPointY, str(vertex + 1))
                circle_text(endPointX, endPointY, str(i + 1))
                bfs_tree_matrix[vertex][i] = 1
    t.color(line_color)
    return bfs_order, bfs_tree_matrix


# Функція допоміжна для обходу в глибину
def dfs_util(graph, vertex, visited, dfs_order, start, vertices, dfs_tree_matrix):
    graph = [[1 if cell > 1 else cell for cell in row] for row in graph]
    visited[vertex] = True
    dfs_order.append(vertex)

    for i in range(len(graph[vertex])):
        if graph[vertex][i] and not visited[i]:
            keyboard.wait('q')
            startPointX = vertices[vertex]['x']
            startPointY = vertices[vertex]['y']
            endPointX = vertices[i]['x']
            endPointY = vertices[i]['y']
            if graph[i][vertex]:
                kef = 1
                if graph[vertex][i] == 2:
                    kef = -1
                graph[i][vertex] = 2
                broke_line(kef, startPointX, startPointY, endPointX, endPointY, "dark blue")
            else:
                line(startPointX, startPointY, endPointX, endPointY, "dark blue", is_arrow=True)
            circle(vertices[i]['x'], vertices[i]['y'], 'dark blue')
            circle_text(startPointX, startPointY, str(vertex + 1))
            circle_text(endPointX, endPointY, str(i + 1))
            dfs_tree_matrix[vertex][i] = 1
            dfs_util(graph, i, visited, dfs_order, start, vertices, dfs_tree_matrix)


# Функція для обходу в глибину
def dfs(graph, start, vertices):
    visited = [False] * len(graph)
    dfs_order = []
    dfs_tree_matrix = [[0]*len(graph) for _ in range(len(graph))]
    circle(vertices[start]['x'], vertices[start]['y'], 'dark blue')
    circle_text(vertices[start]['x'], vertices[start]['y'], str(start + 1))
    dfs_util(graph, start, visited, dfs_order, start, vertices, dfs_tree_matrix)
    return dfs_order, dfs_tree_matrix


# Функція для малювання графа
def draw_graph(vertices, current_matrix, is_dir, line_color):
    for i, row in enumerate(current_matrix):
        for j, value in enumerate(row):
            if not is_dir and i < j:
                continue

            startPointX = vertices[i]['x']
            startPointY = vertices[i]['y']
            endPointX = vertices[j]['x']
            endPointY = vertices[j]['y']

            if value == 0:
                continue

            if i == j:
                angle = (360 / (10 + n[3])) * i
                own_line(startPointX, startPointY, angle, line_color, is_dir)
            elif (current_matrix[j][i] != 0 and is_dir):
                kef = 1
                if (current_matrix[i][j] == 2):
                    kef = -1
                current_matrix[j][i] = 2
                broke_line(kef, startPointX, startPointY, endPointX, endPointY, line_color)
            else:
                line(startPointX, startPointY, endPointX, endPointY, line_color, is_dir)


# Функція для малювання вершин
def draw_vertices(vertices):
    for index, point in enumerate(vertices):
        circle(point['x'], point['y'], vertice_color)
        circle_text(point['x'], point['y'], str(index + 1))


n = {
    1: 3,
    2: 2,
    3: 2,
    4: 1,
}
nJoin = 3221

window_width = 900
window_height = 900
vertices_radius = 30
position_radius = 350
same_line_gap = 30
line_thickness1 = 2
line_thickness2 = 4
text_color = 'white'
line_color = 'black'
vertice_color = '#2b4535'
vertices = get_points_on_circle(position_radius, 10 + n[3], window_width, window_height)

Adir = calcAdir(nJoin, n)
Undir = calcUndir(Adir, 10 + n[3])
is_dir = False

# Зберегти копію початкової матриці
initial_Adir = copy.deepcopy(Adir)

while True:
    print('Виберіть граф: \n1 - напрямлений \n0 - ненапрямлений')
    choice = input()
    if choice == '1':
        current_matrix = Adir
        is_dir = True
        break
    elif choice == '0':
        current_matrix = Undir
        is_dir = False
        break
    else:
        print('Хибний ввід\n')

print('\nВибрана матриця:')
for row in current_matrix:
    print(row)

turtle.setup(width=window_width, height=window_height)
turtle.setworldcoordinates(0, 0, window_width, window_height)

t = turtle.Turtle()
t.width(line_thickness1)
t.speed(20)

draw_graph(vertices, current_matrix, is_dir, line_color)
draw_vertices(vertices)

if current_matrix == Adir:
    t.width(line_thickness2)

    start_vertex = 0
    bfs_result, bfs_tree_matrix = bfs(current_matrix, start_vertex, vertices)
    bfs_result = [x + 1 for x in bfs_result]
    print('\nBFS результат:', bfs_result)
    print('\nМатриця сумiжностi дерева обходу BFS:')
    for row in bfs_tree_matrix:
        print(row)

    keyboard.wait('w')
    t.clear()
    t.width(line_thickness1)
    draw_graph(vertices, initial_Adir, is_dir, line_color)
    draw_vertices(vertices)

    t.width(line_thickness2)

    start_vertex = 0
    dfs_result, dfs_tree_matrix = dfs(current_matrix, start_vertex, vertices)
    dfs_result = [x + 1 for x in dfs_result]
    print('\nDFS результат:', dfs_result)
    print('\nМатриця сумiжностi дерева обходу DFS:')
    for row in dfs_tree_matrix:
        print(row)

turtle.mainloop()
