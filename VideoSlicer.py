import cv2
import os
import imageio
# from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from time import sleep

fps = 0
output_format = ''

# https://stackoverflow.com/questions/22704936/reading-every-nth-frame-from-videocapture-in-opencv
def loadvideo(fullPath, fps, interval):

    images = []
    print('Frames Loading')
    vidcap = cv2.VideoCapture(fullPath)
    readfps = vidcap.get(cv2.CAP_PROP_FPS)
    print(f'Video FPS:{readfps} Requested FPS {fps}')
    success, image = vidcap.read()

    if readfps/ fps >= 1:
        multiplier = round(readfps/fps,0)
    else:
        multiplier = 1

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
def savevideo(img_list, frame_list, folderPath, vidname, suf, fps_out, output_format):

    print(f'Starting Encoding in: {output_format} format')

    img = img_list[0]
    height, width, layers = img.shape
    size = (width,height)
    vid_length_t = round(len(img_list)/fps, 1)

    final_path = folderPath+vidname+'_trimmed'+"."
    if output_format == 'MP4':
        temp_final_path = final_path+suf
        out = cv2.VideoWriter(temp_final_path,cv2.VideoWriter_fourcc(*'mp4v'), round(fps_out,2), size)

        print (frame_list)
        if frame_list[0] < frame_list[1]:
            for i in range(len(img_list)):
                out.write(img_list[i])
        else:
            for i in range(len(img_list)-1,-1,-1):
                print(i)
                out.write(img_list[i])
        out.release
        print(f'Saving Video, Path:{temp_final_path}, FPS: {round(fps,2)}, Length:{vid_length_t}(s) ')

    elif output_format == 'GIF':
        temp_gif_list = []
        if frame_list[0] < frame_list[1]:
            for i in range(len(img_list)):
                temp_gif_list.append(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))
        else:
            for i in range(len(img_list)-1,-1,-1):
                temp_gif_list.append(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))

        counter = 0
        while True:

            path_to_check = final_path[:-1]+'_'+str(counter)+'.gif'

            if os.path.exists(path_to_check):
                counter += 1
            else:
                temp_final_path = path_to_check
                break

        imageio.mimwrite(temp_final_path, temp_gif_list, fps=fps_out)
        print(f'Saving Video, Path:{temp_final_path}, FPS: {round(fps,2)}, Length:{vid_length_t}(s) ')

    elif output_format == 'BOTH':
        print("BOTH Selected")
        counter = 0
        while True:

            path_to_check = final_path[:-1]+'_'+str(counter)+'.mp4'

            if os.path.exists(path_to_check):
                counter += 1
            else:
                temp_final_path = path_to_check
                break

        out = cv2.VideoWriter(temp_final_path,cv2.VideoWriter_fourcc(*'mp4v'), round(fps_out,2), size)

        print (frame_list)
        if frame_list[0] < frame_list[1]:
            for i in range(len(img_list)):
                out.write(img_list[i])
        else:
            for i in range(len(img_list)-1,-1,-1):
                print(i)
                out.write(img_list[i])
        out.release
        print(f'Saving Video, Path:{temp_final_path}, FPS: {round(fps,2)}, Length:{vid_length_t}(s) ')

        temp_gif_list = []
        if frame_list[0] < frame_list[1]:
            for i in range(len(img_list)):
                temp_gif_list.append(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))
        else:
            for i in range(len(img_list)-1,-1,-1):
                temp_gif_list.append(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))

        counter = 0
        while True:

            path_to_check = final_path[:-1]+'_'+str(counter)+'.gif'

            if os.path.exists(path_to_check):
                counter += 1
            else:
                temp_final_path = path_to_check
                break

        imageio.mimwrite(temp_final_path, temp_gif_list, fps=fps_out)
        print(f'Saving Video, Path:{temp_final_path}, FPS: {round(fps,2)}, Length:{vid_length_t}(s) ')

    else:
        print('Unable to save Video')

def nothing(val):
    pass

