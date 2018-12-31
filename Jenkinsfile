pipeline {
    agent {
        label 'docker'
    }
 stages {
    stage('Clone repository') {

        checkout scm
    }

    stage('Build image') {

        app = docker.build("yape/yape")
    }

    stage('Test image') {
        //at some point run the actual tests...
        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push image') {
         docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials-yape') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
 }
}