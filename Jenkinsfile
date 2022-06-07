pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker-compose -f production.yml build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose -f production.yml up -d'
            }
        }
    }
}
