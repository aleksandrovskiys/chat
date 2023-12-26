@PHONY: build run

build:
	@echo "Building..."
	@docker build -t socket-chat:latest .


run:
	echo "Running..."
	if [ "$(shell docker ps -aq -f name=socket-chat)" ]; then docker rm -f socket-chat; fi
	docker run -d -p 5550:80 --rm --name socket-chat socket-chat:latest
