#!/bin/bash

VENV_DIR="venv"

start() {
    printer "🚀 Starting the app"
    docker run --rm --name app-chatbot -p 7860:7860 app-chatbot
    handler
}

stop() {
    printer "🛑 Stopping the app"
    docker stop app-chatbot
    handler
}

setup() {
    printer "🔨 Setting up the app"
    python -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install --upgrade pip
    git submodule update --init --recursive
    docker build -t app-chatbot .
    docker run --rm --name app-chatbot -p 7860:7860 app-chatbot
    handler
}

build() {
    printer "🔧 Building the app"
    mkdir -p build
    rm -rf build/*
    cp -r app build/app
    rm -f build/app/README.md
    cp .gitattributes build
    cp .gitignore build
    cp Dockerfile build
    cp app/README.md build
    handler
}

clear() {
    printer "🧹 Clearing all"
    rm -rf $VENV_DIR
    docker rm -f app-chatbot
    docker rmi app-chatbot
    handler
}

deploy() {
    printer "📦 Deploying the app"
    rm -rf chatbot/*
    cp -r app chatbot/app
    cp .gitattributes chatbot
    cp .gitignore chatbot
    cp Dockerfile chatbot
    cp app/README.md chatbot
    cd chatbot
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
    build)
        build
        ;;
    clear)
        clear
        ;;
    deploy)
        deploy
        ;;
    *)
        echo "Usage: $0 {start|stop|setup|build|clear|deploy}"
        ;;
esac
