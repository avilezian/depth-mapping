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

    max = np.max(img)
    min = np.min(img)
    print(f"Max pixel value: {max}")
    print(f"Min pixel value: {min}")

    npimg = np.array(img)

    def ordered_response(npimg):
        # do stuff
        return y
    
    def nosm(npimg):
        # do stuff
        return x

    

    d = np.abs(npimg - np.median(npimg))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zero(len(d))

    newimg = npimg[s<2.0]


    result = Image.fromarray((npimg).astype(np.uint8))

    result.save(self.destination)

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="filepath to Studio Camera Depth File")
parser.add_argument("destination", help="destination to save .bmp")
args = parser.parse_args()

if __name__ == "__main__":
    main(depthmapper(args.filepath, args.destination))