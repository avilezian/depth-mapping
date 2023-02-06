import numpy as np
from struct import *
import os
from matplotlib import pyplot as plt
from PIL import Image

f = open("StaryuDepth", "rb")
magic = unpack('<i', f.read(4))[0]
width = unpack('<h', f.read(2))[0]
height = unpack('<h', f.read(2))[0]
size = width * height

img = []

for w in range(height):
    row = []
    for h in range(width):
        value = unpack('<f', f.read(4))[0]
        row.append(value)
    img.append(row)
f.close()

def max_val(inputlist):
    return max([sublist[-1] for sublist in inputlist])

max = max_val(img)

scaled_img = []

for row in img:
    r = []
    for val in row:
        val = val/max
        r.append(val)
    scaled_img.append(r)

#flat_img = [item for sublist in scaled_img for item in sublist]

packed = pack("f", *(item for sublist in scaled_img for item in sublist))
print(packed)
print("MAGIC = ", magic)
print("IMAGE WIDTH = ", width)
print("IMAGE HEIGHT = ", height)
print("IMAGE SIZE = ", size)

plt.imshow(scaled_img, interpolation='nearest')
plt.show()


