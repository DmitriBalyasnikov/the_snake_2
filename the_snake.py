"""Змейка — игра, в которой игрок управляет змейкой."""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE    # 32 cells
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # 24 cells

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """
    Базовый класс для игрового объекта.

    Атрибуты:
    - position (list): позиция объекта на плоскости в формате [x, y].
    - body_color (tuple): цвет объекта в формате (R, G, B).

    Методы:
    - __init__(): инициализирует новый экземпляр игрового объекта.
    - draw(): метод для отрисовки объекта. По умолчанию ничего не делает.
    """

    def __init__(self):
        """Инициализирует новый экземпляр игрового объекта."""
        self.position = [0, 0]
        self.body_color = (0, 0, 0)

    def draw(self):
        """Метод для отрисовки объекта. По умолчанию ничего не делает."""
        pass


class Snake(GameObject):
    """
    Класс для представления змейки в игре.

    Наследуется от класса GameObject.

    Атрибуты:
    - start_position (list): начальная позиция змейки.
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

    def __init__(self, x=0, y=0, body_color=SNAKE_COLOR):
        """Инициализирует новый экземпляр змейки c заданными параметрами."""
        super().__init__()
        start_position = [x, y]
        self.position = start_position
        self.start_position = start_position
        self.body_color = body_color
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow_on_next_move = False

    def draw(self):
        """Рисует змейки на экране."""
        for position in self.positions:
            left = position[0] * GRID_SIZE
            top = position[1] * GRID_SIZE
            rect = pygame.Rect(left, top, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def grow(self):
        """Устанавливает флаг для роста змейки при следующем движении."""
        self.grow_on_next_move = True

    def reset(self):
        """Сбрасывает состояние змейки к начальному."""
        self.position = self.start_position
        self.positions = [self.start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow_on_next_move = False

    def move(self):
        """Перемещает змейку в соответствии c текущим направлением движения."""
        new_x = self.positions[0][0] + self.direction[0]
        new_y = self.positions[0][1] + self.direction[1]

        if new_x >= GRID_WIDTH:
            new_x = 0

        if new_x < 0:
            new_x = GRID_WIDTH - 1

        if new_y >= GRID_HEIGHT:
            new_y = 0

        if new_y < 0:
            new_y = GRID_HEIGHT - 1

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
        if self.positions.__len__ == 1:
            return False
        head_position = self.get_head_position()
        tail_positions = self.positions[1:]
        for position in tail_positions:
            if position == head_position:
                return True
        return False

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

    def __init__(self, color=APPLE_COLOR):
        """Инициализирует новый экземпляр яблока."""
        super().__init__()
        self.position = []
        self.body_color = color
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1)
        y = randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)

    def draw(self):
        """Рисует яблоко на экране."""
        left = self.position[0] * GRID_SIZE
        top = self.position[1] * GRID_SIZE
        rect = pygame.Rect(left, top, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
    - Если пользователь закрывает окно (событие pygame.QUIT),
      завершает работу pygame и вызывает SystemExit.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Инициализирует игру и запускает основной игровой цикл.

    Создает объекты змейки и яблока, настраивает центральный элемент экрана,
    a затем входит в бесконечный цикл,
    который обрабатывает действия пользователя,
    обновляет состояние игры и отображает на экране.
    """
    pygame.init()

    snake = Snake(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
    apple = Apple()

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
            apple.randomize_position()

        # Проверка столкновения с яблоком
        if snake.positions[0] == apple.position:
            apple.randomize_position()  # Появление нового яблока
            snake.grow()   # Увеличение длины змейки

        # Отрисовка игрового поля
        screen.fill(BOARD_BACKGROUND_COLOR)  # Заполнение фона
        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки

        pygame.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
