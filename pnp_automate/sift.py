import cv2, numpy as np
from function import *

img1 = None
win_name = 'Camera Matching'
MIN_MATCH = 10


detector = cv2.SIFT_create()


cap = cv2.VideoCapture(0)              
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():       
    ret, frame = cap.read() 
    if img1 is None:  
        res = frame
    else:             
        img2 = frame
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
        kp1, desc1 = detector.detectAndCompute(gray1, None)
        kp2, desc2 = detector.detectAndCompute(gray2, None)
        
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(desc1, desc2)
        good_matches = sorted(matches, key=lambda x: x.distance)

        matchesMask = np.zeros(len(good_matches)).tolist()

        if len(good_matches) > MIN_MATCH: 
            
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ])
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ])
           
            homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5)
            accuracy=float(mask.sum()) / mask.size
            print("accuracy: %d/%d(%.2f%%)"% (mask.sum(), mask.size, accuracy))
            if mask.sum() > MIN_MATCH:  
                matchesMask = mask.ravel().tolist()
                pts = np.array(pts, dtype=np.float32).reshape((-1, 1, 2))
                dst = cv2.perspectiveTransform(pts,homography)
                print(dst)
                img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

            else:
                matchesMask = None

        try:
            res = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, \
                            matchesMask=matchesMask,
                            flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        except Exception as e:
            res = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None,
                            flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
                            
    cv2.imshow(win_name, res)
    key = cv2.waitKey(1)
    if key == 27:   
            break          
    elif key == ord(' '): 
        pts = get_four_points(frame)
        img1 = draw_quadrilateral(frame, pts)
else:
    print("can't open camera.")
cap.release()                          
cv2.destroyAllWindows()