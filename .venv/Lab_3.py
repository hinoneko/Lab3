import random
import math
import turtle


def calcAdir(seed, variant):
    random.seed(seed)  # Встановлення генератора випадкових чисел
    n = 10 + variant[3]  # Кількість вершин графа

    matrix = [] # Ініціалізація матриці напрямленого графа
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.uniform(0, 2.0))  # Заповнення елементів матриці випадковими числами
        matrix.append(row)
    k = 1.0 - variant[3] * 0.02 - variant[4] * 0.005 - 0.25  # Обчислення коефіцієнта k

    for i in range(n):
        for j in range(n):
            matrix[i][j] *= k
            matrix[i][j] = math.floor(matrix[i][j])  # Округлення

    return matrix


def calcUndir(matrix, N):
    undir = []  # Ініціалізація матриці ненапрямленого графа
    for i in range(N):
        undir.append([])
        for j in range(N):
            undir[i].append(0)  # Заповнення матриці 0
    # Заповнення матриці ненапрямленого графа
    for i in range(N):
        for j in range(N):
            undir[i][j] = matrix[i][j] or matrix[j][i]
    return undir


# Функція для малювання вершин графа
def circle(x, y):
    t.pencolor(vertice_color)
    t.penup()
    t.goto(x, y - vertices_radius)
    t.pendown()
    t.fillcolor(vertice_color)
    t.begin_fill()
    t.circle(vertices_radius)
    t.end_fill()


# Функція для малювання тексту поруч із вершиною
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
    # Якщо потрібно малювати стрілку, додати стрілку на кінець лінії
    if is_arrow:
        t.setheading(t.towards(second_point_x, second_point_y))
        t.forward(t.distance(second_point_x, second_point_y) - vertices_radius)
        t.stamp()

    t.goto(second_point_x, second_point_y)

    # Повернути нахил курсора у початкову позицію
    if is_arrow:
        t.setheading(0)


# Функція для малювання ламаної лінії
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

# Функція для малювання петлі
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

# Функція для отримання координат вершин розміщених по колу
def get_points_on_circle(radius, num_points, width, height):
    points = []
    angle_increment = 360 / num_points

    for i in range(num_points):
        angle = math.radians(i * angle_increment)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append({'x': x + width / 2, 'y': y + height / 2})

    return points


# Задання параметрів графа
n = {
    1: 3,
    2: 2,
    3: 2,
    4: 1,
}
nJoin = 3221

window_width = 900  # Ширина вікна
window_height = 900  # Висота вікна
vertices_radius = 30  # Радіус кола-вершини
position_radius = 350  # Радіус кола для позиціонування вершин
same_line_gap = 30  # Відстань між лініями, що проведені між двома точками графа, але в різних напрямах
line_thickness = 2  # Товщина ліній
text_color = 'white'  # Колір тексту
line_color = 'black'  # Колір ліній
vertice_color = '#2b4535'  # Колір заповнення кола вершин
vertices = get_points_on_circle(position_radius, 10 + n[3], window_width, window_height)  # визначення координат вершин

Adir = calcAdir(nJoin, n)  # Генерація напрямленого графа
Undir = calcUndir(Adir, 10 + n[3])  # Генерація ненапрямленого графа
is_dir = False  # Прапорець напрямленості

# Вибір типу графа (напрямлений або ненапрямлений)
while True:
    print('Виберіть граф: \n1 - напрямлений \n0 - ненапрямлений')
    choice = input()
    if choice == '1':
        current_matrix = Adir
        is_dir = True
        break
    elif choice == '0':
        current_matrix = Undir
        is_dir == False
        break
    else:
        print('Хибний ввід\n')

# Вивід матриці
print('\nВибрана матриця:')
for row in current_matrix:
    print(row)

# Налаштування вікна малювання
turtle.setup(width=window_width, height=window_height)
turtle.setworldcoordinates(0, 0, window_width, window_height)

t = turtle.Turtle()
t.width(line_thickness)
t.speed(20)

# Малювання ліній з'єднання графа
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
        elif (current_matrix[j][i] != 0 and is_dir):
            kef = 1
            if (current_matrix[i][j] == 2):
                kef = -1
            current_matrix[j][i] = 2

            broke_line(kef, startPointX, startPointY, endPointX, endPointY)
        else:
            line(startPointX, startPointY, endPointX, endPointY, is_dir)


# Малювання вершин графа
for index, point in enumerate(vertices):
    circle(point['x'], point['y'])
    circle_text(point['x'], point['y'], str(index + 1))

turtle.mainloop()  # Запуск головного циклу для збереження вікна
