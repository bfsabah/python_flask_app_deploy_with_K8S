# BUILD A PYTHON FLASK APP AND DEPLOY WITH KUBERNETES
In this article, you will learn how to develop a simple python application in Python Flask and deploy it on Kubernetes.
**Kubernetes** is a commonly used container orchestration and management system. Kubernetes is an open-source platform and it enables users to deploy, maintain and scale applications and their features. Kubernetes allows the user to choose a preferred programming language or framework and enable the user to be able to track and monitor logs. Kubernetes has a very large community that is ready to help and provide answers to questions and also provide solutions to difficulties.

We would use Kubernetes to deploy our Python Flask application as it allows us to deploy and manage our application seamlessly, it also allows us to scale and release new features while reducing the resources to only those that are required to make our application run smoothly.

**Flask** is a lightweight Python web framework. It allows users to build applications faster and easier and also gives room to scale complex applications.

Flask is a microframework, hence, it allows the developer to use different tools and packages as it doesn’t enforce a particular layout.

Flask has a large community that provides different packages and extensions to enable developers to perform different functionalities with ease, and also provide answers to different questions and issues the developer might run into.

Every flask application has an in-built server. It accepts requests from the webserver and converts it to information for the Python application.

Meanwhile, the web server makes the application accessible to the public. It accepts requests from the user and sends a reverse proxy to the application server.

**The requirements for building and deploying our flask application are:**

- Python (We will work with Python 3) and Pip package manager
- Docker and DockerHub
- Kubectl

**Creating a basic Flask Application**<br>
To create a Flask application we need to install the Flask package for python. But before we do that it is advisable to always create a virtual environment so that everything we will do doesn’t affect the Python installed on our machine.

**Step 1: Installations**<br>
The first steps we’ll take in building our flask application is to create our application folder, install the python virtual environment and install our flask package.

Create the application directory:
```
mkdir my_flask_app
cd my_flask_app
```
Install python virtual environment with pip:
```
pip install virtualenv
```
Create a virtual environment for our app:
```
virtualenv venv
```
Activate the virtual environment we created:
```
source venc/bin/activate
```
Install the Flask package:
```
pip install Flask
```
Save all the packages in a file:
```
pip freeze > requirements.txt
```
**Step 2 : Build the Flask Application**<br>
Create app.py file and start coding.

Code Snippet comes here****

To run the app on your local :
```
python app.py
```
**Step 3: Serve HTML/Template Files**

Flask allows us to display contents to our users with HTML. In this step, we are going to create an HTML file for our home page.

Flask reads HTML files from a directory called templates and reads assets like your CSS, Javascript and images from the static directory.

Create templates and static directories inside our my_flask_app directory:
```
mkdir templates static
```
Create a new file in the templates directory and name it home.html. We will add a few lines of HTML codes to this file before we create a route for it in our app.

Our home.html file will look like this:

https://github.com/bfsabah/python_flask_app_deploy_with_K8S/blob/b38c4cbd2240e98b60ec8510f700fda761f9b1c1/templates/home.html#L1-L12

Next, we will create a route and function to serve our HTML file. To serve HTML files in flask, we will import and use a Flask function called render_template.

Our app.py now file will look like this:

https://github.com/bfsabah/python_flask_app_deploy_with_K8S/blob/65294e4d3aa6cea77b9fe4e645688dd57b5e8b3f/app.py#L1-L19

Run the application on your local machine by running:
```
python app.py
```

Navigate to localhost:5000/home on your preferred browser to view your Flask application.

![image](https://user-images.githubusercontent.com/113843658/222987812-9b2a5cb2-21e4-4847-9009-f4d0b90b8de7.png)


Now that we have our basic Flask app running, we will go on to build a docker image for our application so we can deploy it with Kubernetes.

**Step 4: Build a Docker image**

We need to create a container to be able to run our application on Kubernetes. To create this container we have to create a Docker image that will be published to a registry on Dockerhub.

To build our docker image we need to create a Dockerfile in our application directory.

Create a file and name it Dockerfile and add the following lines in it:

https://github.com/bfsabah/python_flask_app_deploy_with_K8S/blob/65294e4d3aa6cea77b9fe4e645688dd57b5e8b3f/Dockerfile#L1-L9

In the Dockerfile, we are building our application off a python base image on the first line. The next line creates a work directory and the third line in the Dockerfile sets the created directory as the work directory. The fourth and sixth line copies requirements.txt and installs the packages in it, meanwhile the fifth line upgrades the pip python package manager. Next thing we do is copy all the files in our application directory and expose our application to port 5000 and run our application with the last line.

The next step we’ll take is to build our docker image by running:
```
docker build -t [DockerHub_username]/my_flask_app .
```
Add a tag to the image:
```
docker tag my_flask_app:latest [DockerHub_username]/my_flask_app:0.1
```
Run the docker image:
```
docker run -p 5000:5000 [DockerHub_username]/my_flask_app:0.1
```
Push the image to Dockerhub:
```
docker push [DockerHub_username]/my_flask_app:0.1
```
**Step 5: Deploy App on Kubernetes**

We will deploy our basic Flask app as a standalone pod and expose it as a LoadBalance service. To do this we first create a namespace. Namespaces allow the user to segment clusters.

Create namespace flaskapp:
```
kubectl create namespace flaskapp
```
To list all the namespaces in your cluster run:
```
kubectl get namespace
```
Next, we’ll create a deploy manifest file that will create and also get our deploy running

Create a manifest file named my_flask_app_deploy.yaml:

https://github.com/bfsabah/python_flask_app_deploy_with_K8S/blob/65294e4d3aa6cea77b9fe4e645688dd57b5e8b3f/my_flask_app_deployment.yaml#L2-L22

To roll out the deployment in our flaskapp namespace run:

```
kubectl apply -f my_flask_app_deploy.yaml -n flaskapp
```
To check if this deployment is running:
```
kubectl get deploy -n flaskapp
```
Next, we would forward our local port to the pod’s container port:
```
kubectl port-forward deployment/myflaskapp-deploy -n flaskapp 5000:5000
```
Navigate to localhost:5000/home to see your Flask application.

Next, we will create a Kubernetes service to create a stable network for the running pod. To do this we will create a manifest file.

Create a manifest file called my_flask_app_service.yaml:

https://github.com/bfsabah/python_flask_app_deploy_with_K8S/blob/65294e4d3aa6cea77b9fe4e645688dd57b5e8b3f/my_flask_app_service.yaml#L2-L15

To create the service run:
```
kubectl apply -f my_flask_app_service.yaml -n flask
```
It may take a bit of time to provision the cloud LoadBalancer.

To verify if it’s provisioned run:
```
kubectl get svc -w
```
Once you see an EXTERNAL-IP for the service, navigate to it on your browser to check your preferred web browser.
