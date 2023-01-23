import os
import sys

import pygame
import requests

pygame.init()
size = window_width, window_height = 900, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
gameDisplay = pygame.display.set_mode((window_width, window_height))
font1 = pygame.font.SysFont("arialblack", 13)  # шрифт для получаемого текста
font2 = pygame.font.SysFont("arialblack", 13)  # шрифт для надписей "войти" и "регистрация"
text_coord = 'Координаты'
text_map = 'Масштаб'

input_coord = pygame.Rect(10, 10, 300, 20)
input_map = pygame.Rect(320, 10, 300, 20)# прямоугольник для ввода текста
sign_in_button = pygame.Rect(650, 10, 200, 20)
sign_in_label = font2.render("Найти", True, "black")

color_inactive = pygame.Color("#474747")
color_active = pygame.Color('white')
color_coord = color_inactive
color_map = color_inactive
active_coord = False
active_map = False
crashed = False
image = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_coord.collidepoint(event.pos):
                active_coord = not active_coord
            else:
                active_coord = False
            if input_map.collidepoint(event.pos):
                active_map = not active_map
            else:
                active_map = False
            color_coord = color_active if active_coord else color_inactive
            color_map = color_active if active_map else color_inactive

            # если нажата кнопка "войти"
            if sign_in_button.collidepoint(event.pos):
                coord = text_coord
                map = text_map

                map_request = "http://static-maps.yandex.ru/1.x/?ll="
                map_request += coord + '&spn='
                map_request += map + ',' + map + '&l=map'
                response = requests.get(map_request)

                if not response:
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)

                # Запишем полученное изображение в файл.
                map_file = "map.png"
                image = True

        if event.type == pygame.KEYDOWN:
            if active_coord:
                if event.key == pygame.K_RETURN:
                    text_coord = ''
                elif event.key == pygame.K_BACKSPACE:
                    text_coord = text_coord[:-1]
                else:
                    text_coord += event.unicode
            if active_map:
                if event.key == pygame.K_RETURN:
                    text_map = ''
                elif event.key == pygame.K_BACKSPACE:
                    text_map = text_map[:-1]
                else:
                    text_map += event.unicode

    gameDisplay.fill((0, 0, 0))

    # рендер текста
    txt_coord = font1.render(text_coord, True, color_coord)

    screen.blit(txt_coord, (input_coord.x + 5, input_coord.y - 1))
    pygame.draw.rect(screen, color_coord, input_coord, 2)

    txt_map = font1.render(text_map, True, color_map)

    screen.blit(txt_map, (input_map.x + 5, input_map.y - 1))
    pygame.draw.rect(screen, color_map, input_map, 2)

    pygame.draw.rect(screen, (255, 255, 255), sign_in_button)  # кнопка "найти"
    screen.blit(sign_in_label, (660, 10))

    if image:
        with open(map_file, "wb") as file:
            file.write(response.content)

        screen.blit(pygame.image.load(map_file), (20, 30))
        pygame.display.flip()

    pygame.display.update()
