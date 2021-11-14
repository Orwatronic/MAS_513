# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:56:18 2021

@author: Husam
"""

import cv2
import numpy as np
from realsense_depth import *
import pyrealsense2 as rs


point = (0,0)




# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))





width = 640 #512
height = 480 #512

#initialiaze the camera 
dc = DepthCamera()

while(True):
    
    #Capture frame-by-frame
    #ret, frame = cap.read()
    
    #Capture frome lidar camera
    ret,depth_frame,color_frame = dc.get_frame()
      #show_distanse from pixel
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())


      
      
    # Detecting objects
    blob = cv2.dnn.blobFromImage(color_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
     for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
            color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
            depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)
            depth_pixel = [center_x,center_y]
            distance= depth_frame.get_distance(center_x,center_y)
            depth_point = rs.rs2_deproject_pixel_to_point(color_intrin, depth_pixel, distance)
            # Rectangle coordinates
            x = int(center_x - w /2)#it was x-w and i changed it to x+w
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
     if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        #if label == 'chair':
        color = colors[class_ids[i]]
        color_image = cv2.rectangle(color_image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(color_image, label, (x, y + 30), font, 3, color, 3)
      #show coordinates(x,y,z)
        cv2.circle(color_image, [x,y],5, (0,0,255))
        cv2.circle(color_image, [x + w  ,y + h],5, (0,0,255))
        cv2.putText(color_image, "X = {}m".format(depth_point[0]), (x + w, y +h -80), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
        cv2.putText(color_image, "Y = {}m".format(depth_point[1]), (x+w, y+h - 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)      
        cv2.putText(color_image, "Z = {}m".format(distance), (x+w, y+h - 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
        print(label,depth_point[0],depth_point[1],distance)
    

    #Display the resulting frame
    cv2.imshow('black and white',color_image)#img_boxes
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()

#cv2.imshow("Image", frame)
#cv2.waitKey(0)
#cv2.destroyAllWindows()