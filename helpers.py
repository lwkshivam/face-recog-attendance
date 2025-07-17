import pickle
import numpy as np
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

ENCODING_FILE = 'data/encodings.pkl'
ATTENDANCE_FILE = 'attendance.csv'
MATCH_THRESHOLD = 0.6
MIN_GAP_MINUTES = 1

SHEET_URL = 'https://docs.google.com/spreadsheets/d/1J4z50wb_BrPY9V_l3cfRjBkZvpX8C89bQ-iZCaU1NXg/edit?gid=0#gid=0'
CREDENTIALS_FILE = 'creds.json'

last_seen = {}

def load_saved_encodings():
    with open(ENCODING_FILE, 'rb') as file:
        return pickle.load(file)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def compare_faces(new_face, known_faces):
    for name, saved_face in known_faces.items():
        similarity = cosine_similarity(new_face, saved_face)
        if similarity > (1 - MATCH_THRESHOLD):
            return name
    return "Unknown"

def connect_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open_by_url(SHEET_URL).sheet1

def mark_attendance(name):
    now = datetime.now()
    status = "IN"

    if name in last_seen:
        last_time, last_status = last_seen[name]
        if now - last_time > timedelta(minutes=MIN_GAP_MINUTES):
            status = "OUT" if last_status == "IN" else "IN"
        else:
            return
    else:
        status = "IN"

    # Local CSV
    with open(ATTENDANCE_FILE, 'a') as file:
        file.write(f"{name},{now.strftime('%Y-%m-%d %H:%M:%S')},{status}\n")

    # Google Sheets
    try:
        sheet = connect_google_sheet()
        sheet.append_row([name, now.strftime('%Y-%m-%d %H:%M:%S'), status])
    except Exception as e:
        print(f"[Google Sheets Error] {e}")

    last_seen[name] = (now, status)

def read_attendance():
    try:
        with open(ATTENDANCE_FILE, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    except FileNotFoundError:
        return []
