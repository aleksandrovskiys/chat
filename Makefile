@PHONY: build

build:
	@echo "Building..."
	@docker build -t chat:latest .


run:
	@echo "Running..."
	@docker run -d -p 5550:80 --rm --name chat chat:latest
