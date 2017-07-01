import picamera
import cv2
import numpy as np

def main():
    camera = picamera.PiCamera()
    camera.capture('img.jpg')

    img = cv2.imread('img.jpg',0)
    click_list = getXY(img)
    print click_list

list_of_clicks = []
def getXY(img):

   #define the event
   def getxy_callback(event, x, y, flags, param):
    global list_of_clicks
    if event == cv2.EVENT_LBUTTONDOWN :
       list_of_clicks.append([x,y])
       print "click point is...", (x,y)

   #Read the image
   print "Reading the image..."

   #Set mouse CallBack event
   cv2.namedWindow('image')
   cv2.setMouseCallback('image', getxy_callback)


    # show the image
   print "Please select the color by
      clicking on the screen..."
   cv2.imshow('image', img)
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   #obtain the matrix of the selected points
   print "The clicked points..."
   print list_of_clicks

   return list_of_clicks

if __name__ == '__main__':
    main()
