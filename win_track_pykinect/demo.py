from visual import *
import vpykinect

vpykinect.draw_sensor(frame())
skeleton = vpykinect.Skeleton(frame(visible=False))
skeleton.frame.visible = False
raised = False

while True:
    rate(30)
    skeleton.frame.visible = skeleton.update()
    if skeleton.frame.visible:
        right_hand = skeleton.joints[11]
        right_shoulder = skeleton.joints[8]
        spine = skeleton.joints[1]
        if right_hand.y > right_shoulder.y and not raised:
            raised = True
            print('Recognized right hand wave.')
        elif right_hand.y < spine.y and raised:
            raised = False
    print skeleton.joints[vpykinect.JointId.HandRight.value].pos
