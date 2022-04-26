#!/usr/bin/env python

import cv2, cv_bridge
import rospy
from sensor_msgs.msg import Image
import numpy as np
import os
import time

class Camera():
    def __init__(self):
        rospy.init_node('cam_node')
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback)
        self.rate = rospy.Rate(30)
        self.bridge = cv_bridge.CvBridge()

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.image =  np.asanyarray(image)

    def get_image(self):
        return self.image


if __name__ == '__main__':
    camera = Camera()

    #img = camera.get_image()
    for i in range(10):
        camera.rate.sleep()
    i = 1
    flag = True

    while not rospy.is_shutdown():
        path = os.path.join(os.path.expanduser('~'), 'ROS_Works', 'ForTensorLearn', 'Resources', '{}.png'.format(i))
        img = camera.get_image()
        
        c_time = time.time()
        if flag == False:
            cv2.imshow('Imaaageeee', img)
            cv2.waitKey(1)
        if flag == True:
            a = input()
            flag = False
            c_time = time.time()
        if time.time()-c_time>5:
            flag = True
            if a == 's':
                cv2.imwrite(path, img)
                i= i+1
                a = None
    cv2.destroyAllWindows()