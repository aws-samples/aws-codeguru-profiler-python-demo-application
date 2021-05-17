# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from skimage import io, exposure
from skimage import img_as_ubyte
from skimage.color import rgb2gray, rgba2rgb


class ImageEditor:
    @staticmethod
    def brighten_image(source_filename, target_filename):
        image = io.imread(source_filename)
        brightened_image = exposure.adjust_gamma(image, 0.1)
        io.imsave(fname=target_filename, arr=img_as_ubyte(brightened_image))

    @staticmethod
    def monochrome(source_filename, target_filename):
        image = io.imread(source_filename)
        image_grey = rgb2gray(rgba2rgb(image))
        io.imsave(fname=target_filename, arr=img_as_ubyte(image_grey))
