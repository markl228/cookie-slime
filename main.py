import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen, *groups):
        for y in range(self.height):
            for x in range(self.width):
                # clos[self.board[y][x]]
                Box(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    groups[self.board[y][x]])
                pygame.draw.rect(screen, pygame.Color('white'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        else:
            print(cell)


class Box(pygame.sprite.Sprite):
    image = load_image('grass.png')
    grass = load_image('box.png')

    def __init__(self, x, y, a, *group):
        super().__init__(*group)
        self.image = Box.image
        self.grass = Box.grass
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (a, a))
        self.grass = pygame.transform.scale(self.grass, (a, a))
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        self.image = self.grass


def main():
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Координаты клетки')
    board = Board(16, 16)

    all_sprites = pygame.sprite.Group()
    new_sprites = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                all_sprites.update(event)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        new_sprites.draw(screen)
        board.render(screen, all_sprites, new_sprites)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()