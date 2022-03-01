"""
Useful links:
http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html

https://idorobotics.com/2021/03/08/extracting-ros-bag-files-to-python/


"""
import rosbag
import rospy
import os
import sys
import cv2
from cv_bridge import CvBridge
import matplotlib.pyplot as plt

class Args:
	"""
	Things that can be arguments. For now its just rosbag
	"""
	rosbag_name = None

def parseArgs():
	"""
	Parse the arguments.
	"""
	args = Args()
	if len(sys.argv) < 2:
		print("Usage: python read_rgbd.py <rosbag>")
		sys.exit(1)
	args.rosbag_name = sys.argv[1]
	return args

def parseBag(args):
	"""
	Parses the bag from the argument.
	"""
	bag = rosbag.Bag(args.rosbag_name)
	bridge = CvBridge()

	i=0
	for topic, msg, t in bag.read_messages():
		if i > 4:
			break

		print("Msg %d:" % i)
		print(topic, type(msg))
		print("width: %d\nheight: %d\nencoding: %s\nstep: %d" % (int(msg.width), int(msg.height), msg.encoding, int(msg.step)))

		cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
		print(cv_image.dtype)
		print(cv_image.shape)
		# plt.hist(cv_image.ravel(), bins=100)
		if topic == "/camera/color/image_raw":
			plt.imshow(cv_image)
		else:
			plt.imshow(cv_image, cmap=plt.cm.gray)
		plt.show()

		i+=1
		print(" ")
		
		

if __name__ == "__main__":
	args = parseArgs()
	parseBag(args)
