#!/usr/bin/python

import sys
import pygame
from pygame.locals import *
from bitarray import bitarray
pygame.init()
pygame.font.init()
import pickle


size = width, height = 320, 240


## colors
black = [0,0,0]
white = [255,255,255]
grey  = [100,100,100]
red = [200,0,0]

## raster
sx = 16  # pixel breit
sy = 8   # pixel hoch
px = 1   # dicke der Linie
spacing = 15  # breite eines Pixel auf dem schirm
offx = 10   # offset des rasters
offy = 10   # offset des rasters

screen = pygame.display.set_mode(size)
images = []
image_idx = 0




def grid(screen, offx = 0, offy = 0):
    # horizontal
    for i in range(sy+1):
        pygame.draw.line(screen, grey, [offx, offy+(i*spacing)], [offx+(sx*spacing), offy+(i*spacing)], px )
    for i in range(sx+1):
        pygame.draw.line(screen, grey, [offx+(i*spacing), offy], [offx+(i*spacing), offy+(sy*spacing)], px )


def draw_pixel_to_grid(screen, x,y, offx = 0, offy = 0):
    x1 = offx+(spacing*(x))+px
    y1 = offy+(spacing*(y))+px
    w = spacing-1
    h = spacing-1
    #print("Draw position:", x,y)
    pygame.draw.rect(screen, red, [x1,y1,w,h], 0)

def click_in_grid(screen, scx,scy, offx = 0, offy = 0):
    x =  (scx - offx) / spacing
    y =  (scy - offy) / spacing
    return (int(x),int(y))

def draw_coord(screen, pos):
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("{}, {}".format(pos[0], pos[1]), 1, white)
        textpos = text.get_rect(centerx=screen.get_width()/2)
        screen.blit(text, textpos)
        #print ("Gridpos:", click_in_grid(screen, pos[0], pos[1], offx, offy))
    #print ("Pos:", pos)


def add_image(images):
    image = [False for x in range(sx*sy)]
    images.append(image)
    return images

def remove_image(images, image_num):
    del images[image_num]
    image_num -=1
    return images

def image_next():
    image_idx +=1
    image_idx = image_idx % len(images)

def image_prev():
    image_idx -=1
    if image_idx < 0:
        image_idx = 0

def copy_current_image(images, image_idx):
    images.insert(image_idx+1, images[image_idx])
    return images


def draw_image(screen, images, number=0):
    for y in range(sy):
        for x in range(sx):
            if images[number][y*sx+x]:
                draw_pixel_to_grid(screen, x, y, offx, offy)

def save_images(images, filename='test.h', pickle_name='test.pickle'):
    with open(filename, 'w') as f:
        f.write("static const unsigned char PROGMEM animation[] = {")
        for image in images:
            for x in range(8):
                b = bitarray(image[x:x+8])
                f.write(hex(int.from_bytes(b.tobytes(),  byteorder='little')))
                f.write(",")
        f.write("};")

    # write pickle
    with open(pickle_name, 'wb') as f:
        pickle.dump(images, f)

def load_images(filename='test.pickle'):
    with open(filename, 'rb') as f:
        images = pickle.load(f)
    return images


add_image(images)
try:
    print("Image {}/{}".format(image_idx, len(images)))
except:
    pass
while 1:
    screen.fill(black)
    grid(screen, 10,10)
    x,y = (0,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_coord(screen,  pygame.mouse.get_pos())
            scx, scy = event.pos
            x,y = click_in_grid(screen, scx, scy, offx=offx, offy=offy)
            images[image_idx][y*sx+x] = not images[image_idx][y*sx+x]
        if event.type == pygame.KEYDOWN:
            if event.unicode == 's':
                save_images(images)
            if event.unicode == 'l':
                images = load_images()
                print("images:", images)
            if event.unicode == '+':
                images = add_image(images)
            if event.unicode == '-':
                images = remove_image(images)
            if event.unicode == 'n':
                image_idx +=1
                image_idx = image_idx % len(images)
            if event.unicode == 'c':
                # copy current image
                images = copy_current_image(images, image_idx)
            if event.unicode == 'p':
                image_idx -=1
                if image_idx < 0:
                    image_idx = 0
            try:
                print("Image {}/{}".format(image_idx, len(images)))
            except:
                pass
    draw_image(screen, images, image_idx)
    ###draw_data(screen)
    pygame.display.flip()
