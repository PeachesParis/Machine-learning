import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Conv2D, Flatten, MaxPooling2D, Dense

#load dataset here
#-------------------

#use opencv to load pictures
def load_data():
 
 #empty list that will store images and corrosponding labeels
 images=[]
 labels=[]

 #line that will start a loop that will iterate over image in the pathfor img_path in dataset_path:
 img=cv2.imread(img_path)
 img=cv2.resize(img,(128,128))
 
 #adds every prosecessed images list
 images.append(img)

 #adding corrosponding labels
 labels.append(label)

 #converts images and labels to np.array and rteurns them
 return np.array(images), np.array(labels)
 
images,labels=load_data()
images=images/225.0 #normalize the image

#BUILD
#THE
#MODEL
#Convolutional Neural Network(CNN)
model= Sequential([
 
 #first convulution layer
   Conv2D(32, (3,3),
 activation='relu',
   input_shape=(128,128,3)),
   MaxPooling2D((2,2)),
 Conv2D(64,(3,3),
   activation='relu'),
   MaxPooling2D((2,2)),
   Flatten(), #converts the 2D into 1D vector

   # performs classification based on extracted data, outputs apobability
   Dense(1, activation='sigmoid')
])

#compile configures the model for trainning
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#Trainging model
model.fit(images, labels, epochs=10,
           validation_split=0.2)

#obstacle 
# detection in 
# real- life

def obstacle_detection(feed):
 
 #resizes to make sure it matches the input size shape
 img=cv2.resize(feed, (128,128)) 

 #expand dimension
 img=np.expand_dims(img, axis=0)/255.0

 prediction=model.predict(img)

 #compares the prediction threshold of 0.5 if less(false=no obstacle detection) more(True= obstacles detected)
 return prediction[0][0] > 0.5

 #incase of a vidoe feed

def video_cap(feed):
 
 #intialises video capture
 cam_feed=cv2.VideoCapture(0)

 #video will be opened and loop will run while vido capture is open
 while cam_feed.isOpened():
  
  #ret for status if cam_read was read succefully, and frame for actaul feed
    ret,feed=cam_feed.read()
    if not ret:
     break
 
  
  #function is called to check for obstacles
    if obstacle_detection(feed):
     print("obstacle has been detected")
    
    #display current frame fro the video capturer
    cv2.imshow('Feed', feed)

 #will wait for 2 millisecond and if any key press it will exit
    if cv2.waitKey(2) != -1:
     break

 #realses video capture and closes all onpenCV windows
 cam_feed.release()
 cv2.destroyAllWindows()


 
 
