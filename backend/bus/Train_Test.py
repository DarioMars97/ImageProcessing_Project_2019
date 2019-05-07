import cv2
import numpy as np
import operator
import imutils
import os
from django.conf import settings
from .models import Image
import base64

MIN_CONTOUR_AREA = 700
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


class ContourWithData:
    npaContour = None  # contour
    boundingRect = None  # bounding rect for contour
    intRectX = 0  # bounding rect top left corner x location
    intRectY = 0  # bounding rect top left corner y location
    intRectWidth = 0  # bounding rect width
    intRectHeight = 0  # bounding rect height
    fltArea = 0.0  # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):  # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):  # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False  # much better validity checking would be necessary
        return True


def prepNum(img):
    
    img = imutils.resize(img,width=500,height=500)
    kernel = np.ones((3,3),np.uint8)
    img1 = img.copy()
    gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(gray)
    blurred = cv2.GaussianBlur(gray,(7,7),0)
    thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2) 
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnt_areas=[]
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > 800:
            cnt_areas.append((area,cnt))
    cnt_areas.sort(key=operator.itemgetter(0),reverse=True)
    num_cnts = len(cnt_areas)
    if num_cnts < 3:
        cnt_areas = cnt_areas[:num_cnts]
    else:
        cnt_areas = cnt_areas[:3]
    
    for cnt in cnt_areas:
        cv2.drawContours(mask,[cnt[1]] , 0, (255,255,255), 2)
        
    (x,y) = np.where(mask == 255)
    (topx,topy) = (np.min(x),np.min(y))
    (bottomx,bottomy) = (np.max(x),np.max(y))
    out = img[topx:bottomx+1,topy:bottomy+1]
    gray = cv2.cvtColor(out,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(7,7),0)
    thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) 
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) 
    return closing


def detect_numbers(file_data=False, string_data=False):
    allContoursWithData = []
    validContoursWithData = []

    try:
        file_path = os.path.join(settings.STATIC_ROOT, 'classifications.txt')
        npaClassifications = np.loadtxt(file_path, np.float32)
    except:
        return "error, unable to open classifications.txt, exiting program"



    try:
        file_path = os.path.join(settings.STATIC_ROOT, 'flattened_images.txt')
        npaFlattenedImages = np.loadtxt(file_path, np.float32)
    except:
        return "error, unable to open flattened_images.txt, exiting program"
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
    kNearest = cv2.ml.KNearest_create()
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    imgTestingNumbers = None
    if file_data:
        image = Image.objects.latest("id")
        image = image.image.path
        imgTestingNumbers = cv2.imread(image)
    elif string_data:
        image = Image.objects.latest("id")
        image = image.text
        nparr = np.fromstring(base64.b64decode(image), np.uint8)
        imgTestingNumbers = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if imgTestingNumbers is None:
        return "error: image not read from file"
    # end if


    # imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)
    imgGray = prepNum(imgTestingNumbers)
    kernel = np.ones((1, 1), np.uint8)
    # dilated = cv2.dilate(imgTestingNumbers, kernel, iterations=1)
    # eroded = cv2.erode(dilated, kernel, iterations=1)
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)  # blur

    imgThresh = cv2.adaptiveThreshold(imgBlurred,
                                      255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV,
                                      11,
                                      2)

    imgThreshCopy = imgThresh.copy()

    npaContours, _ = cv2.findContours(imgThreshCopy,
                                      cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)

    for npaContour in npaContours:  # for each contour
        contourWithData = ContourWithData()
        contourWithData.npaContour = npaContour
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)
        allContoursWithData.append(contourWithData)
    # end for

    for contourWithData in allContoursWithData:
        if contourWithData.checkIfContourIsValid():
            validContoursWithData.append(contourWithData)
        # end if
    # end for

    validContoursWithData.sort(key=operator.attrgetter("intRectX"))

    strFinalString = ""

    for contourWithData in validContoursWithData:
        cv2.rectangle(imgTestingNumbers,
                      (contourWithData.intRectX, contourWithData.intRectY),
                      (contourWithData.intRectX + contourWithData.intRectWidth,
                       contourWithData.intRectY + contourWithData.intRectHeight),
                      (0, 255, 0),
                      2)

        imgROI = imgThresh[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                 contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
        npaROIResized = np.float32(npaROIResized)
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=1)
        strCurrentChar = str(chr(int(npaResults[0][0])))
        if strCurrentChar == ' ':
            strCurrentChar = ''
        strFinalString = strFinalString + strCurrentChar

    return strFinalString
