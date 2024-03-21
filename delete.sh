#!/bin/zsh

docker-compose down
rm -r nextcloud
rm locust/testfile_*
rm -r db