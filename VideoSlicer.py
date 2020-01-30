import cv2

# https://stackoverflow.com/questions/22704936/reading-every-nth-frame-from-videocapture-in-opencv
def loadvideo(fullPath, fps, interval):

    images = []
    print('Frames Loading')
    vidcap = cv2.VideoCapture(fullPath)
    readfps = vidcap.get(cv2.CAP_PROP_FPS)
    print(f'Video FPS:{readfps} Requested FPS {fps}')
    # print(readfps)
    success, image = vidcap.read()
    
    multiplier = round(readfps/ fps,0)
    print(f'Multiplier:{multiplier}')

    while success:
        frameId = int(round(vidcap.get(1)))
        success, image = vidcap.read()
        interval = interval + 1

        if (frameId == 0) or (frameId % multiplier == 0):
            images.append(image)
    
    vidcap.release()

    return images, readfps, interval, multiplier

# https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
def savevideo(list, folderPath, vidname, suf, fps):
    print('Starting Encoding')
    first_frame = 0
    last_frame = len(list)-1
    img = list[1]
    height, width, layers = img.shape
    size = (width,height)
    vid_length_t = round(len(list)/fps, 1)

    final_path = folderPath+vidname+str(3)+"."+suf

    out = cv2.VideoWriter(final_path,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    for i in range(len(list)):
        out.write(list[i])
    out.release

    print(f'Saving Video, Path:{final_path}, FPS: {fps}, Length:{vid_length_t}(s) ')

def nothing(val):
    pass

def main():
    
    folderPath = 'C:/Users/Bren/Videos/'
    videoFile = "waterfall.mp4"
    vidname, suf = videoFile.split('.')

    fullPath = folderPath + videoFile

    images = []
    trimed_frames_coords = []

    interval = 0
    readfps = 1
    fps = 15

    frame_select_tb_name = 'Frm Sel'
    window_capture_name = 'Video Capture'


    images, readfps, interval, multiplier = loadvideo(fullPath, fps, interval)
# savevideo(images)

    print(f"Image Count:{len(images)}")

    first_frame = 0
    last_frame = len(images)-2
    frame_count = 1
    first_frame_name = 'First'
    last_frame_name = 'Last'

    cv2.namedWindow(window_capture_name,cv2.WINDOW_NORMAL)
    cv2.createTrackbar(frame_select_tb_name, window_capture_name , 0, last_frame, nothing)
    cv2.imshow(window_capture_name,images[0])


    while True:
    
        key = cv2.waitKeyEx(30) #esc key
        if key == ord('q') or key == 27:
            break

        value = cv2.getTrackbarPos(frame_select_tb_name, window_capture_name)

        #arrow codes could be different based on different computers configurations
        if key == 2424832: #left arrow
            value = cv2.getTrackbarPos(frame_select_tb_name, window_capture_name) 
            if value == 0:
                value = 0
            else:
                value = value - 1
            # value = value - 1
            cv2.setTrackbarPos(frame_select_tb_name, window_capture_name,value)
            print('left')
        
        if key == 2555904: #right arrow
            value = cv2.getTrackbarPos(frame_select_tb_name, window_capture_name) 
            if value == (last_frame):
                value = (last_frame)
            else:
                value = value + 1
            cv2.setTrackbarPos(frame_select_tb_name, window_capture_name,value)
            # print('right')
            print(f'value:{value}')
        
        if key == 32: #spacebar
            temp_val = cv2.getTrackbarPos(frame_select_tb_name, window_capture_name)
            trimed_frames_coords.append(temp_val) 
            # cv2.createTrackbar(frame_select_tb_name, window_capture_name , temp_val , last_frame, nothing)
            if len(trimed_frames_coords) == 1:
                print(f'First Frame:{temp_val}')
            else:
                print(f'Second Frame:{temp_val}')

        if len(trimed_frames_coords)==2:
            trimed_frames_coords.sort()
            print(f'Min Frame:{trimed_frames_coords[0]}, Max Frame:{trimed_frames_coords[1]}')
            cv2.destroyWindow(window_capture_name)
            savevideo(images[trimed_frames_coords[0]:trimed_frames_coords[1]],folderPath, vidname, suf, readfps/multiplier) 
            break

        cv2.imshow(window_capture_name, images[value])

if __name__ == '__main__':

    main()

