import math
import mediapipe as mp

def are_index_fingers_touching(hand1_landmarks, hand2_landmarks):
    # Define the landmarks for the index fingers of both hands
    index_finger_1 = hand1_landmarks[8]  # Index finger tip landmark for hand 1
    index_finger_2 = hand2_landmarks[8]  # Index finger tip landmark for hand 2

    # Calculate the Euclidean distance between the two index fingers
    distance = math.sqrt((index_finger_1.x - index_finger_2.x)**2 + (index_finger_1.y - index_finger_2.y)**2)

    # Define a threshold for considering them as touching (you can adjust this)
    touch_threshold = 0.03  # Adjust as needed

    # Check if the distance is below the threshold
    if distance < touch_threshold:
        return True
    else:
        return False

def index_dist(hand1_landmarks, hand2_landmarks):
    index_finger_1 = hand1_landmarks[8]  # Index finger tip landmark for hand 1
    index_finger_2 = hand2_landmarks[8]  # Index finger tip landmark for hand 2

    # Calculate the Euclidean distance between the two index fingers
    distance = math.sqrt((index_finger_1.x - index_finger_2.x)**2 + (index_finger_1.y - index_finger_2.y)**2)
    return distance

def stop_touch(hand1_landmarks, hand2_landmarks):
    index_finger_1 = hand1_landmarks[8]  # Index finger tip landmark for hand 1
    index_finger_2 = hand2_landmarks[8]  # Index finger tip landmark for hand 2
    thumb_finger_1 = hand1_landmarks[4]  # Thumb for hand1
    thumb_finger_2 = hand2_landmarks[4]  # Thumb for hand2
    
    distance1 = math.sqrt((index_finger_1.x - thumb_finger_1.x)**2 + (index_finger_1.y - thumb_finger_1.y)**2)
    distance2 = math.sqrt((index_finger_2.x - thumb_finger_2.x)**2 + (index_finger_2.y - thumb_finger_2.y)**2)

    # Define a threshold for considering them as touching (you can adjust this)
    touch_threshold = 0.03  # Adjust as needed
    
    if distance1 and distance2 < touch_threshold:
        return True
    else:
        return False
    

