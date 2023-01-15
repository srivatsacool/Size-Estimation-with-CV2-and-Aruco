```python
import cv2 
import matplotlib.pyplot as plt
import imutils
import numpy as np
#plt.style.use('seaborn-white')
%matplotlib inline
```


```python
img = cv2.imread("phone.jpg")
```


```python
plt.imshow(img)
```




    <matplotlib.image.AxesImage at 0x1e370af34c0>




    
![png](README_files/README_2_1.png)
    



```python
# Resize and convert the image to grayscale and remove Gaussian noise
img = imutils.resize(img , width = 500)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
plt.imshow(gray)
```




    <matplotlib.image.AxesImage at 0x1e371161ff0>




    
![png](README_files/README_3_1.png)
    



```python
# perform edge detection by first dilating and then erosion to
# join broken boundaries of object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
plt.imshow(edged)
```




    <matplotlib.image.AxesImage at 0x1e3711dd240>




    
![png](README_files/README_4_1.png)
    



```python
# find contours in the edge map
cnts_ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts_)
im = np.expand_dims(edged, axis=2).repeat(3, axis=2) 
for k, _ in enumerate(cnts):
    im = cv2.drawContours(im, cnts, k, (0, 230, 255), 6)
plt.imshow(im)

```




    <matplotlib.image.AxesImage at 0x1e370e77fd0>




    
![png](README_files/README_5_1.png)
    



```python
img_ = img.copy()
for cnt in cnts_[0]:
    # Get rect
    x,y,w,h = cv2.boundingRect(cnt)
    im_STRAIGHT = cv2.rectangle(img_,(x,y),(x+w,y+h),(0,255,0),2)
    im_STRAIGHT = cv2.circle(img_, (int(x) ,int(y)) , 10, (0,255,9), -1)
    im_STRAIGHT = cv2.putText(img_ , f'Height : {h}' ,(int(x)-50 ,int(y)+50), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2 )
    im_STRAIGHT = cv2.putText(img_ , f'Width : {w}' ,(int(x)-50 ,int(y)+75), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2 )
plt.imshow(im_STRAIGHT)
```




    <matplotlib.image.AxesImage at 0x1e370ee7520>




    
![png](README_files/README_6_1.png)
    



```python
img__= img.copy()
for cnt in cnts_[0]:
    # Get rect
    rect = cv2.minAreaRect(cnt)
    (x, y), (w, h), angle = rect
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    print(f"The center for the obeject x: {x} y: {y} and Height: {h} , width: {w}")
    im_ROTATED = cv2.circle(img__, (int(x) ,int(y)) , 10, (0,255,9), -1)
    im_ROTATED = cv2.drawContours(img__,[box],0,(0,0,255),2)
    im_ROTATED = cv2.putText(img__ , f'Height : {h}' ,(int(x)-50 ,int(y)+50), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2 )
    im_ROTATED = cv2.putText(img__, f'Width : {w}' ,(int(x)-50 ,int(y)+75), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2 )
plt.imshow(im_ROTATED)
```

    The center for the obeject x: 270.8501892089844 y: 133.045654296875 and Height: 194.91464233398438 , width: 97.60841369628906
    




    <matplotlib.image.AxesImage at 0x1e370f4a620>




    
![png](README_files/README_7_2.png)
    


#  Finding the Aruco marker


```python
img2 = cv2.imread("phone_aruco_marker.jpg")
plt.imshow(img2)
```




    <matplotlib.image.AxesImage at 0x1e370fa7370>




    
![png](README_files/README_9_1.png)
    



```python
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameters = cv2.aruco.DetectorParameters()
print(parameters,aruco_dict)
```

    < cv2.aruco.DetectorParameters 000001E370A78FA0> < cv2.aruco.Dictionary 000001E370A5FC30>
    


```python
corners, _, _ = cv2.aruco.detectMarkers(img2, aruco_dict, parameters=parameters)
# Draw polygon around the marker
int_conrners =np.int0(corners)
int_conrners
```




    array([[[[777, 318],
             [632, 293],
             [656, 148],
             [803, 173]]]], dtype=int64)




```python
# plt.imshow(cv2.polylines(img2, int_conrners, True, (0, 255, 0), 7))
```




    <matplotlib.image.AxesImage at 0x1e371007ac0>




    
![png](README_files/README_12_1.png)
    



```python
# Aruco Perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)
print(f'The perimeter of the marker is = {aruco_perimeter}')
```

    The perimeter of the marker is = 590.5354766845703
    


```python
# Pixel to cm ratio
pixel_cm_ratio = aruco_perimeter / 20
#we are dividing the peri by 20 beacause each side on the marker is of 5cm ,i.e. 20cm
print(pixel_cm_ratio)
```

    29.526773834228514
    
