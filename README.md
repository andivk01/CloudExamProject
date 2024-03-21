The project was run on a machine with the following specifications:
- OS: EndevourOS (Arch Linux, zsh shell)
- CPU: Ryzen 3 4300u (4 cores, 4 threads)
- RAM: 8GB

To run the project, you need to have Docker and Docker Compose installed on your machine.

## Quick Start Guide
To start the project, execute:
```bash
./run.sh
```
This script:
- Creates test files (KB, MB, GB).
- Deploys containers using Docker Compose (docker-compose up -d).
- Prepares for locust tests by configuring nextcloud_app as a trusted domain in Nextcloud.

After running the script, wait 30 seconds and you can access the Nextcloud instance at http://localhost:8080.
The locust web interface is available at http://localhost:8888.

To reset the project environment, run:
```bash
./delete.sh
```
This stop and removes containers, volumes, and test files, reverting your setup to its original state.