import argparse
import logging
import math
import os

from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('-indir', type=str, default='test-dataset', help='Input directory')
parser.add_argument('-outdir', type=str, default='output', help='Output directory')
args = parser.parse_args()

logging.basicConfig(filename="mylog.log", filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def color_diff(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)


def sort(c_list, base_color):
    logging.info('\nSorting by color {}'.format(base_color))
    for key in sorted(c_list.keys(), key=lambda k: color_diff(c_list[k], base_color)):
        logging.info('{}: {}'.format(key, c_list[key]))
    return sorted(c_list.items(), key=lambda x: color_diff(x[1], base_color))


new_size = (1, 1)

'''Значения взяты из Wikipedia'''
red = 255, 0, 0
orange = 255, 165, 0
yellow = 255, 255, 0
green = 0, 255, 0
cyan = 0, 255, 255
blue = 0, 0, 255
violet = 128, 0, 255
'''---------------------------'''

red_list = {}
orange_list = {}
yellow_list = {}
green_list = {}
cyan_list = {}
blue_list = {}
violet_list = {}

s_colors = [red, orange, yellow, green, cyan, blue, violet]
colors_names = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'violet']
img_lists = [red_list, orange_list, yellow_list, green_list, cyan_list, blue_list, violet_list]
try:
    if len(os.listdir(args.indir)) == 0:
        logging.error('No images in input directory')
        print('No images in input directory')
        exit(1)
    for filename in os.listdir(args.indir):
        file = os.path.join(args.indir, filename)
        if os.path.isfile(file):
            logging.info('\nProcessing {}'.format(file))
            img = Image.open(file)
            rgb = img.resize(new_size).getpixel((0, 0))
            logging.info('RGB: {}'.format(rgb))

            min_diff = 999999999
            min_index = 0
            for i, color in enumerate(s_colors):
                diff = color_diff(rgb, color)
                if diff < min_diff:
                    min_diff = diff
                    min_index = i
            logging.info('Closest color: {}'.format(s_colors[min_index]))
            img_lists[min_index][file] = rgb
except FileNotFoundError:
    logging.error('Input directory not found')
    print('Input directory does not exist. Create \'test-dataset\' directory and put images there'
          ' or use -indir argument.')
    exit(1)

print('Sorted images:')
for i, color in enumerate(s_colors):
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    j = 0
    img_lists[i] = sort(img_lists[i], color)
    logging.info('\nColor: {}'.format(color))
    print('\nColor: {}'.format(color))
    for file, rgb in img_lists[i]:
        logging.info('File: {}'.format(file))
        print('File: {}'.format(file))
        logging.info('RGB: {}'.format(rgb))
        print('RGB: {}'.format(rgb))
        img = Image.open(file)
        img.save(
            os.path.join(args.outdir, str(i) + '_' + str(j) + '_' + colors_names[i] + '_' + os.path.basename(file)))
        j += 1
logging.info('\nDone')
