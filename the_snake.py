"""Змейка — игра, в которой игрок управляет змейкой."""

from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # 32 cells
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # 24 cells

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Список возможных направлений
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет по-умолчанию
DEFAULT_COLOR = (0, 0, 0)

# Позиция по-умолчанию
DEFAULT_X_POSITION = 0
DEFAULT_Y_POSITION = 0
DEFAULT_POSITION = (DEFAULT_X_POSITION, DEFAULT_Y_POSITION)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс для игрового объекта.

    Атрибуты:
    - position (tuple): позиция объекта на плоскости в формате (x, y).
    - body_color (tuple): цвет объекта в формате (R, G, B).

    Методы:
    - __init__(): инициализирует новый экземпляр игрового объекта.
    - draw(): метод для отрисовки объекта. По умолчанию ничего не делает.
    """

    def __init__(self):
        """Инициализирует новый экземпляр игрового объекта."""
        self.position = DEFAULT_POSITION
        self.body_color = DEFAULT_COLOR

    def draw(self):
        """Метод для отрисовки объекта. По умолчанию ничего не делает."""

    def _draw_cell(self, pos: tuple[int, int], color: tuple[int, int, int]):
        position_x, position_y = pos
        left = position_x * GRID_SIZE
        top = position_y * GRID_SIZE
        rect = pg.Rect(left, top, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс для представления змейки в игре.

    Наследуется от класса GameObject.

    Атрибуты:
    - start_position (tuple): начальная позиция змейки.
    - body_color (tuple): цвет тела змейки.
    - position (list): текущая позиция змейки.
    - positions (list): список позиций сегментов змейки.
    - direction (tuple): текущее направление движения змейки.
    - next_direction (tuple): следующее направление движения змейки.
    - grow_on_next_move (bool): флаг, указывающий на необходимость
      роста змейки при следующем движении.

    Методы:
    - __init__(): инициализирует новый экземпляр змейки
      c заданными параметрами.
    - draw(): рисует змейки на экране.
    - grow(): устанавливает флаг для роста змейки при следующем движении.
    - reset(): сбрасывает состояние змейки к начальному.
    - move(): перемещает змейку в соответствии c текущим направлением движения.
    - get_head_position(): возвращает позицию головы змейки.
    - collision_detected(): проверяет наличие столкновения змейки c
      собственным хвостом.
    - update_direction(): обновляет направление движения змейки.
    """

    def __init__(self, start_pos_x=0, start_pos_y=0, body_color=SNAKE_COLOR):
        """Инициализирует новый экземпляр змейки c заданными параметрами."""
        super().__init__()
        start_position = (start_pos_x, start_pos_y)
        self.position = start_position

        # Мы храним стартовую позицию змейки потому, что она используется далее
        # в методе reset()
        self.start_position = start_position
        self.body_color = body_color
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow_on_next_move = False

    def draw(self):
        """Рисует змейки на экране."""
        for position in self.positions:
            self._draw_cell(position, color=self.body_color)

    def grow(self):
        """Устанавливает флаг для роста змейки при следующем движении."""
        self.grow_on_next_move = True

    def reset(self):
        """Сбрасывает состояние змейки к начальному."""
        self.position = self.start_position
        self.positions = [self.start_position]

        random_direction_index = randint(0, len(DIRECTIONS) - 1)
        self.direction = DIRECTIONS[random_direction_index]

        self.next_direction = None
        self.grow_on_next_move = False

    def move(self):
        """Перемещает змейку в соответствии c текущим направлением движения."""
        head_x, head_y = self.get_head_position()
        new_x = (head_x + self.direction[0]) % GRID_WIDTH
        new_y = (head_y + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if not self.grow_on_next_move:
            self.positions.pop()
        else:
            self.grow_on_next_move = False

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def collision_detected(self):
        """Проверяет наличие столкновения змейки c собственным хвостом."""
        if len(self.positions) == 1:
            return False
        head_position = self.get_head_position()
        tail_positions = self.positions[1:]
        return head_position in tail_positions

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple(GameObject):
    """
    Класс для представления яблока в игре.

    Наследуется от класса GameObject.

    Атрибуты:
    - position (tuple): текущая позиция яблока на игровом поле.
    - body_color (tuple): цвет яблока.

    Методы:
    - __init__(): инициализирует новый экземпляр яблока c заданным цветом
      и случайным расположением на поле.
    - randomize_position(): устанавливает случайную позицию яблока на поле.
    - draw(): рисует яблоко на экране.
    """

    def __init__(self, color=APPLE_COLOR, restricted_cells=None):
        """Инициализирует новый экземпляр яблока."""
        super().__init__()
        self.body_color = color
        if restricted_cells is None:
            restricted_cells = []
        self.randomize_position(restricted_cells)

    def randomize_position(self, restricted_cells: list[tuple[int, int]]):
        """Устанавливает случайную позицию яблока на игровом поле."""
        self.position = self._get_random_position(restricted_cells)

    def _get_random_position(self, restricted_cells: list[tuple[int, int]]):
        """Устанавливает случайную позицию яблока на игровом поле."""
        while True:
            x = randint(0, GRID_WIDTH - 1)
            y = randint(0, GRID_HEIGHT - 1)
            position = (x, y)
            if position not in restricted_cells:
                return position

    def draw(self):
        """Рисует яблоко на экране."""
        self._draw_cell(self.position, self.body_color)


def handle_keys(game_object):
    """
    Обрабатывает события клавиатуры и направление движения game_object.

    Параметры:
    - game_object: объект, направление движения которого нужно изменить.

    Поведение:

    - При нажатии на клавиши co стрелками изменяет
      next_direction объекта game_object,
      учитывая текущее направление,
      чтобы предотвратить движение в обратную сторону.
    - Если пользователь закрывает окно (событие pg.QUIT),
      завершает работу pg и вызывает SystemExit.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Инициализирует игру и запускает основной игровой цикл.

    Создает объекты змейки и яблока, настраивает центральный элемент экрана,
    a затем входит в бесконечный цикл,
    который обрабатывает действия пользователя,
    обновляет состояние игры и отображает на экране.
    """
    pg.init()

    snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
    apple = Apple(restricted_cells=snake.positions)

    # Цикл одной игры
    while True:

        clock.tick(SPEED)  # Ограничение FPS

        # Обработка действий пользователя
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        if snake.collision_detected():
            snake.reset()
            apple.randomize_position(snake.positions)

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow()  # Увеличение длины змейки
            apple.randomize_position(snake.positions)

        # Отрисовка игрового поля
        screen.fill(BOARD_BACKGROUND_COLOR)  # Заполнение фона
        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки

        pg.display.update()  # Обновление экрана


if __name__ == "__main__":
    main()
