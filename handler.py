import json

def grab_and_post(event, context):
    body = {
        "message": "Temporary Result. In Development",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    # Using Reddit API, Get the Title, Link, and Text of the latest post

    # Using the Github API, create a new issue with the Title from Reddit,
    # Link, and Text of the challenge
    return response
