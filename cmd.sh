#!/bin/bash

VENV_DIR="venv"

start() {
    printer "🚀 Starting the app"
    docker-compose up
    handler
}

stop() {
    printer "🛑 Stopping the app"
    docker-compose down
    handler
}

setup() {
    printer "🔨 Setting up the app"
    python -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install --upgrade pip
    git submodule update --init --recursive
    docker-compose up --build
    handler
}

clear() {
    printer "🧹 Clearing all"
    rm -rf $VENV_DIR
    docker-compose down --volumes --rmi all
    handler
}

deploy() {
    printer "📦 Deploying the app"
    rm -rf Chatbot/*
    cp -r app Chatbot/app
    cp .gitignore Chatbot
    cp Dockerfile Chatbot
    cp app/README.md Chatbot
    rm -f Chatbot/app/README.md
    cd Chatbot
    git checkout main
    git add .
    git commit -m "Deployed the app"
    git push
    cd ..
    git checkout main
    git submodule update --remote
    git add .
    git commit -m "Deployed the app"
    git push
    handler
}

printer() {
    echo ""
    echo $1
    echo ""
}

handler() {
    if [ $? -eq 0 ]; then
        printer "✅ Process completed successfully"
    else
        printer "❌ An error occurred during the process"
        exit 1
    fi
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    setup)
        setup
        ;;
    clear)
        clear
        ;;
    deploy)
        deploy
        ;;
    *)
        echo "Usage: $0 {start|stop|setup|clear|deploy}"
        ;;
esac
