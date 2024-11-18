import cv2
import base64
import time
from inference_sdk import InferenceHTTPClient


def glove_detection():
    # Initialize the inference client
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="iwu6gopcW3OxqABAtPsS"
    )

    # Model ID
    MODEL_ID = "gloves-gzbgu-yvuux/1"

    # Function to run inference on a frame
    def infer_frame(frame):
        # Encode the frame as a JPG image
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_image = base64.b64encode(buffer).decode("utf-8")

        # Perform inference
        try:
            result = CLIENT.infer(encoded_image, model_id=MODEL_ID)
            return result
        except Exception as e:
            print(f"Inference error: {e}")
            return None

    # Open the camera
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify the camera index

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    print("Press 'q' to quit the camera manually.")

    # Timer variables
    start_time = time.time()
    detection_made = False

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from camera.")
            break

        # Optionally resize frame for faster processing
        resized_frame = cv2.resize(frame, (640, 480))

        # Perform inference
        result = infer_frame(resized_frame)

        if result:
            # Parse the result for bounding boxes and predictions
            predictions = result.get("predictions", [])
            for prediction in predictions:
                label = prediction.get("class", "Unknown")
                confidence = prediction.get("confidence", 0)
                x_min, y_min = int(prediction["x"] - prediction["width"] / 2), int(prediction["y"] - prediction["height"] / 2)
                x_max, y_max = int(prediction["x"] + prediction["width"] / 2), int(prediction["y"] + prediction["height"] / 2)

                # Draw the bounding box and label
                cv2.rectangle(resized_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(
                    resized_frame,
                    f"{label} ({confidence:.2f})",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                # If gloves are detected, print and stop detection
                if label.lower() == "gloves" and confidence > 0.6:
                    predicted_gl = True
                    print("Gloves detected")
                    detection_made = True
                    cap.release()
                    cv2.destroyAllWindows()
                    return predicted_gl
                    exit()

        # Check if 10 seconds have elapsed without detection
        elapsed_time = time.time() - start_time
        if elapsed_time > 10 and not detection_made:
            predicted_gl = False
            
            print("Gloves not predicted")
            break

        # Show the live video with bounding boxes
        cv2.imshow("Camera Feed", resized_frame)

        # Exit manually on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    
    return predicted_gl




