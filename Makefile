@PHONY: build run

build:
	@echo "Building..."
	@docker build -t chat:latest .


run:
	echo "Running..."
	if [ "$(shell docker ps -aq -f name=chat)" ]; then docker rm -f chat; fi
	docker run -d -p 5550:80 --rm --name chat chat:latest
