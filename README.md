# PnP

## date
- created ```data.csv``` which has the images and the rotational and trasitional co-ordinates

## date
- Applied SIFT on the ```imgdata``` and created ```sift_img```
- used BF matcher to match the keypoints on 2 images in ```des_match.py```

## 13-11-24
- to get 6 points for dlt we have decided to get the best 6 points detected by sift. 
- also to get those points by masking so that the points which are of no intrest region are ignored.

## 15-11-24
- coded ```dlt_hardcode.py```
- while working on ```img1.jpg``` we got to know that there is only one plane so dlt fails on it..

## 16-11-24
- used ```img5.jpg and img4.jpg``` then the sift is giving uneven matches.
- 