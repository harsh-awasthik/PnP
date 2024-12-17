import cv2, numpy as np
from function import *

img1 = None
win_name = 'Camera Matching'
MIN_MATCH = 10


detector = cv2.SIFT_create()

#camera matrix of the realsence camera
camera_matrix = np.array([[675.537322,0.000000,311.191300],
                          [0.000000,677.852071,221.610964],
                          [0, 0, 1]])

dist_coeffs = np.zeros((4, 1)) #Assuming no distortion
gate_dimensions = (18, 24)  # in (x, y) cm

object_points = np.array([[0, 0, 0],  # Origin as the top-left of the box/gate
                          [gate_dimensions[0], 0, 0],
                          [gate_dimensions[0], gate_dimensions[1], 0],
                          [0, gate_dimensions[1], 0]], dtype=np.float32)

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


        #For Rotational Vectors
        line1 = f"Yaw = NULL, Pitch = NULL, Roll = NULL"

        #For transational Vectors
        line2 = f"x = NULL, y=NULL"

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
            
                #Solving pnp line 60-79
                image_points = dst.reshape(-1, 2)
                success, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_P3P)
                
                #For Rotational Vectors
                R, _ = cv2.Rodrigues(rvec)
                yaw, pitch, roll = rotational_to_euler(R)
                line1 = f"Yaw = {yaw}, Pitch = {pitch}, Roll = {roll}"

                #For transational Vectors
                line2 = f"x = {tvec[0]}, y={tvec[1]}"

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
                            
        else:
            # Overlay the text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            color = (255, 255, 255)
            x = res.shape[1] - 200  
            y = 20  

            cv2.putText(res, line1, (x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)
            cv2.putText(res, line2, (x, y + 20), font, font_scale, color, font_thickness, cv2.LINE_AA)

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