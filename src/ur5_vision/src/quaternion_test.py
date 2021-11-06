#! /usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from tf.transformations import quaternion_from_euler
import csv

moveit_commander.roscpp_initialize(sys.argv)  #Initializing moveit_commander                  
rospy.init_node('move_group_python_interface_tutorial', anonymous=True) #Creating the node
robot = moveit_commander.RobotCommander() #choosing the right robot

arm_group = moveit_commander.MoveGroupCommander("manipulator")
#Put the arm in the --- position
arm_group.set_named_target("up")
plan1 = arm_group.go()

with open('/home/orwah/catkin_ws/src/ur5_vision/src/coord.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print(line)
        x=line[0]
        y=line[1]
        z=line[2]
        x=float(x)
        y=float(y)
        z=float(z)

# Pose Position
pose_goal = geometry_msgs.msg.Pose()
pose_goal.position.x = x
pose_goal.position.y = y
pose_goal.position.z = z

# Pose Orientation
pose_goal.orientation.x = 0.4
pose_goal.orientation.y = 0.1
pose_goal.orientation.z = 0.4
pose_goal.orientation.w = 1

arm_group.set_pose_target(pose_goal)
plan1 = arm_group.go(wait=True)

rospy.sleep(10)
moveit_commander.rosccp_shutdown()