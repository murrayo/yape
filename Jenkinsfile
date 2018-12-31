pipeline {
    agent {
        label 'docker'
    }
 stages {
    stage('Clone repository') {
        steps {
            checkout scm
        }
    }

    stage('Build image') {
        steps {
            script {
                def yapeimage = docker.build("yape/yape")
            }
        }
    }

    stage('Test image') {
        //at some point run the actual tests...
        steps {
            yapeimage.inside {
                sh 'echo "Tests passed"'
            }
        }
    }

    stage('Push image') {
         docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials-yape') {
            yapeimage.push("${env.BUILD_NUMBER}")
            yapeimage.push("latest")
        }
    }
 }
}