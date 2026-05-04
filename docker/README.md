# Docker

## Learning Path

### Official Docker Tutorial
- Completed the official Docker tutorial: [welcome-to-docker](https://github.com/0xRaz-b/welcome-to-docker)
- Built an image using `docker build`
- Ran my first container using `docker run`
- Accessed the app via `localhost` on an exposed port



### Tutorial 2 — Multi-Container App
- Completed the multi-container tutorial: [multi-container-app](https://github.com/0xRaz-b/multi-container-app)
- Used `docker compose up` to orchestrate multiple containers simultaneously
- Connected a Node.js app to a MongoDB database using `compose.yaml`
- Used `docker compose watch` for hot reload during development
- Learned about volumes for data persistence between container restarts

### Concepts Learned
- **Dockerfile**: instruction file used to build an image
- **Image**: immutable environment 
- **Container**: a running instance of an image
- **Ports**: bridge between the host machine and the container 
- **docker compose**: orchestrate multiple containers with a single command
- **compose.yaml**: configuration file defining all services, ports, and volumes
