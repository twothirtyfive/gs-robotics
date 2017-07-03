import picamera, cv2, sys
import numpy as np
from gopigo import *
from control import *
ix,iy,ex,ey = -1,-1,-1,-1
drawing = False
done = False
kp_initial = []

def main():
    queue = []
    camera = picamera.PiCamera()
    camera.capture('img.jpg')

    initial_img = cv2.imread('img.jpg')
    original = initial_img.copy()

    click_list = getXY(initial_img)

    cropped_hsv = crop_img(original, click_list, 'HSV')
    cropped_rgb = crop_img(original, click_list, 'RGB')

    lower_hsv,upper_hsv = myStats(cropped_hsv)
    lower_rgb, upper_rgb = myStats(cropped_rgb)

    hsv_bw_image = color_in_image(original, [lower_hsv,upper_hsv], 'HSV')
    rgb_bw_image = color_in_image(original, [lower_rgb,upper_rgb], 'RGB')

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow("image", np.hstack([rgb_bw_image, hsv_bw_image]))
    cv2.waitKey(0)
    cv2.destroyAllWindows

    keypoints = detect_blobs(rgb_bw_image, np.count_nonzero(rgb_bw_image))
    global kp_initial
    kp_initial = find_biggest_blob(keypoints)
    print "initial size: ",kp_initial.size
    print "initial point: ", kp_initial.pt
    ins = decision(kp_initial)
    queue.append(ins)

    k = 0
    while queue != []:
        if read_enc_status() == 0:
            instructions = queue.pop(0)
            maneuver(instructions)
        camera.capture('img'+ str(k) + '.jpg')
        img = cv2.imread('img' + str(k) + '.jpg')
        hsv_bw_image = color_in_image(img, [lower_hsv,upper_hsv], 'HSV')
        rgb_bw_image = color_in_image(img, [lower_rgb,upper_rgb], 'RGB')
        # cv2.imshow("image", np.hstack([rgb_bw_image, hsv_bw_image]))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows

        print np.count_nonzero(hsv_bw_image)
        bw_image = hsv_bw_image
        if np.count_nonzero(hsv_bw_image) == 0:
            bw_image = rgb_bw_image
        keypoints = detect_blobs(rgb_bw_image, np.count_nonzero(bw_image))

        kp = []
        kp = find_biggest_blob(keypoints)
        print "size: ",kp.size
        print "point: ",kp.pt
        ins = decision(kp)
        queue.append(ins)

        k += 1
        if not (70 <= kp.pt[0] <= 650):
            ins = decision(kp)
            queue.insert(0, ins)
        print queue

    #image is 1920x1080
    # for k in keypoints:
    #     print "pt: ",k.pt
    #     print "size: ",k.size
    #     print "angle: ", k.angle

def decision(kp):
    if kp == []:
        return 4,0
    x = kp.pt[0]
    if not 300 <= x <= 420:
        if x < 300:
            dif = (360-x)/12.
            return 0,dif
        else:
            dif = (x-360)/12.
            return 1,dif
    else:
        if kp.size < kp_initial.size:
            return 2,0
        elif kp.size > kp_initial.size:
            return 3,0
        else:
            return 4,0

def maneuver(instructions):
    set_speed(40)
    if instructions[0] == 0:
        turn('left', instructions[1])
    elif instructions[0] == 1:
        turn('right', instructions[1])
    elif instructions[0] == 2:
        fwd()
    elif instructions[0] == 3:
        bwd()
    elif instructions[0] == 4:
        stop()
    else:
        print "You done goofed."
        raise SystemExit

def find_biggest_blob(keypoints):
    if len(keypoints):
        big, size = keypoints[0], 0
        if len(keypoints) != 1:
            for k in keypoints:
                if k.size > size:
                    size = k.size
                    big = k
        return big
    return kp_initial

def detect_blobs(image, nz_count):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = False
    params.filterByConvexity = True
    params.filterByInertia = False
    params.minThreshold = 0
    params.maxThreshold = 256
    params.minArea = 30
    params.maxArea = image.size
    params.minConvexity = 0.7
    params.maxConvexity = 1.0

    reverse = 255-image
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(reverse)
    return keypoints


def myStats(cropped):
    con = 3.0
    mean,stdDv = cv2.meanStdDev(cropped)
    lower,upper = [],[]
    upper = mean + con*stdDv
    for m in range(3):
        if (255 - mean[m][0]) < con*stdDv[m][0]:
            upper[m][0] = 255
    lower = mean - con*stdDv
    for m in range(3):
        if mean[m][0] < con*stdDv[m][0]:
            lower[m][0] = 0

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

def crop_img(image, vertices, param):
    if param == 'HSV':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x_min,y_min = float("inf"), float("inf")
    x_max,y_max = float("-inf"), float("-inf")
    for v in vertices:
        if v[0] < x_min and v[1] < y_min:
            x_min,y_min = v[0],v[1]
        if v[0] > x_max and v[1] > y_max:
            x_max,y_max = v[0],v[1]
    cropped = image[y_min:y_max, x_min:x_max].copy()
    return cropped

def color_in_image(image, boundary, param):
    if param == 'HSV':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower, upper = boundary
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    print lower
    print upper

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    output[mask == 255] = [255,255,255]
    # retval, output = cv2.threshold(output, 1, 255, cv2.THRESH_BINARY)

    # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # cv2.imshow("image", np.hstack([image, output]))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows

    return mask

if __name__ == '__main__':
    main()
