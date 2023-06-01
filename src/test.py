import cv2
from Img2sketches import img2sketches

img_path = "../images/cat/n02123045_9.JPEG"
img = cv2.imread(img_path)
cv2.imshow("My Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
sketch = img2sketches(img)
print(sketch)
