deploy:
	serverless deploy --aws-s3-accelerate

invoke:
	serverless invoke -f grab_and_post

.PHONY: deploy invoke