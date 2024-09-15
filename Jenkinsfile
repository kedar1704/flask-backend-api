pipeline {
    agent any

    environment {     
    DOCKERHUB_CREDENTIALS= credentials('dockerhub_login')     
    } 

    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Code download') {
            steps {
                git branch: 'master', url: 'https://github.com/kedar1704/flask-backend-api.git'
            }
        }
        stage('Dockerize app') {
            steps {
                sh 'pwd'
                sh 'docker build -t python_app:$BUILD_NUMBER .'
            }
          }
        stage('Docker images') {
            steps {
                sh 'docker images'
            }
          }
        stage('Wait for Approval') {
            steps {
                script {
                    def userInput = input(
                        message: 'Do you want to continue?',
                        parameters: [
                            [$class: 'BooleanParameterDefinition', 
                             defaultValue: false, 
                             description: 'Click "Yes" to continue pushing to dockerhub or "No" to abort', 
                             name: 'Push to dockerhub']
                        ]
                    )
                    
                    if (userInput) {
                        echo 'Deploying the image to dockerhub'
                    } else {
                        echo 'Dont push image. Aborting pipeline.'
                        currentBuild.result = 'ABORTED'
                        error('Pipeline aborted by user.')
                    }
                }
            }
        }
        stage('Push image to dockerhub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'                		
	              echo 'Login Completed'
		            sh 'docker tag python_app:$BUILD_NUMBER kedar1704/python_app:$BUILD_NUMBER'
		            sh 'docker push kedar1704/python_app:$BUILD_NUMBER'
            }
          }
	stage('get pods') {
            steps {
                sh 'kubectl get po'
            }
          }
	stage('Apply manifests') {
            steps {
                sh 'cd k8s'
		sh "sed -i 's#image: kedar1704/flask-backend-api:v3#image: kedar1704/python_app:$BUILD_NUMBER#g' deployment.yaml"
		sh "kubectl apply -f k8s/deployment.yaml"
		sh "kubectl apply -f k8s/sts.yaml"
		sh "kubectl apply -f k8s/svc.yaml"
		sh "kubectl apply -f k8s/db-secret.yaml"
            }
          }
	stage('Get all ') {
            steps {
                sh 'kubectl get all -n default'
            }
          }
    }
}
