import cv2

import docdetect
import numpy as np
import sys

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
    thresh_val = 0.9
    # avg = thresh_val
	# apply average thresholding , if the max thresh in the image is > thresh_val
    if maxV > thresh_val:
        avg = ( maxV - minV ) / 2 # * 3 ???? 
    else:
        avg = thresh_val

    # avg = ( maxV - minV ) / 4
    
    print (len(edges))
    print (edges)
    print ("------")
    print (edges[edges > avg] )
    print ("------")
    print (edges[edges < avg])
    print ("------")
    edges[edges > avg] = 255
    print (edges[edges > avg])
    print ("------")
    edges[edges <= avg] = 0
    print (edges[edges <= avg])
    # edges.convertTo(cv2.COLOR_BGR2RGB)
    # np.clip(edges, 0, 255, out=edges)
    # edges1 = edges.astype('uint8')
    edges1 = np.uint8(edges)
    cv2.imshow("Show by CV2",edges1)
    cv2.waitKey(1)
    # cv2.imwrite("resizeimg.jpg",newimg)
    # edges = docdetect.detect_edges(im, blur_radius=7)
    
    lines_unique = docdetect.detect_lines(edges1)
    _intersections = docdetect.find_intersections(lines_unique, im)
    return docdetect.find_quadrilaterals(_intersections)


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
