
test: build_test_docker
	docker run --rm backend_technical_unittest:latest

build_test_docker:
	docker build -t backend_technical_unittest:latest -f Dockerfile.test .

runserver: build
	docker run --rm -p 5000:5000 backend_technical:latest

build:
	docker build -t backend_technical:latest .

