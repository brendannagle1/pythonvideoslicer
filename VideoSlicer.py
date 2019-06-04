import cv2

folderPath = 'C:/Users/Bren/Videos/'
videoFile = "waterfall.mp4"
vidname,suf = videoFile.split('.')

fullPath = folderPath + videoFile

images = []

interval = 0
loadedint = 0
trim_frames = []
readfps = 1

frame_select_name = 'Frm Sel'
window_capture_name = 'Video Capture'

# https://stackoverflow.com/questions/22704936/reading-every-nth-frame-from-videocapture-in-opencv
def loadvideo(fullPath,fps):
	
	global interval, loadedint

	vidcap = cv2.VideoCapture(fullPath)
	readfps = round(vidcap.get(cv2.CAP_PROP_FPS))
	# print(readfps)
	success,image = vidcap.read()
	
	multiplier = readfps / fps

	while success:
		frameId = int(round(vidcap.get(1)))
		success, image = vidcap.read()
		interval = interval + 1

		if frameId % multiplier == 0:
			images.append(image)
			loadedint = loadedint + 1
	
	vidcap.release()
	# print(interval)
	# print(loadedint)
	return images, fps, readfps
# https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
def savevideo(list):
	global folderPath,vidname,suf,fps

	img = list[1]
	height, width, layers = img.shape
	size = (width,height)

	out = cv2.VideoWriter(folderPath+vidname+str(3)+"."+suf,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
	for i in range(len(list)):
		out.write(list[i])
	out.release

images, fps, readfps = loadvideo(fullPath,30)
# savevideo(images)

print(len(images))

first_frame = 0
last_frame = loadedint-1
frame_count = 1
first_frame_name = 'First'
last_frame_name = 'Last'

def on_frame_trackbar(val):
	global first_frame,last_frame,images,trim_frames
	frame_count = val
	cv2.setTrackbarPos(first_frame_name, window_capture_name, last_frame)
	cv2.imshow(window_capture_name,images[val])


cv2.namedWindow(window_capture_name,cv2.WINDOW_NORMAL)
cv2.createTrackbar(frame_select_name, window_capture_name , first_frame, (last_frame-1), on_frame_trackbar)
cv2.imshow(window_capture_name,images[0])


while True:
	key = cv2.waitKey(30)
	if key == ord('q') or key == 27:
		break
	if key == 32:
		trim_frames.append(cv2.getTrackbarPos(frame_select_name, window_capture_name) ) 
	if len(trim_frames)==2:
		cv2.destroyWindow(window_capture_name)
		print('Saving Video')
		savevideo(images[trim_frames[0]:trim_frames[1]]) 
		break
