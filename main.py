import pygame
from random import choice, randint
import os
import sys

from figure import gorisont_shape, cube_shape
from figure import left_s_shape, right_s_shape
from figure import left_g_shape, right_g_shape


WIDTH = 700  # ширина окна
HEIGHT = 650  # высота окна
WIDHT_PLAY = 300  # ширина игрового поля
HEIGHT_PLAY = 600  # высота игрового поля
BLOCK_SIZE = 30  # размер одной клетки
FPS = 50  # значение fps
GRAVITY = 0.1  # значение гравитации

clock = pygame.time.Clock()  # подключение модуля clock
color_for_shape = [(0, 255, 225), (204, 0, 255),
                   (0, 13, 255), (0, 255, 166),
                   (255, 0, 255), (255, 0, 119),
                   (250, 255, 117), (131, 140, 214),
                   (204, 131, 214), (255, 153, 153)]  # цвета для фигур

pygame.init()  # подключение pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # установка размеров окна
pygame.display.set_caption('Cosmos-tetris')  # установка названия игры
all_sprites = pygame.sprite.Group()
screen_rect = (0, 0, WIDTH, HEIGHT)


class Shape:
    '''Класс для хранения данных о фигурах'''
    def __init__(self, x, y, shape_type, color_type):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.color_type = color_type
        self.rotation = 0


