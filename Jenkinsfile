pipeline {
    parameters {
        string(name: 'git_user', defaultValue: 'kodekolli', description: 'Enter github username:')
    }

    agent any
    environment {
        USER_CREDENTIALS = credentials('DockerHub')
        registryCredential = 'DockerHub'
        dockerImage = ''
    }
    stages {
        stage('clone repo') {
            steps {
                git url:"https://github.com/${params.git_user}/python-jinja2-login.git", branch:'test'
            }
        }
        stage('Deploying sample app to Test EKS cluster') {
            when { branch 'test' }       
            steps {
                script{
                    echo "Building docker image"
                    dockerImage = docker.build("${USER_CREDENTIALS_USR}/eks-demo-lab:${env.BUILD_ID}")
                    echo "Pushing the image to registry"
                    docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
                        dockerImage.push("latest")
                        dockerImage.push("${env.BUILD_ID}")
                    }
                    echo "Deploy app to EKS cluster"
                    sh 'ansible-playbook python-app.yml --user jenkins -e action=present -e config=$HOME/.kube/qaconfig'
                    sleep 10
                }
            }
            post {
                success {
                    echo "Sample app deployed to Dev EKS cluster."
                }
                failure {
                    echo "Sample app deployment failed to Dev EKS cluster."
                }
            }
        }
        stage('DAST testing using OWASP ZAP') {
            steps {
                sh "sudo mkdir -p ${WORKSPACE}/reports"
                sh "sudo chmod -R 777 ${WORKSPACE}/reports"
                sh '''#!/bin/bash
                ELB=$(kubectl get svc -n default helloapp-svc -o jsonpath="{.status.loadBalancer.ingress[0].hostname}" --kubeconfig=$HOME/.kube/qaconfig)
                docker run -v ${WORKSPACE}/reports:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -r app.html -t http://$ELB || true
                '''
            }
        }
    }
}
