import numpy as np
import imutils
from imutils import contours
import cv2
import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="Size Estimation with OpenCV",
    page_icon="🔤",
    layout = "wide",
    initial_sidebar_state="expanded")

def img_pre_process(img):
    # convert BGR image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # remove Gaussian noise from the image
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # sort the contours from left-to-right and initialize the
    (cnts, _) = contours.sort_contours(cnts)
    dis3.image(edged)
    # cv2.imshow('processsed img' , edged)
    
    # print(cnts,_)
    return cnts
    
def ArucoMarker(img , size_of_one_side = 5 , total_markers = 50 , draw = True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco, f'DICT_{size_of_one_side}X{size_of_one_side}_{total_markers}')
    #print(key)
    #Load the dictionary that was used to generate the markers.
    arucoDict = cv2.aruco.getPredefinedDictionary(key)
    # Initialize the detector parameters using default values
    arucoParam = cv2.aruco.DetectorParameters()
    # Detect the markers
    bboxs, ids, rejected = cv2.aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    corners = np.intp(bboxs)
    if draw ==True:
        marker_img = cv2.polylines(img, corners, True, (0, 255, 0), 7)
        dis2.image(marker_img)
        # cv2.imshow('marker', marker_img )
    
    return  corners
 
def process_img(img , MARKER_SIDE_SIZE , TOT_NO_MARKERS, SHOW_MARKER ,MESUREMENT_TYPE):
      
        cnts  = img_pre_process(img)
        corners_of_marker = ArucoMarker(img , MARKER_SIDE_SIZE, TOT_NO_MARKERS ,SHOW_MARKER)
        print(corners_of_marker)
        pixelsPerMetric = None
        perimeter_of_marker = None
        if len(corners_of_marker)!= 0 :
            perimeter_of_marker = cv2.arcLength(corners_of_marker[0], True)
            if MESUREMENT_TYPE =="Inch in":
                pixelsPerMetric = perimeter_of_marker / ((MARKER_SIDE_SIZE * 0.393701)*4)
            elif MESUREMENT_TYPE == "Feet ft":
                pixelsPerMetric = perimeter_of_marker / ((MARKER_SIDE_SIZE * 0.0328084)*4)
                print(pixelsPerMetric)
            else:
                pixelsPerMetric = perimeter_of_marker / (MARKER_SIDE_SIZE*4)
        else:
            pixelsPerMetric = 38.0
        # loop over the contours individually   
        for cnt in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(cnt) < 2000:
                continue
            rect = cv2.minAreaRect(cnt)                         
            (x, y), (w, h), angle = rect

            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = w /pixelsPerMetric
            object_height = h / pixelsPerMetric       
            
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            
            img = cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            img = cv2.polylines(img, [box], True, (255, 0, 0), 2)
            img = cv2.putText(img, "Width {} {}".format(round(object_width, 1) ,  MESUREMENT_TYPE.split(" ")[-1]), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            img = cv2.putText(img, "Height {} {}".format(round(object_height, 1) ,  MESUREMENT_TYPE.split(" ")[-1] ), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            dis1.image(img)
            # cv2.imshow('result' , img)
            # cv2.waitKey(0)


if __name__=='__main__':
    
    
    st.markdown("""
            <style>
                .sidebar .sidebar-content {
                    width: 375px;
                }
                .big-font {
                    font-size:80px;
                    font-weight : 1000;
                }
                .small-font {
                    font-size:40px;
                    font-weight : 700;
                    color : #b3b3b3 ; 
                }
                .MuiGrid-item{
                    font-size:19px;
                }
                .css-1yy6isu p{
                    font-size:25px;
                }
                .st-dx{
                    font-size :18px;
                }
                .css-1fv8s86 p{
                    font-size:18px;
                }
            </style>""", unsafe_allow_html=True)

    st.markdown('<p ><center class="big-font">Size Estimation with Aruco marker and OpenCV</center></p>', unsafe_allow_html=True)
    st.markdown('<p ><center class="small-font">Made by :- Srivatsa Gorti</center></p>', unsafe_allow_html=True)
    st.markdown("""---""")
    # st.markdown('<p> My GitHub 📖: https://github.com/srivatsacool </p>', unsafe_allow_html=True)
    st.subheader("Breif Description :")
    st.markdown("""
                - Detection based on **:blue['OpenCV']**, with help of Aruco marker .
                - Main reason of using aruco marker is beacuse it can help with the detection of depth in the image.
                - Detection of **:red[Aruco Marker]** is done via the cv2. aruco submodule (i.e., we don't need additional Python packages).
                - More details in **:green[GitHub]** Repo :- .
                """)
    
    dis1_img = Image.open('images/dis_1.png')
    dis2_img = Image.open('images/dis2.png')
    dis3_img = Image.open('images/dis3.png')
    
    col1, col2 = st.columns([3, 1])
    dis1 = col1.image(dis1_img)
    col2.text("Aruco Marker Detector :")
    dis2 = col2.image(dis2_img)
    col2.markdown("""---""")
    col2.text("Contour Processed Image :")
    dis3 = col2.image(dis3_img)
    
    with st.sidebar:
        FILE_TYPE = st.radio("Detection On :-",('Image', 'Video' , "Webcam"))
        SHOW_MARKER = st.checkbox("Show the processed image :",value = True)
        MESUREMENT_TYPE = st.radio("Mesurment to use :-",('Centimeter cm', 'Inch in' , "Feet ft"))
        st.markdown("""---""")
        SOURCE = "phone_aruco_marker.jpg"
        UPLOAD = st.file_uploader("Choose a file (Supports only .mp4 , .jpg )" , type = ['jpg','mp4'])
        EXAMPLES = st.selectbox('How would you like to be contacted?',options = ("phone_aruco_marker.jpg" ,'phone.jpg', 'Home phone', 'Mobile phone') , index = 0)
        if UPLOAD != None:
            if FILE_TYPE=='Image':
                st.image(UPLOAD)
                SOURCE = UPLOAD.name
            elif FILE_TYPE =='Video':
                SOURCE = UPLOAD.name
                st.text(UPLOAD)
                st.video(open(SOURCE,'rb').read())
            elif FILE_TYPE == 'Webcam':
                SOURCE = 0 
        else:
            SOURCE = EXAMPLES
            if FILE_TYPE=='Image':
                st.image(SOURCE)
            elif FILE_TYPE =='Video':
                st.video(open(SOURCE,'rb').read())
            st.text(SOURCE)
            
        MARKER_SIDE_SIZE = st.slider("Aruco Marker Size ( One side )", min_value = 0, max_value=50, value=5, step=5)
        TOT_NO_MARKERS =  st.slider("Number of Aruco Marker : ", min_value = 0, max_value=200, value=50, step=10)
        
        
    st.markdown("----", unsafe_allow_html=True)
    columns = st.columns((2, 1, 2))
    STARTING_POINT = columns[1].button('Start !!')
    # if FILE_TYPE =="Video":
    #     FPS = st.text("To see the FPS , press 'Start' !!")
    st.markdown("----", unsafe_allow_html=True)
    
    if STARTING_POINT:
        if FILE_TYPE =='Image':
            img = cv2.imread(SOURCE)
            process_img(img , MARKER_SIDE_SIZE , TOT_NO_MARKERS, SHOW_MARKER , MESUREMENT_TYPE)
            
        elif FILE_TYPE =='Video':
            cap = cv2.VideoCapture(SOURCE)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) 
            while True:
                _,img = cap.read()
                process_img(img , MARKER_SIDE_SIZE , TOT_NO_MARKERS, SHOW_MARKER,MESUREMENT_TYPE)      
        
        elif FILE_TYPE =='Webcam / Mobile Camera':
            cap = cv2.VideoCapture(SOURCE)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) 
            while True:
                _,img = cap.read()
                process_img(img , MARKER_SIDE_SIZE , TOT_NO_MARKERS, SHOW_MARKER, MESUREMENT_TYPE)    
                
cv2.destroyAllWindows()
            