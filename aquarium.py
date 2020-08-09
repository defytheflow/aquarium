import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320


def main():
    pygame.init()
    pygame.display.set_caption('Aquarium')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main()
