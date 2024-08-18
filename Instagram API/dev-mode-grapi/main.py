import os
from instagrapi import Client
from instagrapi.types import StoryMention, UserShort
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Instagram credentials from environment variables
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

# Initialize the client
cl = Client()

# Log in to Instagram
cl.login(username, password)

# Path to the image or video for the story
media_path = '1.png'  # Update with the correct file path

# Mention user in the story
mention_username = 'arianamikush'
user = cl.user_info_by_username(mention_username)

# Convert User object to UserShort, or extract necessary data
user_short = UserShort(pk=user.pk, username=user.username, full_name=user.full_name)

# Create the StoryMention object
mention = StoryMention(user=user_short, x=0.5, y=0.5, width=0.6, height=0.1)

# Upload story with mention
cl.photo_upload_to_story(media_path, mentions=[mention])

print("Story uploaded successfully with mention!")
