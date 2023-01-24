import os
import sys

import pygame
import requests

pygame.init()
size = window_width, window_height = 900, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
gameDisplay = pygame.display.set_mode((window_width, window_height))
crashed = False


class Maps_api:
    def __init__(self):
        self.font1 = pygame.font.SysFont("arialblack", 13)  # шрифт для получаемого текста
        self.font2 = pygame.font.SysFont("arialblack", 13)  # шрифт для надписей "войти" и "регистрация"
        self.text_coord = 'Координаты'
        self.text_map = 'Масштаб'

        self.input_coord = pygame.Rect(10, 10, 300, 20)
        self.input_map = pygame.Rect(320, 10, 300, 20)# прямоугольник для ввода текста
        self.sign_in_button = pygame.Rect(650, 10, 200, 20)
        self.sign_in_label = self.font2.render("Найти", True, "black")

        self.color_inactive = pygame.Color("#474747")
        self.color_active = pygame.Color('white')
        self.color_coord = self.color_inactive
        self.color_map = self.color_inactive
        self.active_coord = False
        self.active_map = False
        self.image = False

    def mouse_btn(self, event):
        if self.input_coord.collidepoint(event.pos):
            self.active_coord = not self.active_coord
        else:
            self.active_coord = False
        if self.input_map.collidepoint(event.pos):
            self.active_map = not self.active_map
        else:
            self.active_map = False
        self.color_coord = self.color_active if self.active_coord else self.color_inactive
        self.color_map = self.color_active if self.active_map else self.color_inactive

        if self.sign_in_button.collidepoint(event.pos):
            self.poisk()

    def poisk(self):
        coord = self.text_coord
        map = self.text_map

        map_request = "http://static-maps.yandex.ru/1.x/?ll="
        map_request += coord + '&spn='
        map_request += map + ',' + map + '&l=map'
        self.response = requests.get(map_request)

        if not self.response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        self.image = True

    def input(self, event):
        if self.active_coord:
            if event.key == pygame.K_RETURN:
                self.text_coord = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text_coord = self.text_coord[:-1]
            else:
                self.text_coord += event.unicode
        if self.active_map:
            if event.key == pygame.K_RETURN:
                self.text_map = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text_map = self.text_map[:-1]
            else:
                self.text_map += event.unicode

    def draw(self, screen):
        self.txt_coord = self.font1.render(self.text_coord, True, self.color_coord)

        screen.blit(self.txt_coord, (self.input_coord.x + 5, self.input_coord.y - 1))
        pygame.draw.rect(screen, self.color_coord, self.input_coord, 2)

        self.txt_map = self.font1.render(self.text_map, True, self.color_map)

        screen.blit(self.txt_map, (self.input_map.x + 5, self.input_map.y - 1))
        pygame.draw.rect(screen, self.color_map, self.input_map, 2)

        pygame.draw.rect(screen, (255, 255, 255), self.sign_in_button)  # кнопка "найти"
        screen.blit(self.sign_in_label, (660, 10))

        if self.image:
            with open(self.map_file, "wb") as file:
                file.write(self.response.content)

            screen.blit(pygame.image.load(self.map_file), (20, 30))
            pygame.display.flip()


map_api = Maps_api()
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            map_api.mouse_btn(event)

        if event.type == pygame.KEYDOWN:
            map_api.input(event)

    gameDisplay.fill((0, 0, 0))

    map_api.draw(screen)

    pygame.display.update()
