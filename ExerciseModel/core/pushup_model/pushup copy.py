import cv2
import mediapipe as mp
import pandas as pd
import os

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Output folders
output_image_folder = "output_images1"
push_up_folder = os.path.join(output_image_folder, "pushups")
push_down_folder = os.path.join(output_image_folder, "pushdowns")
os.makedirs(push_up_folder, exist_ok=True)
os.makedirs(push_down_folder, exist_ok=True)

# Initialize CSV data storage
data = []  # List to store rows of CSV
csv_filename = "pushup_dataset.csv"

# Load video
video_path = "pushup.mp4"
cap = cv2.VideoCapture(video_path)

frame_count = 0

print("Instructions:\nPress 'u' for Push Up position\nPress 'd' for Push Down position\nPress 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (MediaPipe requires RGB images)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect pose landmarks
    results = pose.process(frame_rgb)

    # Draw pose landmarks on the frame
    annotated_frame = frame.copy()
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the frame
    cv2.imshow("Pushup Data Collection", annotated_frame)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key in [ord('u'), ord('d')]:
        # Label based on key pressed
        label = "push_up" if key == ord('u') else "push_down"

        # Set the appropriate folder
        folder = push_up_folder if label == "push_up" else push_down_folder

        # Save the frame as an image
        image_filename = f"frame_{frame_count}_{label}.png"
        image_path = os.path.join(folder, image_filename)
        cv2.imwrite(image_path, frame)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = []
            for lm in results.pose_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])

            # Append data row: [image_filename, label, landmarks...]
            data.append([image_filename, label] + landmarks)

        print(f"Saved: {image_filename} with label {label}")

    frame_count += 1

# Release resources
cap.release()
cv2.destroyAllWindows()
pose.close()

# Save data to CSV
columns = ["image_filename", "label"] + [f"lm_{i}_{axis}" for i in range(33) for axis in ["x", "y", "z", "visibility"]]
df = pd.DataFrame(data, columns=columns)
df.to_csv(csv_filename, index=False)

print(f"Dataset saved to {csv_filename}")