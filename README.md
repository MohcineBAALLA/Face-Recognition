# Real-Time Face Detection with Email Alert

## Overview
This project uses **OpenCV** and **MediaPipe** to detect faces in real-time via a webcam. If more than one face is detected, an alert is triggered, capturing the intruder's face and sending an email notification with the image attached.

## Features
- **Real-time face detection** using MediaPipe.
- **Multi-person detection** with a bounding box around each face.
- **Intruder detection**: If more than one face is detected, an alert is triggered.
- **Email notification**: Captures and sends the intruder's face via email.
- **Warning display**: Shows a red warning screen with the intruder's face.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install opencv-python mediapipe
```

For email functionality:
```bash
pip install secure-smtplib
```

## Email Configuration
Before running the script, update the email settings:

```python
EMAIL_SENDER = "Your_Email@gmail.com"  # Your Gmail account
EMAIL_PASSWORD = "Generated Password"   # App password (not your regular password)
EMAIL_RECEIVER = "Receiver_Mail@gmail.com"
```
> **Note:** You need to generate an **App Password** from your Google Account security settings if you're using Gmail.

## How to Run
1. **Ensure your webcam is connected.**
2. **Run the script** in a Python environment:

```bash
python face_detection_alert.py
```
3. **Press 'q' to exit** the application.

## How It Works
1. The script captures webcam frames and detects faces in real-time.
2. If **only one face** is present, it continues monitoring.
3. If **multiple faces** are detected:
   - The new face is **captured and saved**.
   - An **email alert** is sent with the image attached.
   - A **warning window** with a red screen and the intruder's face is displayed.
4. The script prevents multiple alerts from being sent continuously.

## Notes
- This script is designed for **Gmail SMTP**. If using another email provider, modify the SMTP settings accordingly.
- The email feature may not work if **Less Secure Apps** are disabled in your email provider.
- The script **automatically deletes** the intruder's image after sending the email.

## Future Enhancements
- Implement face recognition to differentiate between authorized and unauthorized persons.
- Add support for **sending SMS alerts**.
- Integrate cloud storage for storing detected images securely.

## License
This project is open-source and free to use.

