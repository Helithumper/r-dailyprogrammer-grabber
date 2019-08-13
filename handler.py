import json
import os
import praw
from datetime import datetime
from github import Github

issue_disclaimer = "**THIS WAS WRITTEN BY A BOT** _beep boop_"
latest_n_posts = 5

def attempt_github_post(reddit_post):
    print(f"Attempting Issue Creation for {reddit_post.title}")
    access_token = os.getenv('GITHUB_ACCESS_TOKEN') or ""
    g = Github(access_token)
    repo_name = os.getenv('GITHUB_REPO_NAME') or ""
    repo = g.get_repo(repo_name)
    issues = repo.get_issues(state='all')
    for issue in issues:
        if issue.title == reddit_post.title:
            print(f"Title Conflict with issue {issue.id}")
            return
    
    try:
        difficulty = reddit_post.title.split(' [')[1].split(']')[0]
    except:
        difficulty = "UNKNOWN"

    try:
        stripped_title = reddit_post.title.split('] ')[2]
    except:
        stripped_title = reddit_post.title

    link = reddit_post.url
    label = repo.get_label(difficulty)
    repo.create_issue(
        title=reddit_post.title,
        body=f"# {stripped_title}\n{issue_disclaimer}\n\n**Original Link:** [{link}]({link})\n ## Post Body\n{reddit_post.selftext}",
        labels=[label]
    )

def grab_and_post(event, context):
    reddit_id = os.getenv('REDDIT_CLIENT_ID') or ""
    reddit_secret = os.getenv('REDDIT_CLIENT_SECRET') or ""
    reddit_user_agent = os.getenv('REDDIT_USER_AGENT') or ""
    reddit = praw.Reddit(client_id=reddit_id,
                         client_secret=reddit_secret,
                         user_agent=reddit_user_agent)

    try:
        random_subreddit = reddit.random_subreddit().display_name
        print(f"Successfully Logged in, Random Subreddit: {random_subreddit}")
    except Exception as e:
        print(f"Error logging in: {str(e)}")
        raise e

    reddit_dp = reddit.subreddit('dailyprogrammer')
    posts = list(reddit_dp.new(limit=latest_n_posts))
    posts.reverse()
    for post in posts:
        print(f"Grabbed Post {post.title}")
        attempt_github_post(post)