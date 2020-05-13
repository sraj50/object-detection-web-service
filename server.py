import numpy as np
from flask import Flask, request
import cv2
import json

app = Flask(__name__)
# app.config['DEBUG'] = True

objectList = []
labels_path = "./yolo-coco/coco.names"

# derive paths to YOLO weights and model configuration
weightsPath = "./yolo-coco/yolov3-tiny.weights"
configPath = "./yolo-coco/yolov3-tiny.cfg"


def yolo(file):
    obj_list = []

    # load COCO class labels our YOLO model was trained on
    LABELS = open(labels_path).read().strip().split("\n")

    # initalise list of colors to represent each possiable class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    # load binary image from HTTP POST request
    nparr = np.frombuffer(file, dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # load input image and grab spatial dimensions
    (H, W) = image.shape[:2]

    # load YOLO object detector trained on COCO dataset
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    # determine only the output later names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from input image and then perform a forward
    # pass the YOLO object detector, giving our bounding boxes and probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    # start = time.time()
    layerOutputs = net.forward(ln)
    # end = time.time()

    # show timing information on YOLO
    # print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialise lists of detected bounding boxes, confidences, class IDs
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each detection
        for detection in output:
            # extract class ID and confidence of current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter weak predictions by setting detected probability > min probability
            if confidence > 0.5:
                # scale bounding box coordinates back to relative of size of image
                # YOLO actually returns the centre (x,y) coordinates of bounding box
                # followed by height and width of box
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use centre to derive top and left corner of bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update list of bounding box coordinates, confidences and class ID
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    for class_id, con in zip(classIDs, confidences):
        acc = con * 100
        json_dict = {'label': LABELS[class_id], 'accuracy': '{:.2f}'.format(acc)}
        obj_list.append(json_dict)
    return json.dumps({"objects:": obj_list})


@app.route('/api/object_detection', methods=['POST', 'GET'])
def process():
    # save files locally and then perform processing
    if request.method == 'POST':
        file = request.files['image']
        return yolo(file.read())

    if request.method == 'GET':
        return 'Hello world'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
