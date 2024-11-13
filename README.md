# Security Camera with Motion Detection & Audio Transcription

This project is a Flask-based web application designed for the Raspberry Pi that provides real-time motion detection via a Pi Camera and audio transcription using the Google Speech Recognition API. The app offers a live video feed with motion detection overlays and allows basic audio transcription through a web interface.

## Features
- **Motion Detection**: Detects and highlights areas of movement in a live video feed.
- **Audio Transcription**: Captures audio input and converts it to text.
- **Web Interface**: Serves a web page for live streaming and audio transcription through the `/video_feed` and `/listen` endpoints.

## Requirements
- **Hardware**: Raspberry Pi with a Pi Camera
- **Python Libraries**:
  - `Flask`: For serving the web application.
  - `picamera`: To access and capture images from the Pi Camera.
  - `opencv-python`: For image processing and motion detection.
  - `speech_recognition`: For audio transcription.
  - `pyaudio`: To enable audio input from the microphone.
  - `imutils`: For helper functions in image processing.

## Installation

1. Clone this repository onto your Raspberry Pi.
2. Install the required libraries:
   ```bash
   pip install flask picamera opencv-python speechrecognition pyaudio imutils
   ```
3. Connect and configure the Pi Camera on your Raspberry Pi.
4. Make sure the microphone is attached and recognized by the Raspberry Pi.

## Usage

1. **Run the Application**:
   ```bash
   python main.py
   ```

2. **Access the Web Interface**:
   - Open a web browser and go to `http://<raspberry-pi-ip-address>:5000`.
   - The webpage will show the live video feed with motion detection and the audio transcription below.

## Limitations
- The Google Speech Recognition API requires an internet connection for audio transcription.
- The motion detection threshold may require tuning based on your environment.
