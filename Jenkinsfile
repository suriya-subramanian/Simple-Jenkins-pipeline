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
                    sh "docker build -t python-app:1.0.0 ."
                    sh "docker tag python-app:1.0.0 python-app:latest" 
            }
        }
    }
        stage('Deploy Stage') {
            steps {
                script {
                    echo "preparing to deploy to Kubernetes..."
                    withCredentials([file(credentialsId: 'k8s-kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                        sh '''
                            export KUBECONFIG=$KUBECONFIG_FILE
                            kubectl apply -f deployment.yaml
                            kubectl rollout status deployment/python-app-deployment -n app-deployment
                        '''
                    }
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
