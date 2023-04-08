import pygame
import requests
import math

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Maps API task #12')
size = window_width, window_height = 845, 570
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
gameDisplay = pygame.display.set_mode((window_width, window_height))
crashed = False


class Maps_api:
    def __init__(self):
        self.font1 = pygame.font.SysFont("arialblack", 13)
        self.font2 = pygame.font.SysFont("arialblack", 13)
        self.text_coord = '0,0'
        self.text_map = '0'
        self.text_request = ''
        self.text_adres = ''
        self.map_file = "map.png"
        self.first_response = ''
        self.marks = []

        self.print_adres = pygame.Rect(30, 530, 785, 20)
        self.input_coord = pygame.Rect(30, 10, 190, 20)
        self.input_map = pygame.Rect(225, 10, 190, 20)
        self.input_request = pygame.Rect(420, 10, 190, 20)
        self.sign_in_button = pygame.Rect(630, 10, 190, 20)
        self.background_address = pygame.Rect(0, 530, 845, 20)
        self.sign_in_label = self.font2.render("Найти", True, "black")

        self.map_button = pygame.Rect(630, 50, 190, 20)
        self.map_label = self.font2.render("Схема", True, "black")

        self.sput_button = pygame.Rect(630, 80, 190, 20)
        self.sput_label = self.font2.render("Спутник", True, "black")

        self.gibrid_button = pygame.Rect(630, 110, 190, 20)
        self.gibrid_label = self.font2.render("Гибрид", True, "black")

        self.delet_button = pygame.Rect(630, 140, 190, 20)
        self.delet_label = self.font2.render("Сброс", True, "black")

        self.mail_button = pygame.Rect(630, 170, 190, 20)
        self.mail_label = self.font2.render("Почтовый индекс", True, "black")

        self.color_inactive = pygame.Color("gray")
        self.color_active = pygame.Color('black')
        self.color_coord = self.color_inactive
        self.color_map = self.color_inactive
        self.color_request = self.color_inactive
        self.active_coord = False
        self.active_map = False
        self.active_request = False
        self.image = False

        self.format_image = 'map'

    def input(self, event):  # Взаимодействие с полями ввода
        if self.active_coord:
            if event.key == pygame.K_RETURN:
                self.text_coord = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text_coord = self.text_coord[:-1]
            else:
                self.text_coord += event.unicode
        elif self.active_map:
            if event.key == pygame.K_RETURN:
                self.text_map = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text_map = self.text_map[:-1]
            else:
                self.text_map += event.unicode
        elif self.active_request:
            if event.key == pygame.K_RETURN:
                self.text_request = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text_request = self.text_request[:-1]
            else:
                self.text_request += event.unicode

    def draw(self, screen):  # Отрисовка всех элементов доступных к взаимодействию и вспомагательных элементов
        self.txt_coord = self.font1.render(self.text_coord, True, self.color_coord)
        screen.blit(self.txt_coord, (self.input_coord.x + 5, self.input_coord.y - 1))
        pygame.draw.rect(screen, self.color_coord, self.input_coord, 2)

        self.txt_map = self.font1.render(self.text_map, True, self.color_map)
        screen.blit(self.txt_map, (self.input_map.x + 5, self.input_map.y - 1))
        pygame.draw.rect(screen, self.color_map, self.input_map, 2)

        self.txt_request = self.font1.render(self.text_request, True, self.color_request)
        screen.blit(self.txt_request, (self.input_request.x + 5, self.input_request.y - 1))
        pygame.draw.rect(screen, self.color_request, self.input_request, 2)

        pygame.draw.rect(screen, pygame.Color('white'), self.background_address)
        self.txt_adress = self.font1.render(self.text_adres, True, self.color_active)
        screen.blit(self.txt_adress, (self.print_adres.x + 5, self.print_adres.y - 1))
        pygame.draw.rect(screen, self.color_inactive, self.print_adres, 2)

        pygame.draw.rect(screen, pygame.Color('gray'), self.sign_in_button)
        screen.blit(self.sign_in_label, (705, 10))
        pygame.draw.rect(screen, pygame.Color('gray'), self.map_button)
        screen.blit(self.map_label, (705, 50))
        pygame.draw.rect(screen, pygame.Color('gray'), self.sput_button)
        screen.blit(self.sput_label, (700, 80))
        pygame.draw.rect(screen, pygame.Color('gray'), self.gibrid_button)
        screen.blit(self.gibrid_label, (705, 110))
        pygame.draw.rect(screen, pygame.Color('gray'), self.delet_button)
        screen.blit(self.delet_label, (705, 140))
        pygame.draw.rect(screen, pygame.Color('gray'), self.mail_button)
        screen.blit(self.mail_label, (670, 170))

    def load_image(self):  # Загрузка изображения
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)

        screen.blit(pygame.image.load(self.map_file), (20, 40))

    def mouse_btn(self, event):  # Вынесенная и типизированная обработка действий позьзователя
        if self.input_coord.collidepoint(event.pos):
            self.active_coord = not self.active_coord
        else:
            self.active_coord = False
        if self.input_map.collidepoint(event.pos):
            self.active_map = not self.active_map
        else:
            self.active_map = False
        if self.input_request.collidepoint(event.pos):
            self.active_request = not self.active_request
        else:
            self.active_request = False

        self.color_coord = self.color_active if self.active_coord else self.color_inactive
        self.color_map = self.color_active if self.active_map else self.color_inactive
        self.color_request = self.color_active if self.active_request else self.color_inactive

        if self.sign_in_button.collidepoint(event.pos):
            self.poisk()
        elif self.map_button.collidepoint(event.pos):
            self.format_image = 'map'
            self.poisk()
        elif self.sput_button.collidepoint(event.pos):
            self.format_image = 'sat'
            self.poisk()
        elif self.gibrid_button.collidepoint(event.pos):
            self.format_image = 'sat,skl'
            self.poisk()
        elif self.delet_button.collidepoint(event.pos):
            self.marks = []
            self.text_adres = ''
            self.text_request = ''
            self.poisk()

        elif self.mail_button.collidepoint(event.pos):
            if '[' in self.text_adres:
                self.text_adres = self.text_adres.split(' [')[0]
            else:
                toponym = requests.get("http://geocode-maps.yandex.ru/1.x/?apikey=" \
                                       "40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json".format(
                    self.text_request)).json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                self.text_adres += f' [{toponym_address}]'

    def cords_reconveret(self, cords):  # Преобразование из нажатия на карту в географические координаты
        return ','.join(map(str, [
            float(self.text_coord.split(',')[0]) + cords[0] * 0.0000428 * math.pow(2, 15 - int(self.text_map)),
            float(self.text_coord.split(',')[1]) - cords[1] * 0.0000428 * math.cos(
                math.radians(float(self.text_coord.split(',')[1]))) * math.pow(2, 15 - int(self.text_map))]))

    def search_organizations(self, cords):
        cords = [cords[0] - 320, cords[1] - 265]
        converted_cord = self.cords_reconveret(cords)

        map_params = {'apikey': "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
                      'text':  ','.join(converted_cord.split(',')[::-1]),
                      'lang': 'ru_RU',
                      'type': 'biz',
                      'spn': '0.1,0.1'}

        self.organization_response = \
        requests.get("https://search-maps.yandex.ru/v1/", map_params).json()

        self.marks = [converted_cord]
        self.response = requests.get("http://static-maps.yandex.ru/1.x/",
                                     {'ll': self.text_coord, 'z': str(int(self.text_map)), 'l': self.format_image,
                                      'pt': '~'.join([cord + ',pm2rdm' for cord in self.marks]) * int(
                                          bool(self.marks))})
        if not self.organization_response['features']:
            self.text_adres = 'Ничего не найдено (всё работает но не выдайт организации)'
        else:
            self.text_adres = ', '.join(
                [self.organization_response['features']['properties']['CompanyMetaData']['name'],
                 self.organization_response['features']['properties']['CompanyMetaData']['address']])

        self.image = True
        self.draw(screen)
        self.load_image()

    def search_objects(self, cords):
        cords = [cords[0] - 320, cords[1] - 265]
        converted_cord = self.cords_reconveret(cords)

        map_params = {'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
                      'geocode': converted_cord,
                      'format': 'json'
                      }

        self.text_adres = \
            requests.get("https://geocode-maps.yandex.ru/1.x/", map_params).json()["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]['formatted']

        if len(self.text_adres.split(', ')) > 2:
            self.text_adres = ','.join(self.text_adres.split(', ')[2:])

        self.marks = [converted_cord]
        self.response = requests.get("http://static-maps.yandex.ru/1.x/",
                                     {'ll': self.text_coord, 'z': str(int(self.text_map)), 'l': self.format_image,
                                      'pt': '~'.join([cord + ',pm2rdm' for cord in self.marks]) * int(
                                          bool(self.marks))})

        self.image = True
        self.draw(screen)
        self.load_image()

    def poisk(self, locate_status=False):
        map_request = "http://static-maps.yandex.ru/1.x/"

        if not self.text_request and not locate_status:
            map_params = {'ll': self.text_coord, 'z': str(int(self.text_map)), 'l': self.format_image,
                          'pt': '~'.join([cord + ',pm2rdm' for cord in self.marks]) * int(bool(self.marks))}

            self.response = requests.get(map_request, map_params)

            if not self.response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            else:
                self.image = True
                self.draw(screen)
                self.load_image()
        else:
            self.first_response = requests.get("http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-"
                                               "98533de7710b&geocode={}&format=json".format(
                self.text_request)).json()['response']['GeoObjectCollection']['featureMember']
            self.marks.append(','.join(self.first_response[0]['GeoObject']["Point"]["pos"].split(' ')))
            self.text_adres = self.first_response[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

            if not self.first_response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", self.first_response.status_code, "(", self.first_response.reason, ")")
            else:
                map_params = {'ll': self.text_coord, 'z': str(int(self.text_map)), 'l': self.format_image,
                              'pt': '~'.join([cord + ',pm2rdm' for cord in self.marks]) * int(bool(self.marks))}

                self.response = requests.get("http://static-maps.yandex.ru/1.x/", map_params)

                self.image = True
                self.draw(screen)
                self.load_image()


map_api = Maps_api()
loading = False
screen.fill((255, 255, 255))

while not crashed:
    pygame.draw.rect(screen, pygame.Color('white'), (0, 0, 645, 40))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] in range(20, 620) and event.pos[1] in range(40, 490):
                if event.button == 3:
                    map_api.search_organizations(event.pos)
                elif event.button == 1:
                    map_api.search_objects(event.pos)
            else:
                map_api.mouse_btn(event)
        if event.type == pygame.KEYDOWN:
            map_api.input(event)

    map_api.draw(screen)
    pygame.display.update()
