import numpy as np
import math
import cv2
import statistics

class Filtering:

    def __init__(self, image, filter_name, filter_size, var=None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.filter_name = filter_name
        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        if filter_size % 2 != 0:
            self.filter_size = filter_size
        else:
            self.filter_size = filter_size - 1

        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""

        rows, cols = len(roi), len(roi[0])
        res = 0

        for row in roi:
            for pixel in row:
                res += pixel

        return int(res / (rows * cols))

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""

        res = 1
        rows, cols = len(roi), len(roi[0])

        for row in roi:
            for pixel in row:
                res *= pixel

        return pow(res, 1 / (rows * cols))

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""

        rows, cols = roi.shape
        pixel_list = []

        for row in range(rows):
            for col in range(cols):
                pixel_list.append(roi[row][col])

        local_var = statistics.variance(pixel_list)

        if self.global_var > local_var:
            return self.global_var

        return local_var

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""

        rows, cols = len(roi), len(roi[0])
        n = rows*cols
        pixel_list = []

        for row in roi:
            for ele in row:
                pixel_list.append(ele)

        pixel_list.sort()

        if n % 2 == 0:
            median1 = pixel_list[int(n / 2)]
            median2 = pixel_list[int(n / 2) - 1]
            median = (median1 + median2) / 2
        else:
            median = pixel_list[int(n / 2)]

        return int(median)

    def get_adaptive_median(self, roi):
        """Computes the harmonic filter
                        takes as input:
        kernel: a list/array of intensity values
        order: order paramter for the
        returns the harmonic mean value in the current kernel"""

        # this section is replaced by function is_impluse(self, roi, filsize, i, j)

        return 0

    def is_impluse(self, roi, fil_size, i, j):
        n = int(fil_size/2)

        rs, cs = roi.shape
        pixel_list = []

        for r in range(rs):
            for c in range(cs):
                pixel_list.append(roi[r][c])

        # max_pixel = np.amax(roi)
        max_pixel = max(pixel_list)
        # min_pixel = np.amin(roi)
        min_pixel = min(pixel_list)
        # median_pixel = int(np.median(roi))
        median_pixel = self.get_median(roi)

        if min_pixel < median_pixel < max_pixel:
            if min_pixel < self.image[i-n][j-n] < max_pixel:
                return self.image[i-n][j-n]
            return median_pixel
        else:
            fil_size += 2

        if fil_size <= self.S_max:
            for _ in range(n):
                pad_image = np.pad(roi, 1, mode='constant')

            return self.is_impluse(pad_image, fil_size, i, j)
        else:
            return median_pixel

    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """

        rows, cols = self.image.shape
        new_image = self.image.copy()
        pad_image = self.image.copy()
        n = int(self.filter_size / 2)

        for _ in range(n):
            pad_image = np.pad(pad_image, 1, mode='constant')


        for row in range(n, rows + 1):
            for col in range(n, cols + 1):
                if self.filter_name == "adaptive_median":
                    roi = pad_image[row - n: row + n + 1, col - n: col + n + 1]
                    new_image[row-n][col-n] = self.is_impluse(roi, self.filter_size, row-n, col-n)
                elif self.filter_name == "local_noise":
                    roi = pad_image[row - n: row + n + 1, col - n: col + n + 1]
                    new_image[row-n][col-n] = self.image[row-n][col-n] - (self.global_var / self.filter(roi))*(self.image[row-n][col-n] - self.get_arithmetic_mean(roi))
                else:
                    new_image[row-n][col-n] = self.filter(pad_image[row - n: row + n + 1, col - n: col + n + 1])

        return new_image



