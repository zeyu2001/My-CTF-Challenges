from PIL import Image
import os

# ffmpeg -i trimmed.mp4 -vf fps=60 solve/%d.png
res = Image.open("solve/1.png")

res = res.convert("RGBA")
filenames = os.listdir("./solve")
total = len(filenames)

i = 0
for img_filename in filenames:
    print("{0:.2f}%".format(i / total * 100), img_filename)

    img = Image.open(f"./solve/{img_filename}")

    whitest = []

    for x in range(img.width - 53 * 3, img.width):
        for y in range(53 * 3):
            pix = img.getpixel((x, y))

            # Get the 9 whitest pixels
            if len(whitest) < 9:
                whitest.append({'pix': pix, 'x': x, 'y': y})
            else:
                curr_min_idx = 0
                curr_min = 255 * 3
                for j in range(9):
                    if sum(whitest[j]['pix'][:3]) < curr_min:
                        curr_min_idx = j
                        curr_min = sum(whitest[j]['pix'][:3])
                
                if sum(pix[:3]) > curr_min:
                    whitest[curr_min_idx] = {'pix': pix, 'x': x, 'y': y}

    for pix in whitest:
        res.putpixel((pix['x'], pix['y']), (255, 255, 255, 255))

    i += 1

res.save("new.png","PNG")