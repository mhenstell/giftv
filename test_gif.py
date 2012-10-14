import pygame
from pygame.locals import *
import time
import urllib2
import GIFImage
import threading
import os
import sys
import sh
import random

size = width, height = 320, 240
new_gif_url = "http://www.gif.tv/gifs/"
gif_dir = "/Users/max/Sites/gifs"

image = None
screen = None
images = []
gifs = []



# class GifDownloader ( threading.Thread ):

#     def run ( self ):
#         print "Downloading a new gif!"
#         gifs = os.listdir(gif_dir)
#         new_gif_loc = '%s.gif' % urllib2.urlopen(new_gif_url + "get.php").read()
#         if new_gif_loc in gifs: return

#         new_gif = urllib2.urlopen(new_gif_url + new_gif_loc)
        
#         gif_file = open(os.path.join(gif_dir, new_gif_loc), 'w')
#         gif_file.write(new_gif.read())
#         gif_file.close()

#         try: print sh.Command(os.path.join(os.getcwd(), "fix_gif.sh"))(os.path.join(gif_dir, new_gif_loc), _err=process_output)
#         except Exception as e: print e
#         print "Downloaded %s" % new_gif_loc


def get_tiles(image):
    i = image.image
    i.seek(0)

    tiles = []

    try:
        tried = False
        while 1:
            if i.tile:
                tiles.append(i.tile[0][3])
                tried = False
                i.seek(i.tell()+1)
            else:
                if not tried:
                    i.seek(0)
                    tried = True
                else:
                    return "Error: could not locate metadata properly"
    except EOFError:
        pass
    return "Metadata: %s\n\t%s"%(set(tiles), i.info)

def load_image(filename):
    return GIFImage.GIFImage(filename)
    


def one_loop(image):
    global screen
    print "One loop for %s" % image.filename
    
    while image.cur != len(image.frames) - 2:
        screen.fill((255,255,255))
        image.render(screen, (0,0))
        pygame.display.flip()

    image.rewind()

def preload_gifs():
    
    # while True:
    #     gifs = os.listdir(gif_dir)
    #     if len(gifs) < 5: 
    #         GifDownloader().start()
    #         time.sleep(3)
    #     else: break
    random.shuffle(gifs)

    for x in range(0, 5):
        print "Preloading %s" % gifs[x]
        try: images.append(load_image(os.path.join(gif_dir, gifs[x])))
        except Exception as e:
            print "Error loading %s: %s" % (gifs[x], e)
            continue

def update_gifs():
    new_gifs = os.listdir(gif_dir)
    x = 0
    for gif in new_gifs:
        if x == 2: return
        if gif not in images: 
            print "Adding %s to images" % gif
            try: images[gif] = load_image(os.path.join(gif_dir, gif))
            except Exception as e:
                print "Error loading %s: %s" % (gif, e)
                continue
            x += 1


def main():
    global screen
    global gifs
    
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.NOFRAME)

    if len(sys.argv) > 1:
        while True:
            one_loop(load_image(os.path.join(gif_dir, sys.argv[1])))

    gifs = os.listdir(gif_dir)
    preload_gifs()

    while True:
        # GifDownloader().start()
        # GifDownloader().start()
        
        if len(images) > 0:
            image = images.pop()
            start_time = time.time()       
            while time.time() - start_time < 5:
                one_loop(image)
        else:
            preload_gifs()

while 1:
    main()
