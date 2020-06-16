#!/bin/bash
SERVICE_NAME=dropFile-docker-manager
CONTAINER=dropfile-deploy_back_1
CONTAINER_FRONT=dropfile-deploy_front_1

case "$1" in
  start)
    export ROOT="$(cd "$(dirname "$ROOT")"; pwd)/$(basename "$ROOT")"
    echo "starting your dropfile-deploy system in '$ROOT'..."
    docker-compose up -d
    docker start $CONTAINER $CONTAINER_FRONT
    ;;
  stop)
    docker rm -f $CONTAINER $CONTAINER_FRONT
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
    docker-compose rm -f $CONTAINER $CONTAINER_FRONT
    docker-compose image rm -f dropfile-deploy_back dropfile-deploy_front
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
