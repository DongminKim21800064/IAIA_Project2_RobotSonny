#!/usr/bin/env python3
#-*- coding:utf-8 -*- 

import indydcp_client as client
from tf.transformations import *
import copy
from math import tau
import sys
import cv2 as cv

class Indy10_move_with_CAM():

    def __init__(self) -> None:
        
        robot_ip = "192.168.0.8"    # 예시 STEP IP 주소
        robot_name = "NRMK-Indy10"   # IndyRP2의 경우 "NRMK-IndyRP2"
        self.indy = client.IndyDCPClient(robot_ip, robot_name) # indy 객체 생성

        self.indy.connect() # 로봇 연결

        # Setting 
        self.indy.set_joint_vel_level(9)     # 1 ~ 9
        self.indy.set_task_vel_level(9)     # 1 ~ 9

        deg = tau/360  # For example, entering 90*deg will output 90 degrees.

        self.target_joints_1 = [-10.0*deg,  -10.0*deg, 118.94*deg,   0*deg,  -18.82*deg,  0.08*deg ]     # Flag2
        self.target_joints_2 = [  0.0*deg,  -10.0*deg, 118.94*deg,   0*deg,  -18.82*deg,  0.08*deg ]     # Flag3
        self.target_joints_3 = [ 10.0*deg,  -10.0*deg, 118.94*deg,   0*deg,  -18.82*deg,  0.08*deg ]       # Flag4
        8

        self.target_joint_goal_safe = [-0.1*deg,-23.35*deg, 84.1*deg, 0.02*deg, 115.22*deg, 0.09*deg]     # @Flag4 --> Move safe loc
        self.target_joint_goal_grip = [0.09*deg, -27.2*deg, 133.2*deg, 0.02*deg, 65.64*deg, 0.09*deg] # @Flag4 --> Grip loc
        self.target_joint_end       = [0, 0, 45*deg, 0, 45*deg, 0] # @Flag4 --> Grip loc

        self.flag = 0
        self.pre_flag = 0
        self.vaccum_flag = 0
        self.robot_state = 0
        self.count = 0


    def move(self):
        # Robot Status
        status = self.indy.get_robot_status()
        print("[robot status]:", status)

        # Get Joint Pose
        joint_pos = self.indy.get_joint_pos() # [q1, q2, q3, q4, q5, q6]
        print("[current joint]:", joint_pos)

        # Move Joint to Absolute value
        targ_joint = copy.deepcopy(joint_pos)
        targ_joint[0] = joint_pos[0] - 45
        print("[target joint]:", targ_joint)
        self.indy.joint_move_to(targ_joint)

        # Wait
        status = self.indy.get_robot_status()
        while status['busy']:
            print(self.indy.get_joint_vel())
            status = self.indy.get_robot_status()
        
        print("[current joint]: ", self.indy.get_joint_pos()) # [q1, q2, q3, q4, q5, q6]

        # Move Joint to Relative value
        self.indy.joint_move_by([45, 0, 0, 0, 0, 0])

        # Wait
        status = self.indy.get_robot_status()
        while status['busy']:
            status = self.indy.get_robot_status()

        print("[current joint]: ", self.indy.get_joint_pos()) # [q1, q2, q3, q4, q5, q6]

        # Wait
        status = self.indy.get_robot_status()
        while status['busy']:
            status = self.indy.get_robot_status()

        print("[current joint]: ", self.indy.get_joint_pos()) # [q1, q2, q3, q4, q5, q6]

def main():



    # task position to Relative value
    print("[task] :", self.indy.get_task_pos()) # [x, y, z, u, v, w]
    self.indy.task_move_by([0, -0.1, 0, 0, 0, 0])
    
    # Wait
    status = self.indy.get_robot_status()
    while status['busy']:
        print(self.indy.get_task_vel())
        status = self.indy.get_robot_status()

    print("[task] :", self.indy.get_task_pos()) # [x, y, z, u, v, w]
    self.indy.task_move_by([0, 0.1, 0, 0, 0, 0])

    # Wait
    status = self.indy.get_robot_status()
    while status['busy']:
        status = self.indy.get_robot_status()

    print("[task] :", self.indy.get_task_pos()) # [x, y, z, u, v, w]

    self.indy.disconnect() # 연결 해제


if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        print("[ERROR]", e)