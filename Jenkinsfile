pipeline {
    agent { label 'docker-agent' }

    environment {
        IMAGE_NAME = "url-monitoring-exporter"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Code pulled successfully!"
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('python-exporter') {
                    sh '''
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                    '''
                }
            }
        }

        stage('Verify Image') {
            steps {
                sh 'docker images | grep url-monitoring-exporter'
            }
        }
    }
}
