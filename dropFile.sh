#!/bin/bash
SERVICE_NAME=dropFile-docker-manager
CONTAINER=dropfile-deploy_web_1 # Make this value to yours.

case "$1" in
  start)
    export ROOT="$(cd "$(dirname "$ROOT")"; pwd)/$(basename "$ROOT")"
    # export WATCH="$(cd "$(dirname "$WATCH")"; pwd)/$(basename "$WATCH")"
    echo "[ ROOT  ] starting your dropfile-deploy system in '$ROOT'..."
    # echo "[ WATCH ] watching your download default directory '$WATCH'..."
    docker-compose up -d
    docker start $CONTAINER
    python -c "import os; os.system('npm install') if not os.path.isdir('./node_modules') else None"
    echo "wait for application booting.. about 40 sec required"
    sleep 40
    ;;
  stop)
    docker rm -f $CONTAINER
    ;;
  logs)
    docker logs -f $CONTAINER
    ;;
  open)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open http://localhost:8080/
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open http://localhost:8080/
    elif [[ "$OSTYPE" == "cygwin" ]]; then
        start http://localhost:8080/
    elif [[ "$OSTYPE" == "msys" ]]; then
        start http://localhost:8080/
    elif [[ "$OSTYPE" == "win32" ]]; then
        start http://localhost:8080/
    else
        echo "Unknown OS environment. Are you one of Linux, Windows, MacOSX?"
    fi
    ;;
  delete)
    docker-compose rm -f $CONTAINER
    docker-compose image rm -f dropfile-deploy_web
    ;;
  bash)
    docker exec -it $CONTAINER bash
    ;;
  help)
    echo "$SERVICE_NAME: usages:"
    echo ""
    echo "dropFile <command> [<args>]"
    echo ""
    echo "commands:"
    echo ""
    echo "  start                     starts dropFile-deploy program"
    echo "  stop                      stops dropFile-deploy program"
    echo "  open                      open dropFile web app"
    echo "  delete                    uninstall whole program"
    echo "  bash                      access to web app bash shell"
    echo "  logs                      see whole logs of dropFile-deploy system"
    echo "  help                      prints the document"
    echo ""
    ;;
  *)
    echo "$SERVICE_NAME: invalid command"
    echo ""
    echo "execute 'dropFile help' to see the document"
    echo ""
    ;;
esac
