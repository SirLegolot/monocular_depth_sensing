import rospy
import sys
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import matplotlib.pyplot as plt
import numpy as np

def process_image(msg):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)


    # cv_image = (cv_image - np.min(cv_image)) / np.max(cv_image)
    # cv_image = (cv_image*255).astype(np.uint8)
    # cv_image = cv2.applyColorMap(cv_image, cv2.COLORMAP_JET)


    cv2.imshow("image",cv_image)
    cv2.waitKey(3)

if __name__ == '__main__':
    while not rospy.is_shutdown():
        rospy.init_node('image_sub')
        rospy.loginfo('image_sub node started')
        rospy.Subscriber("/camera/color/image_raw", Image, process_image)

        rospy.spin()