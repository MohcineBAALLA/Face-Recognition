import cv2
import mediapipe as mp
import smtplib
import os
import mimetypes  # Replace imghdr
from email.message import EmailMessage

# Email Configuration
EMAIL_SENDER = "Your_Email@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "Generated Password"   # Replace with your generated app password
EMAIL_RECEIVER = "Receiver_Mail@gmail.com"

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# Open the webcam
cap = cv2.VideoCapture(0)

sent_email = False  # Track if an email has been sent

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (Mediapipe requires RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame for face detection
    results = face_detection.process(frame_rgb)

    detected_faces = []
    
    if results.detections:
        for i, detection in enumerate(results.detections):  # Loop over all detected faces
            # Get bounding box coordinates
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

            # Ensure bounding box stays within frame bounds
            x, y = max(0, x), max(0, y)
            w, h = min(w, frame.shape[1] - x), min(h, frame.shape[0] - y)

            # Extract face ROI (Region of Interest)
            face_roi = frame[y:y+h, x:x+w]
            print(face_roi)
            detected_faces.append(face_roi)

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Show each detected face in separate windows
            if face_roi.size > 0:
                window_name = f"Face {i+1}"  # Unique window name for each face
                cv2.imshow(window_name, face_roi)

        # If more than one person is detected, show a red warning and send an email
        if len(detected_faces) > 1 and not sent_email:
            # Capture the second person's face
            new_face = detected_faces[-1]  # Get the last detected face (new person entering the frame)
            
            # Save the face image
            face_path = "intruder.jpg"
            cv2.imwrite(face_path, new_face)

            # Send email with the face image
            def send_email(image_path):
                msg = EmailMessage()
                msg["Subject"] = "ALERT!"
                msg["From"] = EMAIL_SENDER
                msg["To"] = EMAIL_RECEIVER
                msg.set_content("Someone is in your room.")

                # Attach the image
                mime_type, _ = mimetypes.guess_type(image_path)
                main_type, sub_type = mime_type.split("/") if mime_type else ("image", "jpeg")

                with open(image_path, "rb") as f:
                    img_data = f.read()
                    msg.add_attachment(img_data, maintype=main_type, subtype=sub_type, filename="intruder.jpg")

                # Send email
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                    server.send_message(msg)

            try:
                send_email(face_path)
                print("Email sent successfully!")
                sent_email = True  # Avoid sending multiple emails
                os.remove(face_path)  # Delete the image after sending
            except Exception as e:
                print(f"Failed to send email: {e}")

            # Create a large red warning window with warning message
            warning_window = frame.copy()
            cv2.rectangle(warning_window, (50, 50), (frame.shape[1] - 50, frame.shape[0] - 50), (0, 0, 255), -1)  # Red background
            cv2.putText(warning_window, "WARNING: UNAUTHORIZED PERSON DETECTED!", (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)
            
            # Display the new face in the warning window
            face_resized = cv2.resize(new_face, (380, 380))  # Resize face to fit in the warning window
            warning_window[100:100 + 380, 100:100 + 380] = face_resized  # Position the new face in the warning window

            # Show the large red warning window
            cv2.imshow("WARNING! New Person", warning_window)
            cv2.setWindowProperty("WARNING! New Person", cv2.WND_PROP_TOPMOST, 1)  # Keep warning window on top

    # Display the main frame
    cv2.imshow("Real-Time Face Detection with Warning", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
