import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('indir', type=str, help='Input directory')
parser.add_argument('-outdir', type=str, default='output', help='Output directory')
args = parser.parse_args()

new_size = (1, 1)

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

for filename in os.listdir(args.indir):
    file = os.path.join(args.indir, filename)
    if os.path.isfile(file):
        print('Processing {}'.format(file))
        img = Image.open(file)
        print(img.resize(new_size).getpixel((0, 0)))
