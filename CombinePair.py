import cv2
import math
import numpy as np
import geometry as gm
import copy
import utilities as util
import glob
from PIL import Image
import random

def combine(image1, image2, detector):
    img1 = image1# cv2.resize(image1, (0,0), fx=0.5, fy=0.5)
    img2 = image2# cv2.resize(image2, (0,0), fx=0.5, fy=0.5)

    img1_gs = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2_gs = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

    # Find the key points and descriptors with SIFT -------------------------------#

    sift =detector# cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1_gs,None)
    kp2, des2 = sift.detectAndCompute(img2_gs,None)

    # Generate matching keypoints in images
    match = cv2.BFMatcher()
    matches = match.knnMatch(des1,des2,k=2)

    good = [] 
    for m,n in matches: # Filter for good matches
        if m.distance < 0.7 * n.distance:
            good.append(m)

    # Stitching ------------------------------------------------------------------#

    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    else:
        print("Not enough matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))
    height1,width1 = image1.shape[:2]
    height2,width2 = image2.shape[:2]

    corners1 = np.float32(([0,0],[0,height1],[width1,height1],[width1,0]))
    corners2 = np.float32(([0,0],[0,height2],[width2,height2],[width2,0]))

    warpedCorners2 = np.zeros((4,2))

    for i in range(0,4):
        cornerX = corners2[i,0]
        cornerY = corners2[i,1]
        warpedCorners2[i,0] = (M[0,0]*cornerX + M[0,1]*cornerY + M[0,2])/(M[2,0]*cornerX + M[2,1]*cornerY + M[2,2])
        warpedCorners2[i,1] = (M[1,0]*cornerX + M[1,1]*cornerY + M[1,2])/(M[2,0]*cornerX + M[2,1]*cornerY + M[2,2])

    allCorners = np.concatenate((corners1, warpedCorners2),axis=0)


    [xMin, yMin] = np.int32(allCorners.min(axis=0).ravel() - 0.5)
    [xMax, yMax] = np.int32(allCorners.max(axis=0).ravel() + 0.5)


    dst = cv2.warpPerspective(img1,M,(xMax-xMin, yMax-yMin))
    dst[0:img2.shape[0],0:img2.shape[1]] = img2
    result = dst


    return result
