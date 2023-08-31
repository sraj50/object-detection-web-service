# object-detection-web-service
A web service written in python to detect objects in images and sends a JSON response back to the client listing the objects.

The webservice is contanierized as a Docker image and loaded into a Kubernetes cluster.

The Kubernetes cluster is created using Kind with one master and one worker node.

The web service is exposed as a Kubernetes service which can be called from any external network.

## How the objectives were achieved

1.  A python web service "server.py" was developed that accepts images as POST requests from a client and uses YOLO and OpenCV to process the image and return a JSON object
    with a list of detected objects as the response.

2.  Once the web service was developed, a Docker image was built for the object detection web service

3.  A Kubernetes cluster was created using Kind with one Master and one worker node. The Docker image for the object detection web service was loaded into the cluster.

4.  Next, a deployment configuration was created so that pods will be created and deployed that will have the Docker image running in the pods.

5.  The web service was exposed as a Kubernetes service by creating a service configuration. It also specified the port mapping (NodePort) between the NECTAR VM and the
    Kubernetes services. This allows the object detection web service to be exposed to external networkds.


Please go to the below link to see a demonstration of the assignment.
https://youtu.be/gdeqp6Urs1Q
