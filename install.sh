#!/bin/bash

arg=$1

check_ca_file () {
  FILE="$PWD/install/ca.pem"
  if ! test -f $FILE; then
      echo "Error! File ca.pem not found!"
      echo "Please, put the file into install/ directory and try again!"
      exit 1
  fi
}

cmd_dev () {
  echo "Making \"dev\" environment..."
  docker-compose down -v
  cp ./install/.env.dev .env
  cp ./install/docker-compose.dev.yml docker-compose.yml
  cp ./install/ca.pem ./checker/ca.pem
  cp ./install/ca.pem ./consumer/ca.pem
  echo "...done!"
  build
}

cmd_prod () {
  check_ca_file
  echo "Making \"prod\" environment..."
  docker-compose down -v
  cp ./install/.env.prod .env
  cp ./install/docker-compose.prod.yml docker-compose.yml
  cp ./install/ca.pem ./checker/ca.pem
  cp ./install/ca.pem ./consumer/ca.pem
  echo "...done!"
  build
}

cmd_help () {
  echo "Usage:"
  echo "./setup.sh dev - if you want to use dockerized Kafka and PostgreSQL services"
  echo "./setup.sh prod - if you want to use cloud Kafka and PostgreSQL services"
}

build () {
  echo "Building services..."
  docker-compose build
  echo "...done!"
  echo "Installation finished."
}

case "$arg" in
    dev)
		cmd_dev
		;;
    prod)
		cmd_prod
		;;
    *)
    cmd_help
		;;
esac

