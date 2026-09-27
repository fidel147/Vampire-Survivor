import pygame
from os.path import abspath, dirname, join
from os import walk
from random import uniform, randint, choice
from math import atan2, degrees
from pytmx.util_pygame import load_pygame

PROJECT_ROOT = dirname(dirname(abspath(__file__)))

def asset_path(*parts):
    return join(PROJECT_ROOT, *parts)

window_config = {
    'width': 1280,
    'height': 650,
    'title': "vampire hunt".title(),
    'color': 'blue'
}

tile_config = {
    'size': 64,
    'map': asset_path('data', 'maps', 'world.tmx'),
}

player_config = {
    'image': asset_path('images', 'player', 'down', '0.png'),
    'speed': 400,
    'image_path': (asset_path('images', 'player'),),
    'animation_speed': 5,
    'width': 300,
    'height': 70,
    'color_start' : 'blue',
    'color_end' : 'red',
}

gun_config = {
    'image': asset_path('images', 'gun', 'gun.png'),
    'distance': 140,

}

bullet_config = {
    'image' : asset_path('images', 'gun', 'bullet.png'),
    'cooldown' : 100,
    'distance' : 50,
    'speed': 1200,
    'lifetime': 1000,
}

enemy_config = {
    'animation_speed' : 6,
    'frame_images' : asset_path('images', 'enemies'),
    'speed' : 300,
    'timer' : 300,
    'death_duration' : 400,
}

audio = {
    'shoot': asset_path('audio', 'shoot.wav'),
    'impact' : asset_path('audio', 'impact.ogg'),
    'music' : asset_path('audio', 'music.wav'),
}