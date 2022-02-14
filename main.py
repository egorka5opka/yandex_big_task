import os
import sys

import pygame
import requests
from io import BytesIO
from classes import Button, EditText, ImageButton
import pygame.examples

static_api = "http://static-maps.yandex.ru/1.x/"
geocoder_api = "http://geocode-maps.yandex.ru/1.x/"
geokey = "40d1649f-0493-4b70-98ba-98533de7710b"
SCREEN_SIZE = SCREEN_W, SCREEN_H = 650, 650
spn = 30
center = [0, 0]
map_type = 0
maps = ["map", "sat", "sat,skl"]
maps_names = ["Схема", "Спутник", "Гибрид"]
default_point = "{},pm2ntl"
points = []
motion = {pygame.K_UP: (0, 0.5), pygame.K_DOWN: (0, -0.5),
          pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill((155, 155, 155))
all_sprites = pygame.sprite.Group()
print(pygame.examples.__file__)


def get_map_png(ll=None, spn=None, pts=[], l="map"):
    params = {
        "l": l,
        "size": "650,450"
    }
    if ll:
        params["ll"] = ",".join(map(str, ll))
    if spn:
        params["spn"] = ",".join(map(str, spn))
    if pts:
        params["pt"] = "~".join(pts)
    print(pts)
    response = requests.get(static_api, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return pygame.image.load(BytesIO(response.content))


def draw_map():
    screen.fill((155, 155, 155))
    map_file = get_map_png(ll=center, spn=(spn, spn), l=maps[map_type], pts=points)
    screen.blit(map_file, (0, 0))
    all_sprites.draw(screen)


def calc_coords(geoobj):
    ll = geoobj["Point"]["pos"].split()
    envelope = geoobj["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    return ll, float(dx)


def get_coords(name):
    response = requests.get(geocoder_api, params={
        "apikey": geokey,
        "geocode": name,
        "format": "json"
    })
    if not response:
        print("Ничего не найдено")
        print(response.url)
        exit(0)
    json_response = response.json()
    if not json_response["response"]["GeoObjectCollection"]["featureMember"]:
        return center, spn
    return calc_coords(json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"])


def main():
    global spn, center, map_type, points
    map_type_btn = Button((2, 452), (200, 40), "Схема", all_sprites)
    req_et = EditText((2, 494), (SCREEN_W - 54, 40), 30, all_sprites)
    search_btn = ImageButton((SCREEN_W - 42, 494), (40, 40), "search.png", all_sprites)
    draw_map()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    spn *= 1.5
                    if spn > 90:
                        spn = 90
                    draw_map()
                elif event.key == pygame.K_PAGEDOWN:
                    spn /= 1.5
                    draw_map()
                elif event.key in motion:
                    dx, dy = motion[event.key]
                    center[0] += dx * spn
                    center[1] += dy * spn
                    if center[0] >= 180:
                        center[0] -= 360
                    if center[0] <= -180:
                        center[0] += 360
                    if center[0] == 180:
                        center[0] = 179
                    center[1] = min(max(center[1], -85), 85)
                    draw_map()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if map_type_btn.clicked(event.pos):
                    map_type = (map_type + 1) % len(maps)
                    map_type_btn.change_text(maps_names[map_type])
                    draw_map()
                if search_btn.clicked(event.pos):
                    points.clear()
                    center, spn = get_coords(req_et.text)
                    points.append(default_point.format(",".join(map(str, center))))
                    draw_map()
            req_et.update(event)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


main()
