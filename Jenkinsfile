pipeline {
    agent any

    stages {
        stage('Build Frontend') {
            steps {
                dir('./frontend') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        stage('Build Backend') {
            steps {
                dir('./backend') {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Run Frontend Tests') {
            steps {
                dir('./frontend') {
                    sh 'npm test'
                }
            }
        }
        stage('Run Backend Tests') {
            steps {
                dir('./backend') {
                    sh 'pytest'
                }
            }
        }
        stage('Deploy Frontend') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
                AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
            }
            steps {
                dir('./frontend') {
                    sh 'aws s3 sync build/ s3://ml6-food-ordering-frontend --delete'
                    sh 'aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths "/*"'
                }
            }
        }
        stage('Deploy Backend') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
                AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
            }
            steps {
                dir('./backend') {
                    sh 'aws elasticbeanstalk deploy --application-name ml6-food-ordering-backend --environment-name ml6-food-ordering-backend-env --version-label ${BUILD_NUMBER}'
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline succeeded.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}