import cv2
import glob
import CombinePair
import JPEGEncoder as en

def combine():
    imagelist = sorted(glob.glob("temp/*.jpg"))

    result = en.compress(cv2.imread(imagelist[0]))
    #detector = cv2.xfeatures2d_SIFT.create()
    detector = cv2.xfeatures2d.SURF_create(300)

    for i in range(1, len(imagelist)):
        image = en.compress(cv2.imread(imagelist[i]))

        try:
            result = CombinePair.combine(result, image, detector)
            cv2.imwrite("results/int_res" + str(i) + ".jpg", result)
            print ("Stitched " + str(i + 1) + " Images")

        except Exception as e:
            print(e)
            print ("Fail " + str(i))
            #cv2.imwrite("results/int_res" + str(i) + ".JPG", result)

        h, w = result.shape[:2]

        if h > 4000 and w > 4000:

            if h > 4000:
                hx = 4000/h

                h = h*hx
                w = w*hx

            elif w > 4000:
                wx = 4000/w

                w = w*wx
                h = h*wx

            result = cv2.resize(result, (int(w), int(h)))



    return result
