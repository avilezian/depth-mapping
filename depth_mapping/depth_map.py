from PIL import Image
import numpy as np
from struct import unpack
from dataclasses import dataclass
import argparse

@dataclass
class depthmapper:
    filepath: str
    destination: str

    def __init__(self, filepath, destination):
        self.filepath = filepath
        self.destination = destination

        if not filepath:
            raise Exception("Need a filepath to image")
        
        if not destination:
            raise Exception("Need a destination for depth map")
        elif destination.split(".")[-1] != "bmp":
            raise Exception("Must use .bmp for extension")

def max_val(inputlist):
    """Returns max value from all values in a list of lists
    
    Args:
        inputlist: list of lists
        
    Returns:
        maxvalue: maximum value out of entire inputlist"""
    maxvalue = max([sublist[-1] for sublist in inputlist])
    return maxvalue

def main(self):
    """Takes in a Studio Camera Depth File and saves the depth map as a .bmp
    
    Args:
        self: depthmapper class with filepath and destination
        
    Returns:
        image saved as .bmp in destination"""
    
    f = open(self.filepath, mode='rb')
    magic = unpack('<i', f.read(4))[0]
    
    if magic != 55655:
        raise Exception("Magic number does not match Studio Camera Depth File")
    
    width = unpack('<h', f.read(2))[0]
    height = unpack('<h', f.read(2))[0]
    size = width * height

    print(f"Size of image is {size} pixels, with a width of {width} pixels and a height of {height} pixels")

    img = []
    
    for h in range(height):
        row = []
        for w in range(width):
            value = unpack('<f', f.read(4))[0]
            row.append(value)
        img.append(row)
    f.close()

    max = max_val(img)

    scaled_img = []

    for row in img:
        r = []
        for val in row:
            val = (val*255)/max
            r.append(val)
        scaled_img.append(r)

    npimg = np.array(scaled_img)

    result = Image.fromarray((npimg).astype(np.uint8))

    result.save(self.destination)

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="filepath to Studio Camera Depth File")
parser.add_argument("destination", help="destination to save .bmp")
args = parser.parse_args()

if __name__ == "__main__":
    main(depthmapper(args.filepath, args.destination))