def main():
    global fps, output_format

    def submit():
        global fps, output_format

        fps=int(parse_val_choosen.get())
        output_format = ouput_fmt_chsn.get()
        if fps != '' and output_format != '':
            print("FPS selected is : " + str(fps))
            print("File output selected is : " + str(output_format))
            root.quit()
            root.withdraw()

    root = tk.Tk()
    root.title('Select Frame Reducer')
    root.geometry('250x200')
    ttk.Label(root, text = "Select nth Frame Interval :",
        font = ("Times New Roman", 10)).grid(column = 1,
        row = 1, padx = 10, pady = 10)

    n = tk.StringVar()
    parse_val_choosen = ttk.Combobox(root, width = 27,
                                textvariable = n, state="readonly")
    parse_val_choosen['values'] = (' 1',
                          ' 2',
                          ' 3',
                          ' 4',
                          ' 5',
                          ' 6',
                          ' 8',
                          ' 10',
                          ' 12',
                          ' 15',
                          ' 30',
                          ' 60')

    parse_val_choosen.grid(column = 1,
        row = 2, padx = 30, pady = 10)
    parse_val_choosen.current()

    ttk.Label(root, text = "Select Video Output Type :",
        font = ("Times New Roman", 10)).grid(column = 1,
        row = 3, padx = 10, pady = 10)

    m = tk.StringVar()
    ouput_fmt_chsn = ttk.Combobox(root, width = 27,
                                textvariable = m, state="readonly")
    ouput_fmt_chsn['values'] = ('MP4',
                          'GIF',
                          'BOTH')
    ouput_fmt_chsn.grid(column = 1,
        row = 4, padx = 30, pady = 10)
    ouput_fmt_chsn.current()

    ok_btn=tk.Button(root,text = 'OK',
                  command = submit)
    ok_btn.grid(row=17,column=1)
    root.mainloop()

    # root.withdraw()
    while True:
        try:
            root.filename = filedialog.askopenfilename(initialdir = "/",
                                                  title = "Open MP4 file",
                                                  filetypes = (("MP4", "*.mp4*"),
                                                               ("all files","*.*")))

            folderPath = '/'.join(root.filename.split('/')[0:-1])+'/'
            videoFile =  root.filename.split('/')[-1]
            vidname, suf = videoFile.split('.')
            break

        except:
            print("Please Select a Valid MP4 file")
            sleep(1)

    fullPath = folderPath + videoFile

    images = []
    trimed_frames_coords = []

    interval = 0
    readfps = 1
    # fps = 15

    frame_select_tb_name = 'Frm Sel'
    window_capture_name = 'Video -  Select Trimming Points with Spacebar'


    images, readfps, interval, multiplier = loadvideo(fullPath, fps, interval)

    print(f"Image Count:{len(images)}")

    first_frame = 0
    last_frame = len(images)-2
    frame_count = 1
    first_frame_name = 'First'
    last_frame_name = 'Last'

    cv2.namedWindow(window_capture_name,cv2.WINDOW_NORMAL)
    cv2.createTrackbar(frame_select_tb_name, window_capture_name , 0, last_frame, nothing)

    scale_percentage = 40
    w_out = int(images[0].shape[1]*scale_percentage/100)
    h_out = int(images[0].shape[0]*scale_percentage/100)
    dimensions = (w_out,h_out)
    # print(dimensions)

    img_to_show = cv2.resize(images[0], dimensions, interpolation = cv2.INTER_AREA)

    cv2.imshow(window_capture_name,img_to_show)
    cv2.resizeWindow(window_capture_name,img_to_show.shape[1],img_to_show.shape[0])

    while True:

        key = cv2.waitKeyEx(30)
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
            # trimed_frames_coords.sort()
            print(f'Min Frame:{trimed_frames_coords[0]}, Max Frame:{trimed_frames_coords[1]}')
            cv2.destroyWindow(window_capture_name)

            if trimed_frames_coords[0] < trimed_frames_coords[1]:
                savevideo(images[trimed_frames_coords[0]:trimed_frames_coords[1]],\
                    trimed_frames_coords,folderPath, vidname, suf, readfps/multiplier, output_format)
            else:
                savevideo(images[trimed_frames_coords[1]:trimed_frames_coords[0]],\
                    trimed_frames_coords,folderPath, vidname, suf, readfps/multiplier, output_format)
            break

        img_to_show = cv2.resize(images[value], dimensions, interpolation = cv2.INTER_AREA)
        cv2.imshow(window_capture_name, img_to_show)

if __name__ == '__main__':

    main()
