import argparse
import glob
import os
import random
from os.path import basename, splitext

import numpy as np
import cv2
import math


def crop_image(source_image: np.ndarray, result_image: np.ndarray, shape: tuple) -> (np.ndarray, bool):
    w, h, channels = shape
    cropped_image = np.zeros(shape, np.uint8)
    while True:
        x_offset = random.randint(0, source_image.shape[0] - w)
        y_offset = random.randint(0, source_image.shape[1] - h)
        cropped_result_image = result_image[x_offset: x_offset + w, y_offset: y_offset + h]
        if not cropped_result_image[cropped_result_image > 0].any():
            continue
        is_vein = result_image[x_offset + round(shape[0] / 2), y_offset + round(shape[1] / 2)] / 255
        cropped_image = source_image[x_offset: x_offset + w, y_offset: y_offset + h]

        return cropped_image, cropped_result_image, is_vein


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--source',
                        type=str,
                        help='Path to full images',
                        default='test_files/full_images/*.jpg')
    parser.add_argument('-n',
                        '--number',
                        type=int,
                        help='Number of generated files',
                        default=1000)
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Path to output files',
                        default='test_files/cropped_images/')
    parser.add_argument('-i',
                        '--image-size',
                        type=int,
                        help='Cropped image size ',
                        default=28)
    parser.add_argument('-r',
                        '--save-result-images',
                        type=bool,
                        help='Write True to save black and white cropped result images',
                        default=False)
    args = parser.parse_args()
    save_result_images = args.save_result_images
    source_files = glob.glob(args.source)
    crop_per_file = int(math.ceil(int(args.number) / len(source_files)))
    w = h = args.image_size
    crop_shape = (w, h, 3)
    count = 0
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file_path in glob.glob(output_dir + "*.jpg"):
        os.remove(file_path)
    for file_path in source_files:
        full_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        full_image_filename = basename(file_path)
        output_image_filepath = glob.glob('test_files/full_results/' + splitext(full_image_filename)[0] + '*.png')[0]
        output_image = cv2.imread(output_image_filepath, cv2.IMREAD_GRAYSCALE)
        output_image = cv2.blur(output_image, (5, 5))
        for photo in range(crop_per_file):
            cropped_image, cropped_output_image, is_vein = crop_image(full_image, output_image, crop_shape)
            # save
            output_path = output_dir + str(count) + '_' + '%.2f' % is_vein + '.jpg'
            cv2.imwrite(output_path, cropped_image)
            if save_result_images:
                output_path = output_dir + str(count) + '_' + 'output' + '_' + '%.2f' % is_vein + '.jpg'
                cv2.imwrite(output_path, cropped_output_image)
            count += 1
            print(count, 'out of', args.number, 'path:', output_path)
            if count == args.number:
                break
        if count == args.number:
            break


if __name__ == '__main__':
    main()
