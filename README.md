# Aiven Homework

The project is an implementation of a system that monitors website availability over the network, 
produces metrics about this, and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

## Requirements

* Docker (tested on Docker version 20.10.3, build 48d30b5)
* Docker Compose (docker-compose version 1.24.0, build 0aa59064)

## Installation

The project uses SASL authentication method for Kafka which requires CA certificate.
So **before** the installation you should put your `ca.pem` file into the `install/` directory.

For initial setup, you can use `./install.sh` script. 
There are two options for the installation:
    
1. "Development" mode 

    `./install.sh dev`

    In this configuration, Kafka and PostgreSQL services will be run in docker containers on your local machine. 
    This mode also suggests `Kafdrop` tool for monitoring and managing Kafka 
    (the tool works on `localhost:9000` by default)

2. "Production" mode 

    `./install.sh prod`
    
    This mode uses Aiven cloud Kafka and PostgreSQL services.
  
 
After you choose the mode and run the installation process, 
the script will create `.env`, `docker-compose.yml`, 
and other required files which are completely ready to work in the `dev` mode.

However, if you use `prod` mode, after the installation, you should do two more things:

* specify the Aiven credentials in the `.env` file:

```shell script
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=...

KAFKA_BROKERCONNECT=...
KAFKA_SASL_PLAIN_USERNAME=...
KAFKA_SASL_PLAIN_PASSWORD=...
```    

* initialize database schema by `docker-compose run aiven-prod-init-db` command. 
Enter your DB password to finish.


You're also able to switch between the modes afterward. 
However, in this case, all manual settings will be reset to defaults.

## Run

Options:

    # run with debug output
    docker-compose up
    
    # run as a daemon (silent mode)
    docker-compose up -d
    
## Stop

Options:
    
    # stop services
    docker-compose stop
    
    # stop services and remove containers and networks
    docker-compose down
    
    # stop services and remove containers, networks and volumes
    docker-compose down -v
    
## Testing

### Testing checker script

    docker-compose up aiven-checker-testing

### Testing consumer script

    docker-compose up aiven-consumer-testing
    




 