import pyqrcode
from PIL import Image
import random
import os

os.system("ffmpeg -i Trailer.mp4 -vf fps=60 frames/%d.png")

qr = pyqrcode.create('SEE{W3lc0m3_t0_SEETF_95c42d3be1cb93cce8241235529ad96f8e0e1c12}')
pixels = qr.text().splitlines()

used = []

x, y = 0, 0
for row in pixels:
    print(y)

    for bw in row:
        # Make an image with the pixel

        filename = "frames/{}.png".format(4434 - random.randint(0, 53 * 53))
        while filename in used:
            filename = "frames/{}.png".format(4434 - random.randint(0, 53 * 53))
        used.append(filename)

        img = Image.open(filename)

        if bw == '0':
            # Only add the white pixels
            # Enlarge by 3x
            for i in range(3):
                for j in range(3):
                    img.putpixel((1920 - 53 * 3 + x * 3 + i, y * 3 + j), (255, 255, 255, 255))

        img.save(filename)
        print(filename)

        x += 1
    x = 0
    y += 1

os.system("ffmpeg -framerate 60 -i 'frames/%d.png' -c:v libx264 -pix_fmt yuv420p out.mp4")
os.system("ffmpeg -i out.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4")