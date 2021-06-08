import ExifData, XMPData
import glob
from PIL import Image
import os
import AttitudeData

#input = open("datasets/imageData.txt","w+")

'''
:param fileName: Name of the pose data file in string form e.g. "datasets/imageData.txt"
:param imageDirectory: Name of the directory where images arer stored in string form e.g. "datasets/images/"
:return: dataMatrix: A NumPy ndArray contaning all of the pose data. Each row stores 6 floats containing pose information in XYZYPR form
allImages: A Python List of NumPy ndArrays containing images.
'''


def write():
    # pass

    input = open("datasets/imageData.txt","w+")
    input.close()

    input = open("datasets/imageData.txt","a+")


    for image in sorted(glob.glob('datasets/images/*')):
        # exif_data = ExifData.get_exif_data(Image.open(image))
        # lat, lon = ExifData.get_lat_lon(exif_data)

        # alt, roll, yaw, pitch = XMPData.xmp(image)
        exif_dict = AttitudeData.get_exif_info(image)
        lon, lat, alt = exif_dict['Longitude'],exif_dict['Latitude'],exif_dict['Altitude']
        yaw, pitch, roll = exif_dict['Yaw'], exif_dict['Pitch'], exif_dict['Roll']

        # print lon, lat, alt, yaw, pitch, roll
        st = (os.path.basename(image)) + "," + str(float(lon)) + "," + str(float(lat)) + "," + str(float(alt)) + "," + str(float(yaw)) + "," + str(float(pitch)) + "," + str(float(roll)) + "\n"
        # st = (os.path.basename(image)) + "," + str(float(0)) + "," + str(float(0)) + "," + str(float(0)) + "," + str(float(0)) + "," + str(float(0)) + "," + str(float(0)) + "\n"
        input.write(st)

    input.close()

#write()
