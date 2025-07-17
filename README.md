# Face Recognition Attendance System (with Google Sheets Integration)

This is a real-time face recognition-based attendance system built using MediaPipe, OpenCV, Flask, and the Google Sheets API.

It detects and recognizes faces through the webcam, marks IN/OUT attendance, and logs it to both a local CSV file and a remote Google Sheet.

---

## Features

- Real-time face detection using webcam
- Face recognition using MediaPipe face landmarks
- IN/OUT attendance logging with timestamps
- Logs attendance to:
  - `attendance.csv` (local)
  - Google Sheet (remote)
- Web-based interface:
  - Live webcam feed
  - Admin panel for viewing logs

---

## Folder Structure

face_attendance_gsheets/
├── app.py # Main Flask app
├── register_faces.py # Register and encode new faces
├── helpers.py # Utility functions for attendance and Sheets
├── creds.json # Google API credentials (keep private)
├── attendance.csv # Attendance logs
├── requirements.txt # Python dependencies
├── static/
│ └── faces/ # Face image folders
├── templates/
│ ├── index.html # Webcam interface
│ └── admin.html # Admin log viewer

yaml
Copy
Edit

---

## How It Works

1. Add images of each person to `static/faces/<person_name>/`
2. Run `register_faces.py` to encode face data
3. Launch the app with `python app.py`
4. Open `http://localhost:5000/` in your browser
5. Stand in front of the webcam. If recognized, attendance is marked automatically
6. Visit `/admin` to view logged attendance

---

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/your-username/face_attendance_gsheets.git
cd face_attendance_gsheets
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Add your Google Sheets API credentials:

Enable the Google Sheets API in Google Cloud Console

Create a service account and download the creds.json file

Place creds.json in the root of this project

Share your Google Sheet with the service account email (Editor access)

Register faces:

Place face images in folders under static/faces/

Example: static/faces/Alice/, static/faces/Bob/

Run the script:

bash
Copy
Edit
python register_faces.py
Start the Flask app:

bash
Copy
Edit
python app.py
Open your browser and go to:

http://localhost:5000/ for the live webcam

http://localhost:5000/admin for attendance logs

