import cv2
import numpy as np
import copy

image1 = cv2.imread("coin1.png")
image2 = cv2.imread("coin2.png")
image3 = cv2.imread("coin3.png")
image4 = cv2.imread("coin4.png")

def img_Mask(imagek):
    z = 31  # 31
    k = 70  # 65
    x = 98
    imagem = copy.deepcopy(imagek)
    hsv_image = cv2.cvtColor(imagem, cv2.COLOR_BGR2HLS)
    mask = np.logical_and((hsv_image[:, :, 0] > 23), (hsv_image[:, :, 0] < 50))
    mask = np.uint8(mask * 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (z, z))
    kernelD = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    kernelE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (x, x))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernelD, iterations=2)
    mask = cv2.erode(mask, kernelE, iterations=1)
    return mask

def get_penny_mask(imagein):
    a = 31 # 50
    b = 65 # 10
    #c = 70 # 1
    imageR = copy.deepcopy(imagein)
    hsl_image_r = cv2.cvtColor(imageR, cv2.COLOR_BGR2HLS)
    mask_r = np.logical_and((hsl_image_r[:, :, 0] > 13), (hsl_image_r[:, :, 0] < 130))
    mask_r = np.uint8(mask_r * 255)
    rkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (a, a))
    rkernel_d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (b, b))
    #rkernel_e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (c, c))
    mask_r = cv2.erode(mask_r, rkernel, iterations=1)
    mask_r = cv2.dilate(mask_r, rkernel_d, iterations=2)
    mask_r = cv2.erode(mask_r, rkernel_d, iterations=2)
    imageR[mask_r == 255, :] = 0
    mask_r = 255 - mask_r
    return mask_r

def get_img(mask, image):
    image[mask == 255, :] = 0
    return image

def Circle(mask,image):
    mask2 = cv2.GaussianBlur(mask, (5, 5), 0, 0)
    circles = cv2.HoughCircles(mask2, cv2.HOUGH_GRADIENT, 1, 45, param1=50, param2=30, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))
    return circles

def get_P_amount(img):
    pm = get_penny_mask(img)
    p = Circle(pm, img)
    pc = p.shape[1]
    return pc

def get_amount(img):
    im = img_Mask(img)
    pm = get_penny_mask(img)
    sm = im+pm
    p = Circle(pm, img)
    pc = p.shape[1]
    s = Circle(sm, img)[0]
    c1 = s[:,2]
    for i in range(len(c1)):
        if c1[i] <= 85:
            pc = pc+10
        elif 96 <= c1[i]:
            pc = pc+25
        elif  85 < c1[i] < 96:
            pc = pc+5
    return pc

def out(imag):
    money = get_amount(imag)/100
    print('{:.2f}'.format(money))
    output = 255 - img_Mask(imag)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1.1
    font_color = (255,255,255)
    font_thickness = 2
    text = '$'+'{:.2f}'.format(money)
    x,y = 10,50
    output = cv2.putText(output, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    return output

cv2.imwrite("1.png", out(image1))
cv2.imwrite("2.png", out(image2))
cv2.imwrite("3.png", out(image3))
cv2.imwrite("4.png", out(image4))


cv2.imshow("1", out(image1))
cv2.imshow("2", out(image2))
cv2.imshow("3", out(image3))
cv2.imshow("4", out(image4))
cv2.waitKey(0)
cv2.destroyAllWindows()


