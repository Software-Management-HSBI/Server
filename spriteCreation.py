import math
import random


# Erstellt Trees und Billboards in zufaelligen Abstaenden
@staticmethod
def create_obstacles(segments):
    for i in range(0, len(segments), random.choice([50, 75, 100, 125])):
        direction = random.choice([1, -1])
        add_sprite(segments, i, create_tree(), direction)
        add_sprite(segments, i, create_billboard(), -direction)
        
# Erstellt die NPC-Autos und gibt ihnen zufaellige Position, zufaellige Sprites und zufaellige Geschwindigkeit
@staticmethod
def create_bots(car_amount, segments, segmentLength, maxSpeed):
    for n in range(car_amount):
        offset = random.random() * random_choice([-0.5, 0.5])
        z = math.floor(random.random() * len(segments) * segmentLength)
        sprite = get_car()
        speed = maxSpeed / 4 + random.random() * maxSpeed / 2
        car = {"offset": offset, "z": z, "sprite": sprite, "speed": speed, "percent": 0}
        segment = Util.which_segment(z, segments, segmentLength)
        segment["cars"].append(car)
        cars.append(car)
    return cars

# Hilfsmethode, um Strassenhindernisse einfacher hinzuzufuegen
@staticmethod
def add_sprite(segments, n, sprite, offset):
    segments[n]["sprites"].append({"source": sprite, "offset": offset})

@staticmethod
def get_car():
    i = random.randint(0, 3)
    if i == 0:
        car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}
    elif i == 1:
        car = {"asset": "assets/npc/car02.png", "width": 80, "height": 59}
    elif i == 2:
        car = {"asset": "assets/npc/car03.png", "width": 88, "height": 55}
    elif i == 3:
        car = {"asset": "assets/npc/car04.png", "width": 80, "height": 57}
    else:
        car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}
    return car

@staticmethod
def create_tree():
    i = random.randint(0, 2)
    if i == 0:
        tree = {"asset": "assets/tree/tree01.png", "width": 360, "height": 360}
    elif i == 1:
        tree = {"asset": "assets/tree/tree02.png", "width": 215, "height": 540}
    elif i == 2:
        tree = {"asset": "assets/tree/tree03.png", "width": 282, "height": 295}
    else:
        tree = {"asset": "assets/tree/tree01.png", "width": 360, "height": 360}
    return tree

@staticmethod
def create_billboard():
    i = random.randint(0, 8)
    if i == 0:
        billboard = {"asset": "assets/billboard/BetterCallSus.jpg", "width": 360, "height": 360, "offset": -1}
    elif i == 1:
        billboard = {"asset": "assets/billboard/billboard02.png", "width": 360, "height": 360, "offset": 1}
    elif i == 2:
        billboard = {"asset": "assets/billboard/billboard03.png", "width": 360, "height": 360, "offset": -1}
    elif i == 3:
        billboard = {"asset": "assets/billboard/billboard04.png", "width": 360, "height": 360, "offset": 1}
    elif i == 4:
        billboard = {"asset": "assets/billboard/billboard05.png", "width": 360, "height": 360, "offset": -1}
    elif i == 5:
        billboard = {"asset": "assets/billboard/billboard06.png", "width": 360, "height": 360, "offset": 1}
    elif i == 6:
        billboard = {"asset": "assets/billboard/billboard07.png", "width": 360, "height": 360, "offset": -1}
    elif i == 7:
        billboard = {"asset": "assets/billboard/billboard08.png", "width": 360, "height": 360, "offset": 1}
    elif i == 8:
        billboard = {"asset": "assets/billboard/billboard09.png", "width": 360, "height": 360, "offset": -1}
    else:
        billboard = {"asset": "assets/billboard/BetterCallSus.jpg", "width": 360, "height": 360, "offset": 1}
    return billboard

@staticmethod
def random_choice(options):
    return options[Util.random_int(0, len(options) - 1)]

@staticmethod
def which_segment(n, segments, segmentLength):
    return segments[math.floor(n / segmentLength) % len(segments)]