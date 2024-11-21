import flask
from flask import Flask, render_template, Response
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import speech_recognition as sr
import imutils
import datetime
import time
import pyaudio
import wave

camera = PiCamera()
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

recognizer = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
	recognizer.adjust_for_ambient_noise(source)

reference_frame = None

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

#motion detection
def detect_motion(image):
	global reference_frame
	min_area = 15
	maybe_motion_text = "Not Detected"
	
	current_frame = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	current_frame = cv2.GaussianBlur(current_frame,(21,21),0)
	
	if reference_frame is None:
		reference_frame = current_frame
	
	frame_delta = cv2.absdiff(reference_frame ,current_frame)
	thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
	
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	
	for c in cnts:
		if cv2.contourArea(c) < min_area:
			continue
		(x,y,w,h) = cv2.boundingRect(c)
		cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
		maybe_motion_text = "Detected"
		
	cv2.putText(image, "Motion: {}".format(maybe_motion_text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0),2)
	cv2.putText(image, datetime.datetime.now().strftime("%A %d %B %Y %I: %M: %S5p"), (10,image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35,(0,0,0),1)
	
	return image

def get_camera_frames(camera):
	for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
		image = frame.array
		raw_capture.truncate()
		raw_capture.seek(0)
		image = detect_motion(image)
		_, image = cv2.imencode(".jpg", image)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(get_camera_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

#audio transcriber

@app.route('/listen')		
def transcribe_audio():
	with mic as s:
		audio = recognizer.listen(s)
	try:
		return recognizer.recognize_google(audio)
	except sr.UnknownValueError:
		return "Google Speech Recognition could not understand audio"
	except sr.RequestError as e:
		return "Could not request results from Google Speech Recognition service; {0}".format(e)
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False)
