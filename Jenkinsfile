pipeline {
    agent any

    environment {
        // Remember to change this to your actual Docker Hub username!
        DOCKER_IMAGE = "sursubra/python-app" 
        
        // This automatically generates versions like 1.0.15 based on the Jenkins build number
        APP_VERSION = "1.0.${env.BUILD_NUMBER}" 
    }

    stages {
        stage('Checkout Stage') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Stage') {
            steps {
                script {
                    echo "Building Docker image version ${APP_VERSION}..."
                    // Tag the image with the specific dynamic version AND latest
                    sh "docker build -t ${DOCKER_IMAGE}:${APP_VERSION} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
        
        stage('Push Stage') {
            steps {
                script {
                    echo "Pushing version ${APP_VERSION} to Docker Hub..."
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${APP_VERSION}
                        docker push ${DOCKER_IMAGE}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy Stage') {
            steps {
                script {
                    echo "Preparing to deploy version ${APP_VERSION} to Kubernetes..."
                    withCredentials([file(credentialsId: 'k8s-kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                        sh '''
                            export KUBECONFIG=$KUBECONFIG_FILE
                            
                            # 1. Update the image tag in deployment.yaml to pull the new version
                            sed -i "s|image: .*|image: ${DOCKER_IMAGE}:${APP_VERSION}|g" deployment.yaml
                            
                            # 2. Inject the new version number into the APP_VERSION environment variable
                            sed -i "s|REPLACE_VERSION|${APP_VERSION}|g" deployment.yaml
                            
                            # Apply the changes to the cluster
                            kubectl apply -f deployment.yaml
                            
                            # Watch the rollout happen live!
                            # (Replace 'my-app-deployment' if your deployment is named differently)
                            kubectl rollout status deployment/python-app-deployment -n app-deployment
                            
                            # Reset the file back to "REPLACE_VERSION" so Git tracking doesn't get messy
                            git checkout deployment.yaml
                        '''
                    }
                }
            }       
        }
    }
    
    post {
        success {
            echo "Successfully deployed version ${APP_VERSION}!"
        }
        failure {
            echo "Pipeline failed on version ${APP_VERSION}. Check the console output above."
        }
    }
}