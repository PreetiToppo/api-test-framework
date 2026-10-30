pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        BASE_URL = 'https://jsonplaceholder.typicode.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        
        stage('Run Ruff Linter') {
            steps {
                script {
                    sh 'python -m ruff check .'
                }
            }
        }
        
        stage('Install Allure CLI') {
            steps {
                script {
                    sh 'wget -q https://github.com/allure-framework/allure2/releases/download/2.28.0/allure-2.28.0.zip -O /tmp/allure.zip'
                    sh 'unzip -q /tmp/allure.zip -d /opt/'
                    sh 'ln -sf /opt/allure-2.28.0/bin/allure /usr/bin/allure'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest -n 4 -v --tb=short --alluredir=allure-results'
                }
            }
            post {
                always {
                    junit 'pytest.xml'
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                script {
                    sh 'allure generate allure-results --output reports/allure-report --clean'
                }
            }
        }
        
        stage('Generate HTML Report') {
            steps {
                script {
                    sh 'pytest --html=reports/report.html --self-contained-html -v'
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            echo 'Pipeline completed'
        }
        success {
            echo 'Tests passed successfully!'
        }
        failure {
            echo 'Tests failed. Check the build logs and reports.'
            error 'Test suite failed'
        }
    }
}
