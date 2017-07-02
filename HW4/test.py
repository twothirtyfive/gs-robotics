import picamera
import cv2
import numpy as np
ix,iy,ex,ey = -1,-1,-1,-1
drawing = False
done = False
def main():
    camera = picamera.PiCamera()
    camera.capture('img.jpg')

    img = cv2.imread('img.jpg')
    original = img.copy()
    click_list = getXY(img)

    cropped = crop_img(original, click_list)
    display_image(cropped)
    lower,upper = myStats(cropped)
    print lower
    print upper
    f_image = color_in_image(original, [lower,upper])

def myStats(cropped):
    mean,stdDv = cv2.meanStdDev(cropped)
    lower = mean - 2*stdDv
    upper = mean + 2*stdDv
    low = [lower[0][0],lower[1][0],lower[2][0]]
    up = [upper[0][0],upper[1][0],upper[2][0]]
    return low,up


list_of_clicks = []
def getXY(img):
   #define the event
    def getxy_callback(event, x, y, flags, param):
        global ix,iy,drawing,done,ex,ey
        if event == cv2.EVENT_LBUTTONDOWN :
            drawing = True
            ix,iy = x,y
            print "click point is...", (x,y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,140,0),1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            done = True
            ex,ey = x,y
            cv2.rectangle(img,(ix,iy),(x,y),(0,140,0),1)

   #Read the image
    print "Reading the image..."

   #Set mouse CallBack event
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', getxy_callback)
    while not done:
        cv2.imshow('image', img)
        cv2.waitKey(1)
    # show the image


    cv2.destroyAllWindows()
    global ix,iy,ex,ey
    list_of_clicks.append((ix,iy))
    list_of_clicks.append((ix,ey))
    list_of_clicks.append((ex,iy))
    list_of_clicks.append((ex,ey))

   #obtain the matrix of the selected points
    print "The clicked points..."
    print list_of_clicks

    return list_of_clicks

def display_image(img):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def crop_img(image, vertices):
    x_min,y_min = float("inf"), float("inf")
    x_max,y_max = float("-inf"), float("-inf")
    for v in vertices:
        if v[0] < x_min and v[1] < y_min:
            x_min,y_min = v[0],v[1]
        if v[0] > x_max and v[1] > y_max:
            x_max,y_max = v[0],v[1]
    cropped = image[y_min:y_max, x_min:x_max].copy()
    return cropped

def color_in_image(image, boundary):
    lower, upper = boundary
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    print lower
    print upper

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    output[mask == 255] = [255,255,255]

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow("image", np.hstack([image, output]))
    cv2.waitKey(0)
    cv2.destroyAllWindows

    return output

if __name__ == '__main__':
    main()
