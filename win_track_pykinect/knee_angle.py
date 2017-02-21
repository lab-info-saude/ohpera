"""
Specifies the various skeleton joints.
HipCenter = 0
Spine = 1
ShoulderCenter = 2
Head = 3
ShoulderLeft = 4
ElbowLeft = 5
WristLeft = 6
HandLeft = 7
ShoulderRight = 8
ElbowRight = 9
WristRight = 10
HandRight = 11
HipLeft = 12
KneeLeft = 13
AnkleLeft = 14
FootLeft = 15
HipRight = 16
KneeRight = 17
AnkleRight = 18
FootRight = 19
"""

from visual import *
import vpykinect
import numpy as np

def get_angles(KneeLeftPos, HipLeftPos, AnkleLeftPos):
    trans_a = HipLeftPos - KneeLeftPos
    trans_b = AnkleLeftPos - KneeLeftPos
    angles = np.arccos(np.sum(trans_a * trans_b, axis = 0)/(np.sqrt(np.sum(trans_a ** 2, axis = 0)) * np.sqrt(np.sum(trans_b ** 2, axis = 0))))

    return (np.pi -  angles) * (180/np.pi)



vpykinect.draw_sensor(frame())
skeleton = vpykinect.Skeleton(frame(visible=False))
while True:
    rate(120)
    skeleton.frame.visible = skeleton.update()
    if skeleton.frame.visible:
        # LEFT SIDE
        HipLeft  = skeleton.joints[12]
        KneeLeft = skeleton.joints[13]
        AnkleLeft = skeleton.joints[14]

        HipLeft.color = color.green
        KneeLeft.color = color.red
        AnkleLeft.color = color.green

        HipLeftPos = np.array([HipLeft.x, HipLeft.y, HipLeft.z])
        KneeLeftPos = np.array([KneeLeft.x, KneeLeft.y, KneeLeft.z])
        AnkleLeftPos = np.array([AnkleLeft.x, AnkleLeft.y, AnkleLeft.z])

        l_a = get_angles(np.array(KneeLeftPos).T, np.array(HipLeftPos).T,
        np.array(AnkleLeftPos).T)

        # RIGHT SIDE
        HipRight  = skeleton.joints[16]
        KneeRight = skeleton.joints[17]
        AnkleRight = skeleton.joints[18]

        HipRight.color = color.green
        KneeRight.color = color.red
        AnkleRight.color = color.green

        HipRightPos = np.array([HipRight.x, HipRight.y, HipRight.z])
        KneeRightPos = np.array([KneeRight.x, KneeRight.y, KneeRight.z])
        AnkleRightPos = np.array([AnkleRight.x, AnkleRight.y, AnkleRight.z])
        #print HipLeftPosPos
        #print('{} {} {}'.format(HipLeftPos.x, HipLeftPos.y, HipLeftPos.z))

        r_a = get_angles(np.array(KneeRightPos).T, np.array(HipRightPos).T,
        np.array(AnkleRightPos).T)


        print ('\nLeft Angle %.1f: ' % float(l_a))
        print ('\nRight Angle %.1f: ' % float(r_a))
