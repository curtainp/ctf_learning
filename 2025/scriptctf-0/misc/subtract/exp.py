from PIL import Image
import re, numpy as np
from collections import Counter

width = height = 500
data = open('dist/coordinates.txt').read()
pairs = re.findall(r"\((\d+),\s*(\d+)\)", data)
coordinates = [(int(x), int(y)) for x, y in pairs]
count_coordinates = Counter(coordinates)

img_data = np.zeros((width, height), dtype=np.uint8)
for (x, y), cts in count_coordinates.items():
    if cts == 1:
        img_data[y, x] = 255    # if x, y the result image will rotate by 90 degrees
Image.fromarray(img_data).save("odd_coordinates.png")
