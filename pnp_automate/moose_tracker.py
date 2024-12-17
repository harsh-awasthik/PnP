import cv2
def get_box(img):
    bbox = cv2.selectROI("Tracking", img, True)
    return bbox

def draw_box(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3, 1)


def main():
    tracker = cv2.legacy.TrackerMOSSE_create()

    img1 = cv2.imread("RealsenceImages/img0.jpg")
    bbox = get_box(img1)
    tracker.init(img1, bbox)

    
    img2 = cv2.imread("RealsenceImages/img2.jpg")

    success, bbox = tracker.update(img2)

    draw_box(img2, bbox)
    cv2.imshow("Image with Box", img1)
    cv2.imshow("Img2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()