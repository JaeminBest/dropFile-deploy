#!/bin/bash
NOT_INSTALLED="0"

function docker_install_check() {
  CHECK=$(docker -v)
  if [[ $CHECK == bash* ]]; then
      echo "install Docker first!! (https://www.docker.com/get-started)"
      RET_CHECK="1"
  fi
}

function repo_unpack() {
  CONTAINER_CHECK=$(docker ps | grep dropfile-deploy_web_1)
  if [[ $CONTAINER_CHECK != "" ]]; then
    echo "docker container already up"
  else
    docker rm -f dropfile-deploy_web_1
    IMAGE_CHECK=$(docker images | grep dropfile-deploy_web)
    if [[ $IMAGE_CHECK != "" ]]; then
      echo "docker image already exist"
    else 
      echo "building docker image..."
      docker-compose build
    fi
    echo ""
    echo "================== SETTING DONE ========================="
    echo "| now start your first dropFile web application!        |"
    echo "| COMMAND : ROOT=[ROOT] [WATCH=[WATCH]] dropFile start  |" 
    echo "========================================================="
    echo ""
  fi
}

docker_install_check
if [[ $NOT_INSTALLED == 0 ]];
then
    echo "existing docker found"
    repo_unpack
fi
chmod +x $PWD/dropFile.sh
alias dropFile=$PWD/dropFile.sh
