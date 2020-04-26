import argparse
import os

from PIL import Image

IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')


def crop_resize(srcdst):
    src, dst = srcdst
    try:
        im = Image.open(src)
        if im.size[0] * 480. / 640. < im.size[1]:
            start = int(im.size[1] - im.size[0] * 480. / 640.) // 2
            end = start + int(im.size[0] * 480. / 640.)
            region = (0, start, im.size[0], end)
        else:
            start = int(im.size[0] - im.size[1] * 640. / 480.) // 2
            end = start + int(im.size[1] * 640. / 480.)
            region = (start, 0, end, im.size[1])
        im.crop(region).resize((640, 480), resample=Image.BILINEAR).save(dst)
    except:
        print('Skip', src)


def main(args):
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    files = os.listdir(args.input)
    units = [(os.path.join(args.input, im), os.path.join(args.output,  os.path.splitext(im)[0] + '.png'))
             for im in files if os.path.splitext(im)[-1][1:].lower() in IMAGE_EXTENSIONS]
    print('Number of images:', len(units), 'out of', len(files), ' files')
    for unit in units:
        crop_resize(unit)


def parse_args():
    parser = argparse.ArgumentParser(description='Image crop and resize')
    parser.add_argument('-i', '--input', dest='input')
    parser.add_argument('-o', '--output', dest='output')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
