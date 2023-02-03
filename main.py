import pygame

import engine2


SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450

WHITE = (255, 255, 255)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("")
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    game = engine2.Game(screen)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    game.undo_move()

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.update(pygame.mouse.get_pos())
            else:
                game.update()

        pygame.display.update()
        clock.tick()


main()
