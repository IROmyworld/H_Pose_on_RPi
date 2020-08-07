#
#   Headpose Estimation Capture
#   Edited by IRO
#   Last Update: 26.5.2020
#

from __future__ import print_function
from imutils.video import PiVideoStream
import argparse
import cv2
import LEDControl as LED
import headpose


def main(args):
    
    # Initiate Webcam Stream
    cap = PiVideoStream(src=0).start()

    # Initialize head pose detection
    hpe = headpose.HeadposeEstimation(args["landmark_type"], args["landmark_predictor"])
    headpose.t.add_stage('fpsnf')
    headpose.t.add_stage('fpsyf')
    
    LED.LEDSetup()
    frame_num = 1
    headpose.t.tic('elapsed')
    while True:
        
        headpose.t.tic('tot')
        print('\rFrame: %d' % frame_num, end='')
        headpose.t.tic('cap')
        # Capture the frame
        frame = cap.read()
        
        print(', cap: %.2f' % headpose.t.toc('cap'), end='ms')
        frame = cv2.flip(frame, 1)
        
        # Carry out the Headpose Estimation
        frame, angles = hpe.process_image(frame)
        LED.LEDOutput(angles,[5,10])

        # Display the resulting frame
        if args['disp'] == True: cv2.imshow('frame', frame)
        
        fps = 1000 / headpose.t.toc('tot')
        if angles == None:
            headpose.t.update_min_max('fpsnf', fps)
            print(', fpsnf: %.2f' % fps, end='')
        else:
            headpose.t.update_min_max('fpsyf', fps)
            print(', fpsyf: %.2f' % fps, end='')
            
        if cv2.waitKey(1) & 0xFF == ord('q') or frame_num == args['max_frame_num']:
            headpose.t.toc('elapsed')
            headpose.t.summary()
            break

        frame_num += 1

    # When everything done, release the capture
    if args['disp'] == True: cv2.destroyAllWindows()
    LED.LEDCleanUp()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-disp', action='store_true', dest='disp', default=False, help='Display Output Image.')
    parser.add_argument('-wh', metavar='N', dest='wh', default=[720, 480], nargs=2, help='Frame size.')
    parser.add_argument('-lt', metavar='N', dest='landmark_type', type=int, default=1, help='Landmark type.')
    parser.add_argument('-mfn', metavar='N', dest='max_frame_num', type=int, default=100, 
                        help='Maximum number of frames to process')
    parser.add_argument('-lp', metavar='FILE', dest='landmark_predictor', 
                        default='../models/shape_predictor_68_face_landmarks.dat', help="Landmark predictor data file.")
    args = vars(parser.parse_args())
    main(args)
