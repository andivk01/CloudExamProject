#!/bin/zsh

# create test files in locust directory
python3 create_testfiles.py

# start docker containers
docker-compose up -d

# container id for the nextcloud web app
CONTAINER_ID="nextcloud_app"

echo "Sleeping for 30 seconds to make sure the container is up and running..."
sleep 30

echo "For future improvements we should add encryption"
# docker exec --user www-data $CONTAINER_ID php occ encryption:enable 
# docker exec --user www-data $CONTAINER_ID php occ encryption:encrypt-all 

echo "Adding nextcloud_app to trusted domains..."
docker exec --user www-data $CONTAINER_ID php occ config:system:set trusted_domains 1 --value=nextcloud_app