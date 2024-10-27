"""Вызов необходимых импортов."""
import pygame

from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
"""Константы для размеров поля и сетки:"""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
"""Направления движения:"""
BOARD_BACKGROUND_COLOR = (0, 0, 0)
"""Цвет фона - черный:"""
BORDER_COLOR = (93, 216, 228)
"""Цвет границы ячейки"""
APPLE_COLOR = (255, 0, 0)
"""Цвет яблока"""
SNAKE_COLOR = (0, 255, 0)
"""Цвет змейки"""
SPEED = 20
"""Скорость движения змейки:"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
"""Настройка игрового окна:"""
pygame.display.set_caption("Многострадальная змейка стдудента 53 когорты.")
"""Заголовок окна игрового поля:"""
clock = pygame.time.Clock()
"""Настройка времени."""


class GameObject:
    """Родительский класс игры."""

    def __init__(
        self, position=SCREEN_CENTER, body_color=BOARD_BACKGROUND_COLOR
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Родительский метод отрисовки."""
        raise NotImplementedError
    # TODO переопределить в дочерних классах


class Apple(GameObject):
    """Объявление класса Apple."""

    def __init__(self, position: tuple = (), body_color: tuple = APPLE_COLOR):
        super().__init__(position=position, body_color=body_color)
        self.randomize_position([position])

    def randomize_position(self, restricted_area: tuple = ()) -> None:
        """Метод случайного местонахождения объекта класса Apple."""
        while self.position in restricted_area:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )

    def draw(self):
        """Метод отрисовки объукта класса Aplle."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объявление класса Snake."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR) -> None:
        """Инициализируется объект класса."""
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.reset = self.get_head_position() in self.positions[1:]

    def draw(self):
        """Метод отрисовки объукта класса Snake."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод описывающий механизм движения объекта."""
        x, y = self.get_head_position()
        direction_x, direction_y = self.direction
        head_position_x = (x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH
        head_position_y = (y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        self.positions.insert(0, (head_position_x, head_position_y))
        """Строка возвращающая значение первого элемента объекта."""
        x = 0 if x > GRID_WIDTH else x
        x = GRID_WIDTH if x < 0 else x
        y = 0 if y > GRID_HEIGHT else y
        y = GRID_HEIGHT if y < 0 else y
        """Возможность сквозного прохода объектом границ поля игры."""
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Метод класса возвращающий координаты первого элемента объекта."""
        return self.positions[0]

    def reset(self):
        """Метод сброса значения змейки, до исходного состояния."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = randint(RIGHT, LEFT)

    def update_direction(self):
        """Метод обновления направления движения объекта."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Функция позволяющая управлять объктами на игровом поле."""
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
    """Основная функция игры."""
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    restricted_area = snake.positions
    apple = Apple(restricted_area)

    while True:
        """Основной цикл игры."""
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        snake.draw()
        snake.move()

        if snake.get_head_position() == apple.position:
            """Проверка на наличие объекта класса Aplle в координатах Snake."""
            snake.length += 1
            apple.randomize_position(snake.positions)

        pygame.display.update()


if __name__ == "__main__":
    main()
