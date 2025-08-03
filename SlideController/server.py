from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import subprocess
import psutil  # To check if the process is already running

app = Flask(__name__)

# Initialize webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start_script():
    # Check if main.py is already running
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = proc.info['cmdline']
        if cmdline and 'main.py' in cmdline:
            return jsonify({"message": "Script is already running!"}), 200

    try:
        # Run the main.py script
        subprocess.Popen(['python3', 'SliderController/main.py'])
        return jsonify({"message": "Script started successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)