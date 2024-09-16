Documenatation for the Application 

1. HTTP API Service for Serving Messages

Endpoints:

/get/messages/<account_id>: Fetches messages for a specific account_id with sender and receiver details.
/create: Saves a message with sender and receiver details.
/search: Filters messages based on message_id, sender_number, or receiver_number.

To Post the API use the following request format - 

curl -X POST http://<APISERVICE>:5000/create -H "Content-Type: application/json" \
-d '{"account_id": "123", "sender_number": "111111", "receiver_number": "222222"}'

To get the data from DB use the following request format - 

curl http://<APISERVICE>:5000/get/messages/123

To get the data from DB using parameter use the /search API using this format - 

curl http://<APISERVICE>:5000/search?account_id=”123”

Error Handling and Logging:
Basic error handling and logs are collected using Fluentd and sent to Elasticsearch for log management.

Security:
Dockerfile with best practices, including minimizing image size.


2. DevOps and Terraform

Deployment for Application:
The backend is containerized and deployed as a Kubernetes Deployment.
Zero downtime deployments are ensured with RollingUpdate strategy.

StatefulSet for MySQL:
MySQL is deployed as a StatefulSet with persistent volume claims (PVCs) for data storage and to maintain stable network IDs.
Terraform for EKS:

Service:
The service is exposed through a Kubernetes Service and here NodePort for external access.

Fluentd for Logging:
A Fluentd DaemonSet collects logs from the application and sends them to Elasticsearch for analysis.
Custom parsing rules ensure logs are structured before sending to Elasticsearch.

Terraform for EKS:
Terraform code provisions an AWS EKS cluster,security groups, VPC, subnets, and route tables are configured for Kubernetes network access.
Have used terraform modules for efficiency and least operational overhead.


3. CI/CD Pipeline

Stages:

Clean workspace: Ensures that Jenkins workspace is cleared between builds.
Code download: Pulls the latest code from GitHub.
Dockerize app: Builds the application image.
Docker images: Lists the Docker images for confirmation.
Approval step: Allows manual approval for deployment to DockerHub.
Push to DockerHub: Pushes the image to DockerHub.
Deploy to Kubernetes: Applies Kubernetes manifests (deployment, statefulset, services, secrets).


4. Architectural Diagram

API: HTTP API for serving messages, containerized and deployed on Kubernetes.
Database: MySQL StatefulSet with persistent storage for the message database.
Logging: Fluentd captures logs and sends them to Elasticsearch.
CI/CD: Jenkins pipeline manages the deployment process, from Dockerization to deploying on Kubernetes.
Infrastructure: EKS Cluster provisioned using Terraform on AWS, with autoscaling, IAM roles.


                          +---------------------------+
                          |     Jenkins Pipeline       |
                          +---------------------------+
                                      |
        +------------------------------------------------------------+
        |                 Kubernetes Cluster (Terraform)             |
        +------------------------------------------------------------+
        |                                                            |
    +---v---+               +------------------+                       +----v----+
    |  API  |--(Deployment)->|     Fluentd      |--(logs)--------->|  Elasticsearch  |
    |       |               +------------------+                       +---------+
    +-------+                                                   
        |                              +------------------+ 
        +-------------(MySQL)--------->|   StatefulSet    |
                                       +------------------+





