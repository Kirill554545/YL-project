import pygame
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лови фрукты")

# Определяем путь к изображениям
image_big_path = "C:/Projects/Learning/Project2/zucchini.png"  # Путь к изображению для большого объекта
image_medium_path = "C:/Projects/Learning/Project2/pear.png"  # Путь к изображению для среднего объекта
image_small_path = "C:/Projects/Learning/Project2/apple.png"  # Путь к изображению для маленького объекта
image_player_path = "C:/Projects/Learning/Project2/snake.png"  # Путь к изображению для игрока


# Загружаем изображения
big_obj_image = pygame.image.load(image_big_path).convert_alpha()
medium_obj_image = pygame.image.load(image_medium_path).convert_alpha()
small_obj_image = pygame.image.load(image_small_path).convert_alpha()
player_image = pygame.image.load(
    image_player_path
).convert_alpha()  # изображение игрока

# Определяем размеры объектов
size_large = 90  # Размер большого объекта
size_medium = 80  # Размер среднего объекта
size_small = 60  # Размер маленького объекта
player_size = 80  # Размер игрока (изменено на 80 пикселей)
# Уменьшаем изображения до нужных размеров
big_obj_image = pygame.transform.scale(big_obj_image, (size_large, size_large))
medium_obj_image = pygame.transform.scale(medium_obj_image, (size_medium, size_medium))
small_obj_image = pygame.transform.scale(small_obj_image, (size_small, size_small))
player_image = pygame.transform.scale(
    player_image, (player_size, player_size)
)  # Масштабируем изображение игрока

max_objects = 10  # Определяем максимальное количество падающих объектов на экране


# Класс для падающих объектов
class FallingObject:
    def __init__(self, obj_type):
        images = [
            big_obj_image,
            medium_obj_image,
            small_obj_image,
        ]  # Изображения объектов
        self.image = images[obj_type]
        self.size = self.image.get_size()  # Используем размеры изображения

        self.x = random.randint(0, WIDTH - self.size[0])  # Ширина изображения
        self.y = -self.size[1]  # Начало выше экрана

        # Скорость падения
        self.speed = [3, 2.5, 2][obj_type]  # Скорость падения: увеличена
        self.obj_type = obj_type  # Сохраняем тип объекта

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))  # Рисуем изображение


# Класс для управляемого объекта
class Player:
    def __init__(self):
        self.size = player_size  # Размер игрока
        self.x = (WIDTH - self.size) // 2  # Начальная позиция по центру
        self.y = HEIGHT - self.size - 10  # Немного выше низа экрана
        self.speed = 5  # Скорость движения

    def move(self, dx):
        self.x += dx
        # Ограничиваем движение в пределах экрана
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.size:
            self.x = WIDTH - self.size

    def draw(self, surface):
        surface.blit(player_image, (self.x, self.y))  # Рисуем изображение игрока

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


# Функция для перезапуска игры
def reset_game():
    return [], Player(), 0, False, False  # Возвращаем начальные значения


# Основной игровой цикл


def main():
    clock = pygame.time.Clock()
    falling_objects, player, score, game_over, player_won = reset_game()

    running = True
    game_started = False  # Состояние начала игры

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_started:
            # Отображение сообщения о начале игры
            window.fill((255, 255, 255))  # Устанавливаем белый фон
            font = pygame.font.Font(None, 74)
            start_text = font.render("Нажмите Enter, чтобы начать", True, (0, 0, 0))
            text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            window.blit(start_text, text_rect)

            # Проверка нажатия Enter для начала игры
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # K_RETURN - клавиша Enter
                game_started = True  # Начинаем игру

        else:
            if not game_over and not player_won:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:  # Движение влево
                    player.move(-player.speed)
                if keys[pygame.K_d]:  # Движение вправо
                    player.move(player.speed)

                # Добавляем новый объект только если их меньше максимального количества
                if len(falling_objects) < max_objects and random.randint(1, 30) == 1:
                    obj_type = random.randint(
                        0, 2
                    )  # 0 - большой, 1 - средний, 2 - маленький
                    falling_objects.append(FallingObject(obj_type))

                # Обновляем позиции объектов и проверяем на столкновение с игроком
                for obj in falling_objects:
                    obj.fall()

                    # Проверяем на столкновение
                    if player.get_rect().colliderect(
                        pygame.Rect(obj.x, obj.y, obj.size[0], obj.size[1])
                    ):
                        if obj.obj_type == 0:  # Большой объект
                            score -= 2  # Уменьшаем на 2 очка
                        elif obj.obj_type == 1:  # Средний объект
                            score += 2
                        elif obj.obj_type == 2:  # Маленький объект
                            score += 1

                        # Удаляем объект после столкновения
                        falling_objects.remove(obj)

                # Проверяем, не достиг ли счет отрицательных значений
                if score < 0:
                    game_over = True  # Устанавливаем флаг окончания игры

                # Проверяем достижение счета 30 для победы
                if score >= 30:
                    player_won = True  # Устанавливаем флаг победы

                # Удаляем объекты, которые вышли за границы экрана
                falling_objects = [obj for obj in falling_objects if obj.y < HEIGHT]

                # Очистка экрана
                window.fill((255, 255, 255))  # Устанавливаем белый фон

                # Рисуем все падающие объекты
                for obj in falling_objects:
                    obj.draw(window)

                # Рисуем управляемый объект
                player.draw(window)

                # Отображаем счет
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
                window.blit(
                    score_text, (10, 10)
                )  # Размещение счета в верхнем левом углу

            else:
                # Проверяем, проиграл игрок или победил
                if game_over:
                    # Отображение текста "Game Over!" с первоначальным размером шрифта

                    font = pygame.font.Font(None, 74)  # Оставляем размер шрифта 74
                    game_over_text = font.render("Game Over!", True, (255, 0, 0))
                    text_rect = game_over_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 3)
                    )
                    window.blit(game_over_text, text_rect)

                    # Отображение текста "Нажмите пробел чтобы начать заново" с уменьшенным размером шрифта
                    smaller_font = pygame.font.Font(
                        None, 36
                    )  # Уменьшаем размер шрифта для второго текста
                    restart_text = smaller_font.render(
                        "Нажмите пробел чтобы начать заново", True, (0, 0, 0)
                    )
                    restart_rect = restart_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    window.blit(restart_text, restart_rect)

                elif player_won:
                    # Отображение текста "Вы победили!" с первоначальным размером шрифта
                    font = pygame.font.Font(None, 74)  # Оставляем размер шрифта 74
                    win_text = font.render("Вы победили!", True, (0, 255, 0))
                    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                    window.blit(win_text, text_rect)

                    # Отображение текста "Нажмите пробел чтобы начать заново" с уменьшенным размером шрифта
                    smaller_font = pygame.font.Font(
                        None, 36
                    )  # Уменьшаем размер шрифта для второго текста
                    restart_text = smaller_font.render(
                        "Нажмите пробел чтобы начать заново", True, (0, 0, 0)
                    )
                    restart_rect = restart_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    window.blit(restart_text, restart_rect)

                    # Проверяем нажатие пробела для перезапуска игры
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    falling_objects, player, score, game_over, player_won = (
                        reset_game()
                    )  # Перезапуск игры

                # Обновляем экран
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