def load_image(name, colorkey=None):
    '''Загрузка изображения'''
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:  # удаление фона по необходимости
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Star(pygame.sprite.Sprite):
    stars = [load_image('star.png', -1)]  # добавление данных о звездах
    for elem in (5, 10, 20):
        stars.append(pygame.transform.scale(stars[0], (elem, elem)))

    def __init__(self, position, x_pos, y_pos):
        '''Запись данных о звездах'''
        super().__init__(all_sprites)
        self.image = choice(self.stars)
        self.rect = self.image.get_rect()
        self.speedy = [x_pos, y_pos]
        self.rect.x, self.rect.y = position
        self.gravity = GRAVITY

    def update(self):
        '''Падение звезд'''
        self.speedy[1] += self.gravity
        self.rect.x += self.speedy[0]
        self.rect.y += self.speedy[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()  # удаление звезды при выходе из окна


def start_screen():
    '''Создание первого загрузочного окна'''
    intro_text = ["                ",
                  "                ",
                  "  COSMOS-TETRIS "]  # текст заголовка
    fon = pygame.transform.scale(load_image('space_fon_start.jpg'),
                                 (WIDTH, HEIGHT))  # загрузка изображения фона
    screen.blit(fon, (0, 0))  # добавление фона на экран
    font = pygame.font.Font('18963.ttf', 70)  # параметры текста для заголовка
    text_coord = 50
    for line in intro_text:  # добавление текста на экран
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # параметры первой строки текста для пояснения
    font = pygame.font.Font('18963.ttf', 50)
    # текст и цвет текста
    title_game = font.render("Нажмите в любом", True,
                             pygame.Color(255, 255, 255))
    x = (WIDTH - WIDHT_PLAY) // 2 - WIDHT_PLAY + 150  # координаты для вывода
    y = HEIGHT - HEIGHT_PLAY // 2  # координаты для вывода
    screen.blit(title_game, (x + 50, y - 30))  # вывод текста на экран
    # параметры второй строки текста для пояснения
    font = pygame.font.Font('18963.ttf', 50)
    # текст и цвет текста
    title_game = font.render("месте", True,
                             pygame.Color(255, 255, 255))
    x = (WIDTH - WIDHT_PLAY) // 2 - WIDHT_PLAY + 300  # координаты для вывода
    y = HEIGHT - HEIGHT_PLAY // 2 + 75  # координаты для выбора
    screen.blit(title_game, (x + 50, y - 30))  # вывод текста на экран
    while True:  # основной цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход при нажатии "закрыть"
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # при нажатии в любом месте включается следующее окно
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(dct={}):
    '''генерация уровня'''
    pole = [[(0, 0, 0) for i in range(10)] for j in range(20)]
    for row in range(20):
        for col in range(10):
            if (col, row) in dct:
                # добавление фигуры на поле
                elem = dct[(col, row)]
                pole[row][col] = elem
    return pole


def make_shape():
    '''генерация фигур'''
    global gorisont_shape, cube_shape, left_s_shape
    global right_s_shape, left_g_shape, right_g_shape
    global color_for_shape
    lst_shape = [gorisont_shape, cube_shape, left_s_shape,
                 right_s_shape, left_g_shape, right_g_shape]
    # генерация фигуры случайного вида и случайного цвета
    return Shape(5, 0, choice(lst_shape), choice(color_for_shape))


def make_new_shape(shape, screen):
    '''создание новой фигуры (следующей)'''
    font = pygame.font.Font('18963.ttf', 50)  # выбор шрифта и размера
    title_game = font.render("Далее", True, pygame.Color(255, 255, 255))
    x = (WIDTH - WIDHT_PLAY) // 2 + WIDHT_PLAY  # координата х
    y = HEIGHT - HEIGHT_PLAY // 2 - 150  # координата у
    screen.blit(title_game, (x + 50, y - 50))  # добавление текста на экран
    pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                     (x + 50, y + 20, BLOCK_SIZE * 5 - 25,
                      BLOCK_SIZE * 5))  # добавление поля для рисования фигуры
    pygame.draw.rect(screen, pygame.Color(89, 8, 68),
                     (x + 50, y + 20, BLOCK_SIZE * 5 - 25,
                      BLOCK_SIZE * 5), 5)  # добавление рамки
    form = shape.shape_type[shape.rotation % len(shape.shape_type)]
    for i, i1 in enumerate(form):  # в цикле генерация фигуры
        for j, j1 in enumerate(list(i1)):
            if j1 == '#':
                pygame.draw.rect(screen, shape.color_type,
                                 (x + j * BLOCK_SIZE + 40,
                                  y + i * BLOCK_SIZE + 10,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)


def check_for_pole(now_shape, level):
    '''проверка, чтобы фигура не вышла за поле'''
    form_position = make_shapes_position(now_shape)
    lst = []
    for i in range(20):  # добавление фигуры в список
        pod = []
        for j in range(10):
            if level[i][j] == (0, 0, 0):
                pod.append((j, i))
        lst.append(pod)
    lst1 = []
    for element in lst:
        for elem in element:
            lst1.append(elem)
    for el in form_position:  # проверка на нахождение в поле
        if el not in lst1:
            if el[1] >= 0:
                return False
    return True


def check_for_end_game(lst):
    '''проверка на конец игры'''
    for elem in lst:
        y = elem[1]  # координата у
        if y < 1:  # если фигура затрагивает верхний край поля
            return True
    return False


def make_shapes_position(shape):
    '''генерация списка с позициями фигур'''
    lst = []
    form = shape.shape_type[shape.rotation % len(shape.shape_type)]
    for i, i1 in enumerate(form):
        for j, j1 in enumerate(list(i1)):
            if j1 == '#':  # если в списке стоит знак фигуры
                lst.append((shape.x + j, shape.y + i))  # добавление в список
    for i, el in enumerate(lst):  # генерация на список с позициями
        lst[i] = (el[0] - 2, el[1] - 4)
    return lst


def make_level_for_window(screen, row, col):
    '''рисование уровня на экран'''
    x = (WIDTH - WIDHT_PLAY) // 2  # координата х
    y = HEIGHT - HEIGHT_PLAY - 10  # координата у
    for i in range(row + 1):
        # рисование горизонтальных полос
        pygame.draw.line(screen, (255, 255, 255), (x, y + i * 30),
                         (x + WIDHT_PLAY, y + i * 30))
        for j in range(col + 1):
            # рисование вертикальных полос
            pygame.draw.line(screen, (255, 255, 255), (x + j * 30, y),
                             (x + j * 30, y + HEIGHT_PLAY))


def clear_for_win_row(level, dct):
    '''отчистка строки при заполнении'''
    count = 0  # переменная для количества
    for i in range(len(level) - 1, -1, -1):
        row = level[i]  # строка
        if (0, 0, 0) not in row:  # проверка строки
            count += 1
            flag = i
            for j in range(len(row)):
                try:
                    del dct[(j, i)]  # удаление
                except:
                    continue
    if count > 0:
        for key in sorted(list(dct), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < flag:
                keys = (x, y + count)  # ключ к словарю
                sound_delete.play()  # звуковые эффекты
                dct[keys] = dct.pop(key)  # удаление
    return count


def check_for_set_volue(x, y):
    '''проверка для увеличения/уменьшения громкости звука'''
    if x >= WIDTH - WIDHT_PLAY + 140 and x <= WIDTH - WIDHT_PLAY + 190 \
       and y >= HEIGHT_PLAY - 100 and y <= HEIGHT_PLAY - 50:
        # если нажали на кнопку -
        volue_now = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(volue_now / 2)
    elif x >= WIDTH - WIDHT_PLAY + 210 and x <= WIDTH - WIDHT_PLAY + 260 \
            and y >= HEIGHT_PLAY - 100 and y <= HEIGHT_PLAY - 50:
        # если нажали на кнопку +
        volue_now = pygame.mixer.music.get_volume()
        if volue_now:  # если звук включен
            pygame.mixer.music.set_volume(volue_now * 2)
        else:  # если звук выключен
            pygame.mixer.music.set_volume(0.25)


def past_scores():
    '''возвращает самого большого рекорда'''
    f = open('scores.txt')  # открытие файла
    lst = f.readline()  # чтение текста
    past = lst.rstrip()
    f.close()  # закрытие файла
    return past  # возращение рекорда


def new_scores(scores):
    '''запись нового рекорда'''
    past = int(past_scores())
    if past < scores:  # если новый рекорд больше старого
        f = open('scores.txt', mode='w')  # открытие файла
        f.write(str(scores))  # запись файла
        f.close()  # закрытие файла


def create_star(position):
    '''генерация звезд'''
    star_count = 20  # количество звезд
    number = range(-5, 6)
    for _ in range(star_count):
        Star(position, choice(number), choice(number))  # создание звезды


def draw_mult():
    '''создание экрана при достижении рубежа'''
    screen.fill((0, 0, 0))  # заливка экрана
    cup = load_image('cup.png', -1)  # добавление кубка
    for _ in range(150):  # добавление звезд на экран
        sound_win.play()  # включении музыки
        sound_win.set_volume(1)  # установление громкости
        create_star((randint(10, 650), randint(10, 600)))  # создание звезд
        all_sprites.update()  # обновление спрайтов
        screen.fill((0, 0, 0))
        screen.blit(cup, (200, 200))  # добавление кубка на экран
        all_sprites.draw(screen)
        pygame.display.update()
        pygame.display.flip()  # обновление экрана
        clock.tick(50)  # промежуток во времени
    font = pygame.font.Font('18963.ttf', 85)  # шрифт и размер
    # добавление прямоугольника
    pygame.draw.rect(screen, (255, 255, 255), (40, 280, 620, 110))
    win_text = font.render("Поздравляем!!!", True, pygame.Color(255, 0, 0))
    screen.blit(win_text, (50, 300))  # добавление текста


def draw_end_game():
    font = pygame.font.Font('18963.ttf', 70)  # шрифт и размер
    # рисовать прямоугольник
    pygame.draw.rect(screen, (255, 255, 255), (125, 250, 500, 100))
    if int(scores_now) > int(scores_past):  # если новый рекорд
        text = "Новый рекорд!"
    else:  # если меньше рекорда
        text = "Ты проиграл!"
    end_game = font.render(text, True, pygame.Color(0, 0, 0))
    screen.blit(end_game, (130, 275))  # добавление текста


def terminate():
    '''выход из игры'''
    pygame.mixer.music.pause()  # выключение музыки
    pygame.quit()  # выход
    sys.exit()


pygame.mixer.music.load('music_fon.mp3')  # включение фоновой музыки
pygame.mixer.music.play(-1)  # зацикливание фоновой музыки
# подключение музыки для конца игры
sound_end_game = pygame.mixer.Sound('music_end_game.mp3')
# подключение музыки для удаления ряда
sound_delete = pygame.mixer.Sound('delete_music.mp3')
# подключение музыки для выигрыша в игре
sound_win = pygame.mixer.Sound('end_win.mp3')
image = load_image("cur.png")  # загрузка изображения кубка
x_cur = 0  # для координат курсора
y_cur = 0  # для координат курсора
pygame.mouse.set_visible(False)  # выключение собственного курсора
start_screen()
running = True
global_dct = {}
level = generate_level(global_dct)  # генерация уровня
flag_for_turn = False
now_shape = make_shape()  # фигура сейчас
next_shape = make_shape()  # следующая фигура
time_for_check = 0
time_game = 0
scores_now = 0
scores_past = past_scores()  # прошлый рекорд
while running:  # основной цикл
    velocity = 0.2  # скорость игры
    time_for_check += clock.get_rawtime()  # время игры для проверки
    time_game += clock.get_rawtime()  # время игры
    pole = generate_level(global_dct)  # поле игры
    if time_game / 1000 > 5:  # увеличение скорости со временем
        time_game = 0
        if time_game > 0.12:
            time_game -= 0.005
    if time_for_check / 1000 >= velocity:  # проверка по скорости
        time_for_check = 0
        now_shape.y += 1
        if not(check_for_pole(now_shape, pole)) and now_shape.y > 0:
            now_shape.y -= 1
            flag_for_turn = True
    for event in pygame.event.get():  # цикл событий
            if event.type == pygame.QUIT:  # при выходе
                running = False
            if event.type == pygame.MOUSEMOTION:  # при движении мыши
                x_cur = event.pos[0]  # координата х
                y_cur = event.pos[1]  # координата у
            # при нажатии кнопкой мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверка, где нажали
                check_for_set_volue(event.pos[0], event.pos[1])
            # при нажатии кнопки (для звука)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # если нажали 1
                    # уменьшение звука
                    volue_now = pygame.mixer.music.get_volume()
                    pygame.mixer.music.set_volume(volue_now / 2)
                if event.key == pygame.K_2:  # если нажали 2
                    # увеличение звука
                    volue_now = pygame.mixer.music.get_volume()
                    pygame.mixer.music.set_volume(volue_now * 2)
            # при нажатии кнопки (для движения)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # если нажали вверх
                    # поворот фигуры
                    now_shape.rotation += 1
                    # если не выходит за поле
                    if not(check_for_pole(now_shape, pole)):
                        now_shape.rotation -= 1
                if event.key == pygame.K_DOWN:  # если нажать вниз
                    # более быстрее опускается
                    now_shape.y += 1
                    # если не выходит за поле
                    if not(check_for_pole(now_shape, pole)):
                        now_shape.y -= 1
                if event.key == pygame.K_LEFT:  # при нажатии влево
                    # сдвиг фигуры влево
                    now_shape.x -= 1
                    # если не выходит за поле
                    if not(check_for_pole(now_shape, pole)):
                        now_shape.x += 1
                if event.key == pygame.K_RIGHT:  # при нажатии вправо
                    # сдвиг фигуры вправо
                    now_shape.x += 1
                    # если не выходит за поле
                    if not(check_for_pole(now_shape, pole)):
                        now_shape.x -= 1
    position = make_shapes_position(now_shape)  # позиция фигуры
    for i in range(len(position)):
        x, y = position[i]
        if y > -1:
            pole[y][x] = now_shape.color_type
    if flag_for_turn:  # если работает флаг
        for elem in position:
            el = (elem[0], elem[1])
            global_dct[el] = now_shape.color_type
        now_shape = next_shape  # "будущая" фигура становится "настоящей"
        next_shape = make_shape()  # генерация новой следующей фигуры
        flag_for_turn = False  # выключение флага
        # увеличение очков
        scores_now += clear_for_win_row(pole, global_dct) * 10
    # изображение фона
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))  # добавление фона на экран
    font = pygame.font.Font('18963.ttf', 45)  # шрифт и размер шрифта
    scores_game = font.render('Cчёт: ', True, pygame.Color(255, 255, 255))
    # добавление текста на экран
    screen.blit(scores_game, (WIDTH - WIDHT_PLAY - 350,
                              (HEIGHT - HEIGHT_PLAY) // 2 + 60))
    scores_game_number = font.render(str(scores_now), True,
                                     pygame.Color(255, 255, 255))
    # добавление текста на экран
    screen.blit(scores_game_number, (50, (HEIGHT - HEIGHT_PLAY) // 2 + 120))
    record_scores_game = font.render('Рекорд: ', True,
                                     pygame.Color(255, 255, 255))
    # добавление текста на экран
    screen.blit(record_scores_game, (WIDTH - WIDHT_PLAY - 380,
                                     HEIGHT - HEIGHT_PLAY + 260))
    record_scores_number = font.render(scores_past, True,
                                       pygame.Color(255, 255, 255))
    # добавление текста на экран
    screen.blit(record_scores_number, (50, HEIGHT - HEIGHT_PLAY + 320))
    for i in range(len(pole)):  # цикл рисования фигуры
        for j in range(len(pole[i])):
            pygame.draw.rect(screen, pole[i][j],
                             ((WIDTH - WIDHT_PLAY) // 2 + j * BLOCK_SIZE,
                              HEIGHT - HEIGHT_PLAY + i * BLOCK_SIZE - 10,
                              BLOCK_SIZE, BLOCK_SIZE), 0)
    make_level_for_window(screen, 20, 10)  # рисование уровня
    # прямоугольник для поля
    pygame.draw.rect(screen, (89, 8, 68),
                     ((WIDTH - WIDHT_PLAY) // 2, HEIGHT - HEIGHT_PLAY - 10,
                      WIDHT_PLAY, HEIGHT_PLAY + 2), 5)
    make_new_shape(next_shape, screen)  # рисование следующей фигуры
    if scores_now >= 1000:  # если набран по очкам порог
        pygame.mixer.music.pause()  # остановка фоновой музыки
        sound_win.play()  # включение музыки для нового окна
        draw_mult()  # включение нового окна
        pygame.display.update()
        pygame.time.delay(3500)
        running = False
        new_scores(scores_now)  # обновление рекорда
    if check_for_end_game(global_dct):  # проверка на окончание игры
        draw_end_game()  # включение таблички конца игры
        pygame.mixer.music.pause()  # пауза фоновой музыки
        sound_end_game.play()  # включение музыки конца игры
        pygame.display.update()  # обновление экрана
        pygame.time.delay(3000)
        running = False
        new_scores(scores_now)  # обновление рекорда
    font = pygame.font.Font('18963.ttf', 30)  # шрифт и размер
    scores_game = font.render('Звук', True, pygame.Color(255, 255, 255))
    # добавление текста на экран
    screen.blit(scores_game, (WIDTH - WIDHT_PLAY + 160,
                              HEIGHT_PLAY - 140))
    # добавление кнопок + и -
    pygame.draw.rect(screen, (150, 245, 255),
                     (WIDTH - WIDHT_PLAY + 140, HEIGHT_PLAY - 100, 50, 50))
    pygame.draw.rect(screen, (0, 100, 115),
                     (WIDTH - WIDHT_PLAY + 140, HEIGHT_PLAY - 100, 50, 50), 5)
    pygame.draw.line(screen, (0, 100, 115),
                     (WIDTH - WIDHT_PLAY + 150, HEIGHT_PLAY - 75),
                     (WIDTH - WIDHT_PLAY + 180, HEIGHT_PLAY - 75), 10)
    pygame.draw.rect(screen, (150, 245, 255),
                     (WIDTH - WIDHT_PLAY + 210, HEIGHT_PLAY - 100, 50, 50))
    pygame.draw.rect(screen, (0, 100, 115),
                     (WIDTH - WIDHT_PLAY + 210, HEIGHT_PLAY - 100, 50, 50), 5)
    pygame.draw.line(screen, (0, 100, 115),
                     (WIDTH - WIDHT_PLAY + 220, HEIGHT_PLAY - 75),
                     (WIDTH - WIDHT_PLAY + 250, HEIGHT_PLAY - 75), 10)
    pygame.draw.line(screen, (0, 100, 115),
                     (WIDTH - WIDHT_PLAY + 235, HEIGHT_PLAY - 90),
                     (WIDTH - WIDHT_PLAY + 235, HEIGHT_PLAY - 60), 10)
    if pygame.mouse.get_focused():  # если курсор находится в пределах окна
        screen.blit(image, [x_cur, y_cur])  # рисование собственного курсора
    pygame.display.update()  # обновление
    pygame.display.flip()
    clock.tick(FPS)
terminate()  # выключение игры
