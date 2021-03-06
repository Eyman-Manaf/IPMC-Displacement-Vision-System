# import necessary modules
import math  # access to mathematical functions
import cv2  # access to OpenCV library
from scipy.spatial import distance as dist  # access to distance matrix computation to calculate Euclidean distance
import glob  # used to locate file directory


def main():
    # Create the necessary data structures and variables
    measure_disp = []  # list to store displacement values
    measure_angle = []  # list to store angle values
    width = 50  # width of the reference circle in mm

    # REFERENCE IMAGE #
    image = cv2.imread(path_to_image)  # read initial image/frame
    # image = cv2.imread("C:\\Users\\UserName\\Path_To_File\\FileName.png")
    # image formats supported by cv2.imread includes .jpg .jpeg .png .tiff .tif and many more
    # check OpenCV documentation for full list https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert image to grayscale
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # apply Gaussian Blur to remove noise

    dst, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)  # obtain image threshold
    cnts, hier = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find threshold contours

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)  # sort contours by area in descending order
    ipmc = cnts[1]  # setting ipmc as second-largest contour
    refcircle = cnts[0]  # setting refcircle as largest contour

    extBot = tuple(ipmc[ipmc[:, :, 1].argmax()][0])  # find ref bottommost point of IPMC - max y-value
    extTop = tuple(ipmc[ipmc[:, :, 1].argmin()][0])  # find ref topmost point of IPMC - min y-value

    a = dist.euclidean(extTop, extBot)  # euclidean distance between bottommost and topmost point

    extLeftRef = tuple(refcircle[refcircle[:, :, 0].argmin()][0])  # find leftmost point on the ref circle - min x-value
    extRightRef = tuple(
        refcircle[refcircle[:, :, 0].argmax()][0])  # find rightmost point on the ref circle - max x-value

    dR = dist.euclidean(extLeftRef,
                        extRightRef)  # euclidean dist between the leftmost and rightmost pts on the ref circle
    pixel_to_mm = dR / width  # calculate pixelsPerMetric value

    # SUBSEQUENT IMAGES #
    images = glob.glob(path_to_images)  # subsequent images directory
    # images = glob.glob("C:\\Users\\UserName\\Path_To_File\\FileName*.png")
    # glob.glob returns a possibly-empty list of path names that match pathname
    # the '*' matches zero or more characters in a segment of a name
    # in this case it will return all .png images with the prefix 'FileName'
    # to return all .png images, glob.glob("C:\\Users\\UserName\\Path_To_File\\*.png")

    for fname in images:
        image2 = cv2.imread(fname)  # read images

        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)  # convert image to grayscale
        gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)  # apply Gaussian Blur to remove noise

        dst, thresh = cv2.threshold(gray2, 120, 255, cv2.THRESH_BINARY_INV)  # obtain image threshold
        cnts2, hier = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find threshold contours

        cnts2 = sorted(cnts2, key=cv2.contourArea, reverse=True)  # sort contours by area in descending order
        ipmc2 = cnts2[1]  # setting ipmc2 as second-largest contour

        extBot2 = tuple(ipmc2[ipmc2[:, :, 1].argmax()][0])  # find bottommost point of IPMC in the new frame
        b = dist.euclidean(extTop, extBot2)  # euclidean pixel dist between IPMC bottommost point and ref topmost point
        c = dist.euclidean(extBot2,
                           extBot)  # Euclidean pixel dist between IPMC bottommost point and ref bottommost point
        d2 = c / pixel_to_mm  # convert to real-world value
        measure_disp.append(d2)  # add value to list

        # law of cosines to calculate angle
        x = (a * a) + (b * b) - (c * c)
        y = (2 * a * b)
        angle_gamma = math.acos(x / y)  # calculating arc cosine
        angle_gamma = math.degrees(angle_gamma)  # convert to degrees
        measure_angle.append(angle_gamma)  # add value to list

    # write to file the displacement data
    file = open("Displacement.txt", "w+")  # create new text file
    for item in measure_disp:
        file.write("%s\n" % item)  # write list with new line
    file.close()

    # write to file the angle data
    file = open("Angle.txt", "w+")  # create new text file
    for item in measure_angle:
        file.write("%s\n" % item)  # write list with new line
    file.close()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

# The code was written and tested using PyCharm 2022.1.1 (Community Edition)
# The following is a full list of packages installed along with their respective versions
# setuptools    60.2.0
# pip           21.3.1
# opencv-python 4.5.5.64
# numpy	        1.22.4
# scipy	        1.8.1
# wheel	        0.37.1
# Distance      0.1.3
