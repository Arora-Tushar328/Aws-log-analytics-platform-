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
             script {
                 COMMIT_ID = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          }
             dir('python-exporter') {
              sh """
               docker build -t url-monitoring-exporter:${BUILD_NUMBER} .
               docker tag url-monitoring-exporter:${BUILD_NUMBER} url-monitoring-exporter:latest
               docker tag url-monitoring-exporter:${BUILD_NUMBER} url-monitoring-exporter:${COMMIT_ID}
                """
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
