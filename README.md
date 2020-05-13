# object-detection-web-service
A web service written in python to detect objects in images and sends a JSON response back to the client listing the objects.

The webservice is contanierized as a Docker image and loaded into a Kubernetes cluster.

The Kubernetes cluster is created using Kind with one master and one worker node.

The web service is exposed as a Kubernetes service which can be called from any external network.
