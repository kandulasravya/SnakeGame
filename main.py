import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (12, 121, 136)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(5, 25) * SIZE
        self.y = random.randint(5, 15) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(1)
        self.y.append(1)

    def draw(self):
        self.parent_screen.fill((12, 121, 136))

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
            pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_bg_music()
        self.surface = pygame.display.set_mode((1200, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True

        return False

    def play_bg_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"GAME OVER! Your Score is {self.snake.length - 1}", True, (255, 255, 200))
        self.surface.blit(line1, (400, 300))
        line2 = font.render(f"Press ENTER to play again", True, (255, 255, 200))
        self.surface.blit(line2, (420, 400))
        line3 = font.render(f"Press ESC to exit the game", True, (255, 255, 200))
        self.surface.blit(line3, (420, 500))
        pygame.display.flip()

    def play_sound(self, _sound):
        if _sound == "ding":
            sound = pygame.mixer.Sound("resources/1_snake_game_resources_ding.mp3")
        elif _sound == "crash":
            sound = pygame.mixer.Sound("resources/1_snake_game_resources_crash.mp3")

        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # snake collision with apple
            self.snake.increase_length()
            self.apple.move()
            self.play_sound("ding")

        # snake collision with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                pygame.mixer.music.pause()
                raise Exception("GAME OVER")

        # snake collision with edges
        if self.snake.x[0]>=1200 or self.snake.y[0]>=800 or self.snake.x[0]<0 or self.snake.y[0]<0:
            self.play_sound("crash")
            pygame.mixer.music.pause()
            raise Exception("GAME OVER")

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.2)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 200))
        self.surface.blit(score, (800, 10))


if __name__ == "__main__":
    game = Game()
    game.run()
