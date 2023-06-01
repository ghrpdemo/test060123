build:
	@docker build --tag python-docker .
services:
	@docker-compose -f docker/stack-postgres.yaml up
services-down:
	@docker-compose -f docker/stack-postgres.yaml down
