import cv2
import geometry as gm
import glob

def changePerspective(imageList, dataMatrix):

    images = sorted(glob.glob("temp/*.jpg"))
    print ("Warping Perspective of Images Now")

    for i in range(0,len(images)):
        image = cv2.imread(images[i])
        image = image[::2, ::2, :]

        M = gm.computeUnRotMatrix(dataMatrix[i,:])
        correctedImage = gm.warpPerspectiveWithPadding(image,M)

        cv2.imwrite("temp/" + str(i).zfill(4) + ".jpg", correctedImage)

    print("Done Warping Perspective")
