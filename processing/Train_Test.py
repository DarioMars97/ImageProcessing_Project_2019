import cv2
import numpy as np
import operator
import os

MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

class ContourWithData():
    npaContour = None           # contour
    boundingRect = None         # bounding rect for contour
    intRectX = 0                # bounding rect top left corner x location
    intRectY = 0                # bounding rect top left corner y location
    intRectWidth = 0            # bounding rect width
    intRectHeight = 0           # bounding rect height
    fltArea = 0.0               # area of contour
    
    def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):                            # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False        # much better validity checking would be necessary
        return True
    

def Train_Test(imgname):
    allContoursWithData = []
    validContoursWithData = []
    
    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
    except:
        print( "error, unable to open classifications.txt, exiting program\n")
        os.system("pause")
        return
    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
    except:
        print( "error, unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
        return
    
    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
    kNearest = cv2.ml.KNearest_create()
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)
    imgTestingNumbers = cv2.imread(imgname)
    
    if imgTestingNumbers is None:                           
        print ("error: image not read from file \n\n")      
        os.system("pause")                                  
        return
    
    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)
    imgThresh = cv2.adaptiveThreshold(imgBlurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,17,2)
    imgThreshCopy = imgThresh.copy()
    imgContours,npaContours,npaHierarchy = cv2.findContours(imgThreshCopy,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for npaContour in npaContours:                             
        contourWithData = ContourWithData()                                             
        contourWithData.npaContour = npaContour                                         
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           
        allContoursWithData.append(contourWithData)
        
    for contourWithData in allContoursWithData:                
        if contourWithData.checkIfContourIsValid():             
            validContoursWithData.append(contourWithData)       
   
    validContoursWithData.sort(key = operator.attrgetter("intRectX"))
    strFinalString = ""
    
    for contourWithData in validContoursWithData:
        #cv2.rectangle(imgTestingNumbers,(contourWithData.intRectX,contourWithData.intRectY),(contourWithData.intRectX+contourWithData.intRectWidth,contourWithData.intRectY+contourWithData.intRectHeight),(0, 255, 0),2)
        
        imgROI = imgThresh[contourWithData.intRectY:contourWithData.intRectY+contourWithData.intRectHeight,contourWithData.intRectX:contourWithData.intRectX+contourWithData.intRectWidth]
        
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
        
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
        
        npaROIResized = np.float32(npaROIResized)
        
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)
        
        strCurrentChar = str(chr(int(npaResults[0][0])))   
        
        strFinalString = strFinalString + strCurrentChar
    
    return ("\n" + strFinalString + "\n")
                             
        
       
