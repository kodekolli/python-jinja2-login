pipeline {
    parameters {
        string(name: 'git_user', defaultValue: 'kodekolli', description: 'Enter github username')
        choice(name: 'action', choices: 'deploy\ndelete', description: 'Action to deploy or delete sample app to EKS cluster')
    }

    agent any
    environment {
        USER_CREDENTIALS = credentials('DockerHub')
        registryCredential = 'DockerHub'
        dockerImage = ''
    }
    stages {
        stage('clone prod repo') {
            steps {
                git url:"https://github.com/${params.git_user}/python-jinja2-login.git", branch:'production'
            }
        }
        stage('Deploying sample app to PROD EKS cluster') {
            when { expression { params.action == 'deploy' } }       
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
                        sh 'ansible-playbook python-app.yml --user jenkins -e action=present -e config=$HOME/.kube/prodconfig'
                        sleep 10
                        sh 'export APPELB=$(kubectl get svc -n default helloapp-svc -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")'                    
                }
            }
            post {
                success {
                    echo "Sample app deployed to PROD EKS cluster."
                }
                failure {
                    echo "Sample app deployment failed to PROD EKS cluster."
                }
            }
        }
        stage('Delete sample application from Prod EKS cluster'){
            when { expression { params.action == 'delete' } }
            steps {
                echo "Deleting the app from Prod EKS cluster"
                sh 'ansible-playbook python-app.yml --user jenkins -e action=absent -e config=$HOME/.kube/devconfig'
            }
        }
    }
}
