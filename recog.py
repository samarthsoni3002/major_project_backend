import face_recognition
import cv2
import os


def face_recog():

    known_faces_dir = "./face_recognition/known_faces"  
    known_faces = {}

    for filename in os.listdir(known_faces_dir):
        
        image = face_recognition.load_image_file(f"{known_faces_dir}/{filename}")
        try:
            encoding = face_recognition.face_encodings(image)[0]
            
            known_faces[os.path.splitext(filename)[0]] = encoding
        except IndexError:
            print(f"No face found in {filename}, skipping.")


    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video stream.")
        exit()

    print("Starting face recognition. Please look at the camera.")

    while True:

        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break


        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)


        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = list(known_faces.keys())[match_index]


            
            video_capture.release()
            cv2.destroyAllWindows()
            rec_name = name.split("_")[0]
            rec_desg = name.split("_")[1]




    return rec_name,rec_desg


