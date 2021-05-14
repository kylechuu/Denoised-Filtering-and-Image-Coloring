import numpy as np
import cv2
import math

class Coloring:


    def intensity_slicing(self, image, n_slices):
      #Convert greyscale image to color image using color slicing technique.
      #takes as input:
      #image: the grayscale input image
      #n_slices: number of slices

      #Steps:

      # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
      # 2. Randomly assign a color to each interval
      # 3. Create and output color image
      # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to

        rows, cols = image.shape
        look_up_table = []
        pixel_val = 0
        color_image = np.zeros((rows, cols, 3))

        for _ in range(n_slices+1):
            look_up_table.append((pixel_val, np.random.randint(0, 256, size=3)))
            pixel_val += int(256 / (n_slices + 1))

        # print(look_up_table)

        for row in range(rows):
            for col in range(cols):
                if image[row][col] > look_up_table[-1][0]:
                    color_image[row][col][0] = look_up_table[-1][1][0]
                    color_image[row][col][1] = look_up_table[-1][1][1]
                    color_image[row][col][2] = look_up_table[-1][1][2]
                else:
                    for i in range(len(look_up_table)-1):
                        if look_up_table[i][0] < image[row][col] < look_up_table[i+1][0]:
                            color_image[row][col][0] = look_up_table[i][1][0]
                            color_image[row][col][1] = look_up_table[i][1][1]
                            color_image[row][col][2] = look_up_table[i][1][2]

        return color_image


    def color_transformation(self,image, n_slices, theta):
      #Convert greyscale image to color image using color transformation technique.
      #takes as input:
      #image:  grayscale input image
      #colors: color array containing RGB values

      #Steps:
      # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
      # 2. create red values for each slice using 255*sin(slice + theta[0])
      #    similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
      # 3. Create and output color image
      # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to

      #returns color image

        rows, cols = image.shape
        look_up_table = []
        pixel_val = 0
        color_image = np.zeros((rows, cols, 3))

        for _ in range(n_slices + 1):
            look_up_table.append(pixel_val)
            pixel_val += int(256 / (n_slices + 1))

        for row in range(rows):
            for col in range(cols):
                if image[row][col] > look_up_table[-1]:
                    k = (look_up_table[-1] + look_up_table[-2])/2

                    color_image[row][col][0] = 255*math.sin(k + theta[0])
                    color_image[row][col][1] = 255*math.sin(k + theta[1])
                    color_image[row][col][2] = 255*math.sin(k + theta[2])
                else:
                    for i in range(len(look_up_table)-1):
                        if look_up_table[i] < image[row][col] < look_up_table[i+1]:
                            k = (look_up_table[i] + look_up_table[i+1]) / 2

                            color_image[row][col][0] = 255*math.sin(k + theta[0])
                            color_image[row][col][1] = 255*math.sin(k + theta[1])
                            color_image[row][col][2] = 255*math.sin(k + theta[2])

        return color_image


