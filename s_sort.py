import argparse

parser = argparse.ArgumentParser()
parser.add_argument('indir', type=str, help='Input directory')
parser.add_argument('-outdir', type=str, default='output', help='Output directory')
args = parser.parse_args()
