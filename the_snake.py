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
SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position, body_color):
        self.position = position            # Позиция объекта на игровом поле
        self.body_color = body_color        # Цвет объекта

    def draw(self):
        """Отрисовка объекта на игровом поле"""
        pass  # Реализация будет зависеть от конкретного подкласса


class Snake(GameObject):

    def __init__(self, start_position, body_color=SNAKE_COLOR):
        super().__init__(start_position, body_color)
        self.positions = [start_position]    # Список позиций сегментов змейки
        self.direction = RIGHT               # Текущее направление движения
        self.next_direction = None           # Следующее направление движения 
        self.grow_on_next_move = False                              

    def draw(self):
        for position in self.positions:
            left = position[0] * GRID_SIZE
            top = position[1] * GRID_SIZE
            rect = pygame.Rect(left, top, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def grow(self):
        self.grow_on_next_move = True

    def move(self):
        # Обновление позиции змейки в соответствии с направлением движения
        new_x = self.positions[0][0] + self.direction[0]
        new_y = self.positions[0][1] + self.direction[1]

        if new_x > GRID_WIDTH:
            new_x = 0

        if new_x < 0:
            new_x = GRID_WIDTH

        if new_y > GRID_HEIGHT:
            new_y = 0

        if new_y < 0:
            new_y = GRID_HEIGHT

        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if not self.grow_on_next_move:
            self.positions.pop()  # Удаление последнего сегмента (хвоста)
        else:
            self.grow_on_next_move = False

    def get_head_position(self):
        return self.positions[-1]

    def collision_detected(self):
        if self.positions.__len__ == 1:
            return False
        head_position = self.get_head_position()
        tail_positions = self.positions[:-1]
        for position in tail_positions:
            if position == head_position:
                return True
        return False

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple(GameObject):
    def __init__(self, color=APPLE_COLOR):
        super().__init__(None, color)
        self.spawn()  # Появление яблока в случайной позиции

    def spawn(self):
        # Случайная позиция на игровом поле
        x = randint(0, GRID_WIDTH - 1)
        y = randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)

    def draw(self):
        left = self.position[0] * GRID_SIZE
        top = self.position[1] * GRID_SIZE
        rect = pygame.Rect(left, top, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
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
    # После столкновения змейки с самой собой начинаем игру заново
    while True:
        pygame.init()  # Инициализация PyGame
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)  # Настройка игрового окна
        pygame.display.set_caption('Змейка')  # Заголовок окна игрового поля
        clock = pygame.time.Clock()  # Настройка времени

        # Создание экземпляров классов
        screen_center = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

        snake = Snake(screen_center)  # Змейка по центру поля
        apple = Apple()  # Яблоко

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
                break

            # Проверка столкновения с яблоком
            if snake.positions[0] == apple.position:
                apple.spawn()  # Появление нового яблока
                snake.grow()   # Увеличение длины змейки

            # Отрисовка игрового поля
            screen.fill(BOARD_BACKGROUND_COLOR)  # Заполнение фона
            apple.draw()  # Отрисовка яблока
            snake.draw()  # Отрисовка змейки

            pygame.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
