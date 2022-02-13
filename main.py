import os
import sys

import pygame
import requests
from io import BytesIO
from classes import Button

static_api = "http://static-maps.yandex.ru/1.x/"
geocoder_api = ""
geokey = ""
SCREEN_SIZE = SCREEN_W, SCREEN_H = 650, 650
spn = 30
center = [0, 0]
map_type = 0
maps = ["map", "sat", "sat,skl"]
maps_names = ["Схема", "Спутник", "Гибрид"]
motion = {pygame.K_UP: (0, 0.5), pygame.K_DOWN: (0, -0.5),
          pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill((155, 155, 155))
all_sprites = pygame.sprite.Group()


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
    response = requests.get(static_api, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return pygame.image.load(BytesIO(response.content))


def draw_map():
    screen.fill((155, 155, 155))
    map_file = get_map_png(ll=center, spn=(spn, spn), l=maps[map_type])
    screen.blit(map_file, (0, 0))
    all_sprites.draw(screen)


def main():
    global spn, center, map_type
    map_type_btn = Button((0, 452), "Схема", all_sprites)
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
        pygame.display.flip()

    pygame.quit()


main()
