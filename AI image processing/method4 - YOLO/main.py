import cv2
import numpy as np

def get_yolo_net():
    # Load YOLOv3 pre-trained weights and configuration file
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # Load COCO names file (contains names of all objects that YOLO can detect)
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Get output layer names
    output_layer_names = net.getUnconnectedOutLayersNames()

    return net, classes, output_layer_names

def detect_cars(image_path):
    # Read the image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Prepare the image for YOLO
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Get predictions from YOLO
    outs = net.forward(output_layer_names)

    # Initialize car count
    car_count = 0

    # Set confidence threshold
    confidence_threshold = 0.9

    # Non-maximum suppression parameters
    nms_threshold = 0.4

    # Process the predictions
    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold and class_id == 2:  # Class ID 2 corresponds to "car" in COCO names
                # Calculate coordinates of the bounding box
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Calculate the top-left corner of the bounding box
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maximum suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

    # Draw the bounding boxes and labels
    for i in indices:
        x, y, w, h = boxes[i]
        label = f"Car"
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        car_count += 1

    # Print the number of cars found after non-maximum suppression
    print(f"Number of cars found: {car_count}")

    # Create a resizable window
    cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)

    # Show the result
    cv2.imshow("Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    net, classes, output_layer_names = get_yolo_net()

    # Specify the path to the image you want to process
    image_path = "pics/b.webp"

    # Detect cars in the image
    detect_cars(image_path)
