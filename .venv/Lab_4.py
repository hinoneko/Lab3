import random
import math
import turtle
import time

def multiMatrix(matrix1, matrix2):
    result = [[0 for _ in range(len(matrix1))] for _ in range(len(matrix2))]
    for i in range(len(matrix1)):
        for j in range(len(matrix1)):
            for k in range(len(matrix1)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    return result

def paths2(matrix):
    pow_matrix = multiMatrix(matrix, matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if pow_matrix[i][j]:
                for k in range(len(matrix)):
                    if matrix[i][k] and matrix[k][j]:
                        print(f"{i + 1} -> {k + 1} -> {j + 1}; ", end="\n")

def paths3(matrix):
    pow_matrix = multiMatrix(matrix, matrix)
    pow_matrix2 = multiMatrix(pow_matrix, matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if pow_matrix2[i][j]:
                for k in range(len(matrix)):
                    for m in range(len(matrix)):
                        if matrix[i][k] and matrix[k][m] and matrix[m][j]:
                            print(f"{i + 1} -> {k + 1} -> {m + 1} -> {j + 1}; ", end="\n")

def calculate_out_degrees(matrix):
    out_degrees = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                out_degrees[i] += 1
    return out_degrees

def calculate_in_degrees(matrix):
    in_degrees = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                in_degrees[j] += 1
    return in_degrees

def calculate_total_degrees(matrix, is_directed=True):
    total_degrees = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                total_degrees[i] += 1
                if is_directed:
                    total_degrees[j] += 1
                elif i == j:
                    total_degrees[i] += 1
    return total_degrees

# Перевірка, чи є граф регулярним
def check_regular(graph):
    degrees = calculate_total_degrees(graph)
    is_regular = all(degrees[0] == d for d in degrees)
    if is_regular:
        return True, degrees[0]
    else:
        return False, None

def verHanging(degree):
    hanging_vertices = []
    for i in range(len(degree)):
        if degree[i] == 1:
            hanging_vertices.append(i)
    return hanging_vertices

def verIsolated(degree):
    isolated_vertices = []
    for i in range(len(degree)):
        if degree[i] == 0:
            isolated_vertices.append(i)
    return isolated_vertices

# Генерування напрямленої матриці суміжності
def calcAdir(seed, variant, k):
    random.seed(seed)
    n = 10 + variant[3]

    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.uniform(0, 2.0))
        matrix.append(row)

    for i in range(n):
        for j in range(n):
            matrix[i][j] *= k
            matrix[i][j] = math.floor(matrix[i][j])  # Округлення

    return matrix

# Перетворення напрямленої матриці у ненапрямлену
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

# Функція для малювання вершини
def circle(x, y):
    t.pencolor(vertice_color)
    t.penup()
    t.goto(x, y - vertices_radius)
    t.pendown()
    t.fillcolor(vertice_color)
    t.begin_fill()
    t.circle(vertices_radius)
    t.end_fill()

# Функція для малювання тексту на вершині
def circle_text(x, y, text):
    t.penup()
    t.goto(x, y - 10)
    t.pendown()
    t.color(text_color)
    t.write(text, align="center", font=("Arial", 18, "normal"))

# Функція для малювання лінії між вершинами
def line(first_point_x, first_point_y, second_point_x, second_point_y, is_arrow=False):
    t.penup()
    t.goto(first_point_x, first_point_y)
    t.pendown()
    t.color(line_color)
    if is_arrow:
        t.setheading(t.towards(second_point_x, second_point_y))
        t.forward(t.distance(second_point_x, second_point_y) - vertices_radius)
        t.stamp()

    t.goto(second_point_x, second_point_y)
    if is_arrow:
        t.setheading(0)

# Функція для малювання перерваної лінії між вершинами
def broke_line(coeficient, startPointX, startPointY, endPointX, endPointY):
    middle_point = {
        'x': (startPointX + endPointX) / 2,
        'y': (startPointY + endPointY) / 2
    }
    height = same_line_gap * coeficient

    deltaY = endPointY - startPointY
    deltaX = endPointX - startPointX
    if (deltaY == 0 or deltaX == 0):
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

    line(startPointX, startPointY, divide_point["x"], divide_point["y"])
    line(divide_point["x"], divide_point["y"], endPointX, endPointY, is_dir)

# Функція для малювання петлі на вершині
def own_line(x, y, angle, is_arrow):
    t.up()
    t.goto(x, y)
    t.down()
    t.setheading(angle - 90)
    t.circle(35, 310)
    if is_arrow:
        t.stamp()
    else:
        t.setheading(0)

# Генерування координат точок на колі
def get_points_on_circle(radius, num_points, width, height):
    points = []
    angle_increment = 360 / num_points

    for i in range(num_points):
        angle = math.radians(i * angle_increment)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append({'x': x + width / 2, 'y': y + height / 2})

    return points

# Знаходження транзитивного замикання графу
def transClosure(matrix):
    n = len(matrix)
    closure = [[matrix[i][j] for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i][j] |= closure[i][k] and closure[k][j]
    return closure

def transMatrix(matrix):
    transposed = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            row.append(matrix[j][i])
        transposed.append(row)
    return transposed


def elemenProduct(matrix1, matrix2):
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] * matrix2[i][j])
        result.append(row)
    return result

def strong_components(matrix):

    def dfs(vertex):
        nonlocal component
        visited[vertex] = True
        component.append(vertex)
        for neighbor in range(1, len(matrix)+1):
            if matrix[vertex-1][neighbor-1] == 1 and not visited[neighbor]:
                dfs(neighbor)

    visited = [False] * (len(matrix)+1)
    components = []
    for vertex in range(1, len(matrix) + 1):
        if not visited[vertex]:
            component = []
            dfs(vertex)
            components.append(component)
    return components

def condensation_matrix(matrix, components):
    num_vertices = len(components)
    condensation_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    # Створюємо словник для швидкого доступу до індексів вершин у компоненті
    vertex_index = {}
    for index, component in enumerate(components):
        for vertex in component:
            vertex_index[vertex] = index

    # Заповнюємо матрицю конденсації
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                index_com_i = vertex_index[i + 1]
                index_com_j = vertex_index[j + 1]
                if index_com_i != index_com_j:
                    condensation_matrix[index_com_i][index_com_j] = 1

    return condensation_matrix

# Основна частина програми
n = {
    1: 3,
    2: 2,
    3: 2,
    4: 1,
}
nJoin = 3221

k1 = 1.0 - n[3] * 0.01 - n[4] * 0.01 - 0.3
k2 = 1.0 - n[3] * 0.005 - n[4] * 0.005 - 0.27

window_width = 900
window_height = 900
vertices_radius = 30
position_radius = 350
same_line_gap = 30
line_thickness = 2
text_color = 'white'
line_color = 'black'
vertice_color = '#2b4535'
vertices = get_points_on_circle(position_radius, 10 + n[3], window_width, window_height)
screen = turtle.Screen()

Adir = calcAdir(nJoin, n, k1)
Adir2 = calcAdir(nJoin, n, k2)
Undir = calcUndir(Adir, 10 + n[3])
is_dir = False

while True:
    print('Виберіть граф: \n1 - напрямлений \n0 - ненапрямлений \n2 - модифікований')
    choice = input()
    if choice == '1':
        current_matrix = Adir
        is_dir = True
        break
    elif choice == '0':
        current_matrix = Undir
        is_dir = False
        break
    elif choice == '2':
        current_matrix = Adir2
        is_dir = True
        break
    else:
        print('Хибний ввід\n')

print('\nВибрана матриця:')
for row in current_matrix:
    print(row)

out_degree, in_degree, total_degree = calculate_out_degrees(current_matrix), calculate_in_degrees(current_matrix), calculate_total_degrees(current_matrix, is_dir)
if is_dir:
    print("\nСтепені виходу:", out_degree, "\nСтепені заходу:", in_degree, "\nСтепені:", total_degree)
else:
    print("\nСтепені:", total_degree)

regular, degree = check_regular(current_matrix)
if regular:
    print("\nГраф є регулярним ступеня", degree)
else:
    print("\nГраф не є регулярним")

hanging_vertices, isolated_vertices = verHanging(total_degree), verIsolated(total_degree)
print("\nВисячі вершини:", hanging_vertices)
print("Ізольовані вершини:", isolated_vertices)

turtle.setup(width=window_width, height=window_height)
turtle.setworldcoordinates(0, 0, window_width, window_height)

t = turtle.Turtle()
t.width(line_thickness)
t.speed(200)

if current_matrix == Adir2:
    print("\nШляхи довжиною 2:")
    paths2(Adir2)

    print("\nШляхи довжиною 3:")
    paths3(Adir2)

    matrix_closure = transClosure(Adir2)

    print('\nМатриця досяжності:')
    for row in matrix_closure:
        print(row)

    strongMatrix = elemenProduct(matrix_closure, transMatrix(matrix_closure))
    print("\nМатриця сильної зв'язності:")
    for row in strongMatrix:
        print(row)

    components = strong_components(strongMatrix)

    print("\nКомпоненти сильної зв'язності:")
    for i, component in enumerate(components):
        print(f"Компонента {i + 1}: {component}")

    condensation_adjacency_matrix = condensation_matrix(Adir2, components)
    print("Матриця суміжності графа конденсації:")
    for row in condensation_adjacency_matrix:
        print(row)

for i, row in enumerate(current_matrix):
    for j, value in enumerate(row):
        if (not is_dir and i < j): continue

        startPointX = vertices[i]['x']
        startPointY = vertices[i]['y']
        endPointX = vertices[j]['x']
        endPointY = vertices[j]['y']

        if value == 0:
            continue

        if i == j:
            angle = (360 / (10 + n[3])) * i
            own_line(startPointX, startPointY, angle, is_dir)
        else:
            if (current_matrix[j][i] != 0 and is_dir):
                kef = 1
                if (current_matrix[i][j] == 2):
                    kef = -1
                current_matrix[j][i] = 2

                broke_line(kef, startPointX, startPointY, endPointX, endPointY)
            else:
                line(startPointX, startPointY, endPointX, endPointY, is_dir)

for index, point in enumerate(vertices):
    circle(point['x'], point['y'])
    circle_text(point['x'], point['y'], str(index + 1))

if current_matrix == Adir2:
    vertices2 = get_points_on_circle(position_radius, len(condensation_adjacency_matrix), window_width, window_height)
    time.sleep(5)
    screen.clear()
    for i, row in enumerate(condensation_adjacency_matrix):
        for j, value in enumerate(row):

            startPointX = vertices2[i]['x']
            startPointY = vertices2[i]['y']
            endPointX = vertices2[j]['x']
            endPointY = vertices2[j]['y']

            if value == 1:
                line(startPointX, startPointY, endPointX, endPointY, is_dir)

            for index, point in enumerate(vertices2):
                circle(point['x'], point['y'])
                circle_text(point['x'], point['y'], str(index + 1))

turtle.mainloop()
