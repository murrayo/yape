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
                //use this as initial build step
                def yapeimage = docker.build("yape/yape")
            }
        }
    }
    
    //stage('Test image') {
    //    //at some point run the actual tests...
    //    steps {
    //        script {
    //            yapeimage.inside {
    //                sh 'echo "Tests passed"'
    //            }
    //       }
    //    }
    //}


    stage('Push image') {
        steps {
            script {
                //needs to be redefined due to shortcomings in declarative syntax (scope of variables)
                //it isn't a problem here, since it'll use the cached version since we're running on the 
                //same agent. still annoying. see https://groups.google.com/forum/#!topic/jenkinsci-users/y_IOIxXb4T8
                def yapeimage = docker.build("yape/yape")
                docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials-yape') {
                    yapeimage.push("${env.BUILD_NUMBER}")
                    yapeimage.push("latest")
                }
            }
        }
    }
 }
}