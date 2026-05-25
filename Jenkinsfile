pipeline {
    agent any

    stages {
        stage('Checkout Stage') {
            steps {
                    checkout scm
            }
        }
        stage('Build Stage') {
            steps {
                script {
                    echo "Building the Docker image"
                    sh "docker build -t python-app:1.0.0"
                    sh "docker tag python-app:1.0.0 python-app:latest" 
            }
        }
    }
        stage('Deploy Stage') {
            steps {
                script {
                    echo "preparing to deploy..."
                    sh  "docker run -d -p 3000:3000 --name python-api python-app:latest"
            }
        }       
        
    }
}
    post {
        success {
            echo "Deployment successfull! The app is running on port 3000."
        }
        failure {
            echo "Pipeline failed. check the console output above."
        }
    }
}
