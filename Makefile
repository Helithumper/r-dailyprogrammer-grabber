#!make
include .env
export $(shell sed 's/=.*//' .env)

deploy:
	serverless deploy --aws-s3-accelerate

invoke:
	serverless invoke -f grab_and_post

test-local:

	@python3 run.py

.PHONY: deploy invoke test-local
