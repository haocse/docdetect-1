import cv2

import docdetect
import numpy as np
import sys
import math

def process(im, edge_detection):
    # im = cv2.bitwise_not(im)
    
    rgb_im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    edges = edge_detection.detectEdges(np.float32(rgb_im) / 255.0)

    # bold diate => rectangle. 
    orimap = edge_detection.computeOrientation(edges)
    edges = edge_detection.edgesNms(edges, orimap)
    # edges1 = np.uint8(edges)*255
    minV = 0
    maxV = np.max(edges) # how to deal with maxV => ... i don't know this number... 
    # print (maxV)
    thresh_val = 0.2 # edges usually has a intensity greater than 0.84 ????
    avg = thresh_val
	# apply average thresholding , if the max thresh in the image is > thresh_val
    # if maxV > thresh_val:
    #     avg = ( maxV - minV ) / 2 # * 3 ???? 
    # else:
    #     avg = thresh_val

    # avg = ( maxV - minV ) / 4
    
    # print (len(edges))
    # print (edges)
    # print ("------")
    # print (edges[edges > avg] )
    # print ("------")
    # print (edges[edges < avg])
    # print ("------")
    edges[edges > avg] = 255
    edges[edges <= avg] = 0
    # print (edges[edges <= avg])
    # edges.convertTo(cv2.COLOR_BGR2RGB)
    # np.clip(edges, 0, 255, out=edges)
    # edges1 = edges.astype('uint8')

    # edges[True] = 1
    # edges = edges*255/maxV

    # print (edges[edges <= maxV])
    edges1 = np.uint8(edges)

    
    
    cv2.imshow("Show by CV2",edges1)
    
    # cv2.imwrite("resizeimg.jpg",newimg)
    # edges = docdetect.detect_edges(im, blur_radius=7)
    
    lines_unique = docdetect.detect_lines(edges1, 30)

    num_pix_threshold = 80
    im2 = np.copy(im)
    linesP = cv2.HoughLinesP(edges1, 1, np.pi/180, 65, 45, 10, 10)
    
    if linesP is not None:
        ii = 0
        for line in linesP:
            for x1,y1,x2,y2 in line:
                cv2.line(im2, (x1,y1), (x2,y2), (255,0,255), 2)
                cv2.putText(im2, str(ii), (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,0,255), lineType=cv2.LINE_AA)
                print ("-----")
                print (str(ii))
                print (((x1,y1),  (x2,y2)))
                # cv2.putText(im2,"hiii",(x1,y1), font, 1, (200,0,0), 3, cv2.LINE_AA)
                #  m=tanθ
                # xx = [0,0]
                # mag, ang, x = cv2.cartToPolar([x1,x2],[y1,y2], xx),
                # if x2-x1 != 0 else 9999999

                # r=xsinθ+ycosθ 

                if x2-x1 != 0:
                    k = x2-x1
                    print (str(ii))
                    
                    pass
                else:
                    k = 99999
                    print ("error")
                # p1 = (x1,y1)
                # p2 = (x2,y2)
                rho = np.abs(x2*y1 - y2*x1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2 ) # cv2.norm(p2 - p1)
                theta = -math.atan2((x2 - x1) , (y2 - y1))

                if theta < 0: 
                    rho = -rho


                rho2 = x1*math.sin(theta) + y1*math.cos(theta)
                if rho*rho2 < 0:
                    rho = -rho
                print ("rho: " + str(rho) + "; theta: " + str(theta))
                print ("result: " + str(x1*math.sin(theta) + y1*math.cos(theta)))

                
                # m=y1-k*x1
                # # m = (y2-y1)/(x2-x1)
                # xSlope=-m/(k+(1/k))
                # ySlope=m/(pow(k,2)+1)

                # if math.atan2(ySlope, xSlope) < 0:
                #     theta = np.arctan2(ySlope, xSlope) + np.pi
                #     # rho = np.abs(-y1+m*x1)/math.sqrt(m*m + 1)
                #     rho = math.sqrt(pow(xSlope,2)+pow(ySlope,2))
                #     pass
                # else:
                #     theta = np.arctan2(ySlope, xSlope)
                #     # rho = np.abs(-y1+m*x1)/math.sqrt(m*m + 1)
                #     rho = math.sqrt(pow(xSlope,2)+pow(ySlope,2))
                #     pass



                # theta = math.degrees(math.atan2(y2-y1, x2-x1))
                


                # print ("rho")
                # print (rho)
                # print (theta)
                
                
                # if rho is NaN:
                #     pass
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho 
                y0 = b * rho


        
                x12 = int(x0 + 1000*(-b))
                y12 = int(y0 + 1000*(a))
                x22 = int(x0 - 1000*(-b))
                y22 = int(y0 - 1000*(a))

                cv2.putText(im2, str(ii), (int((x12+x22)/2+30),int((y12+y22)/2)+50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), lineType=cv2.LINE_AA)
                cv2.line(im2, (x12,y12), (x22,y22), (255,255,255), 2)
                # try:

                    
                # except:
                #     print ("except")
                #     cv2.putText(im2, str(ii), (x1+5,y1+5), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), lineType=cv2.LINE_AA)
                #     print (str(ii))

                #     pass

                # pass

            ii = ii + 1



    # print ("-lines_unique-")
    # print (lines_unique)
    for line in lines_unique:
        rho = line[0]
        theta =line[1]
        # print (rho)
        # print (theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho 
        y0 = b * rho 
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(im,  (x1,y1), (x2,y2), (0,0,255), 2)
        
    _intersections = docdetect.find_intersections(lines_unique, im)
    # print (_intersections)

    # for inter in _intersections:
    #     print (inter['lines'])
    #     # cv2.line(im, )
    #     pass

    cv2.imshow("im2", im2)

    # cv2.imshow("---", im)
    cv2.waitKey(1)
    return docdetect.find_quadrilaterals(_intersections)

def drawIntersections(im):

    return im

def draw(rects, im, debug=False):
    if len(rects) == 0:
        return im
    if debug:
        [draw_rect(im, rect, (0, 255, 0), 2) for rect in rects]
    best = max(rects, key=_area)
    if best:
        draw_rect(im, best)
    return im


def _area(rect):
    x, y = zip(*rect)
    width = max(x) - min(x)
    height = max(y) - min(y)
    return width * height


def draw_rect(im, rect, col=(255, 0, 0), thickness=5):
    [cv2.line(im, rect[i], rect[(i+1) % len(rect)], col, thickness=thickness) for i in range(len(rect))]
