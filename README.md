# PnP Progress Log

## date
- Created `data.csv` with images and rotational/translational coordinates.

## date
- Applied SIFT to `imgdata` to create `sift_img`.
- Used BF matcher for keypoint matching in `des_match.py`.

## 13-11-24
- Chose 6 best SIFT-detected points for DLT.
- Used masking to ignore non-interest regions.

## 15-11-24
- Implemented `dlt_hardcode.py`.
- Found DLT fails on `img1.jpg` due to a single plane.

## 16-11-24
- Tested `img5.jpg` and `img4.jpg`, observed uneven SIFT matches.
- Fixed masking issues on `img4.jpg` and manually marked keypoints.
- Filtered keypoints with distances < 20px.
- Planned 3D point calculation for DLT in `dlt_hardcode.py`.

## 18-11-24
- Calculated 6 best 3D coordinates from SIFT.
- Applied DLT using `dlt_chatgpt.py` and a GitHub-sourced `dlt.py`.
