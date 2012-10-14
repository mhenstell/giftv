import os
import urllib2
import sh

new_gif_url = "http://www.gif.tv/gifs/"
gif_dir = "/Users/max/Sites/gifs"

def process_output(line): print(line)

class GifDownloader:

    def run ( self ):
        gifs = os.listdir(gif_dir)
        new_gif_loc = '%s.gif' % urllib2.urlopen(new_gif_url + "get.php").read()
        if new_gif_loc in gifs: return

        print "Downloading %s" % new_gif_loc

        new_gif = urllib2.urlopen(new_gif_url + new_gif_loc)
        
        gif_file = open(os.path.join(gif_dir, new_gif_loc), 'w')
        gif_file.write(new_gif.read())
        gif_file.close()

        try: print sh.Command(os.path.join(os.getcwd(), "fix_gif.sh"))(os.path.join(gif_dir, new_gif_loc), _err=process_output)
        except Exception as e: print e
        print "Downloaded %s" % new_gif_loc


gd = GifDownloader()

while True:
    gd.run()