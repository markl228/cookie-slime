import pygame
import sys
import os


GRASS = 'grass.png'
BOX = 'box.png'
GRASS_SP = pygame.sprite.Group()
BOX_SP = pygame.sprite.Group()
CUT_SP = pygame.sprite.Group()
DICT_OF_SP = {0: GRASS,
              1: BOX}
BAKE_SP = pygame.sprite.Group()
DICT_POS = {(0, 14):'Bake', (1, 14):'Bake', (0, 15):'Bake', (1, 15):'Bake',
            (2, 14):'Сonveyor', (3, 14):'Сonveyor', (2, 15):'Сonveyor', (3, 15):'Сonveyor',
            (4, 14):'Chest', (5, 14):'Chest', (4, 15):'Chest', (5, 15):'Chest'}


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
        self.cell_size = 34

    def render(self, screen, *groups):
        for y in range(self.height):
            for x in range(self.width):
                # clos[self.board[y][x]]
                if self.board[y][x] == 0:
                    Grass(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, groups[1],
                          groups[self.board[y][x]])
                else:
                    Box(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, groups[0],
                        groups[self.board[y][x]])

                pygame.draw.rect(screen, pygame.Color('white'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)
        total = 10
        for i in range(7):
            pygame.draw.rect(screen, pygame.Color(128, 128, 128), (total, 485, 67, 67), 2)
            total += 68

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        if not cell[1] >= 14:
            self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_y >= 14:
            print(DICT_POS[cell_x, cell_y])
        elif cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        else:
            print(cell)


class CutPict(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(CUT_SP)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[0]
        self.rect = self.rect.move(x, y)
        self.image = pygame.transform.scale(self.image, (80, 80))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[324]
        self.image = pygame.transform.scale(self.image, (80, 80))


class СonveyorMenu(CutPict):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[0]
        self.rect = self.rect.move(x, y)
        self.image = pygame.transform.scale(self.image, (80, 80))

    def update(self):
        self.image = self.frames[390]
        self.image = pygame.transform.scale(self.image, (80, 80))


class ChestMenu(CutPict):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[0]
        self.rect = self.rect.move(x, y)
        self.image = pygame.transform.scale(self.image, (80, 80))

    def update(self):
        self.image = self.frames[338]
        self.image = pygame.transform.scale(self.image, (80, 80))


class Box(pygame.sprite.Sprite):
    image = load_image('bake.png')

    def __init__(self, x, y, a, *group):
        super().__init__(*group)
        self.image = Box.image
        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(Box.image, (a, a))
        self.rect.x = x
        self.rect.y = y


class Grass(pygame.sprite.Sprite):
    image = load_image('grass.png')

    def __init__(self, x, y, a, *group):
        super().__init__(*group)
        self.image = Grass.image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (a, a))
        self.rect.x = x
        self.rect.y = y



def main():
    pygame.init()
    size = 500, 560
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Координаты клетки')
    board = Board(14, 14)
    clock = pygame.time.Clock()

    CutPict(load_image("mcblocks.png"), 18, 36, 5, 480)
    СonveyorMenu(load_image("mcblocks.png"), 18, 36, 72, 480)
    ChestMenu(load_image("mcblocks.png"), 18, 36, 140, 480)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        CUT_SP.draw(screen)
        CUT_SP.update()
        BAKE_SP.draw(screen)
        BAKE_SP.update()
        GRASS_SP.draw(screen)
        BOX_SP.draw(screen)
        board.render(screen, BOX_SP, GRASS_SP)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


if __name__ == '__main__':
    main()
