import os
import time
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import sys
#Hello, Welcome for using my Bot.I am Sandro.If you facing any problem then knock me(sandrobiswas36@gmail.com)

# Set the video ID of the video you want to comment on
video_url = input("Enter the YouTube video URL: ")
if 'shorts' in video_url:
    video_id = video_url.split("/")[-1]
else:
    video_id = video_url.split("v=")[1]

# Set the message you want to reply with
message = input("Enter the comment reply message: ")

# Set the path to your API credentials file
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Authenticate with the YouTube API using your credentials file
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
)

# Use run_local_server() instead of run_console()
credentials = flow.run_local_server(port=0)
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Set the file path where the replied user IDs will be stored
replied_ids_file = "C:/Users/sabdr/Desktop/Youtube/replied_ids.json"

# Load the replied user IDs from the file
replied_ids = set()
if os.path.exists(replied_ids_file):
    with open(replied_ids_file, "r") as f:
        data = f.read()
        if data:
            replied_ids = set(json.loads(data))

# Get the comments for the specified video
next_page_token = ''
comment_ids = set()
try:
    while next_page_token is not None:
        comments_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token
        )
        comments_response = comments_request.execute()

        for comment in comments_response['items']:
            comment_id = comment['snippet']['topLevelComment']['id']
            author_name = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            author_channel_id = comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']

            if comment_id not in comment_ids and author_channel_id not in replied_ids:
                # Reply to the comment with the specified message
                reply_request = youtube.comments().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "parentId": comment_id,
                            "textOriginal": message
                        }
                    }
                )
                reply_response = reply_request.execute()
                print(f"Replied to {author_name} ({author_channel_id}): {comment_text}")

                comment_ids.add(comment_id)
                replied_ids.add(author_channel_id)

                # Wait for 1 minute before replying to the next comment
                time.sleep(60)

        next_page_token = comments_response.get('nextPageToken', None)

except KeyboardInterrupt:
    # Save the replied user IDs to the file before exiting the program
    try:
        with open(replied_ids_file, "w") as f:
            json.dump(list(replied_ids), f)
        print(f"Replied user IDs saved to {replied_ids_file}")
    except:
        print(f"Failed to save replied user IDs to {replied_ids_file}")

    sys.exit()
finally:

# Save the replied user IDs to the file before exiting the program
    try:
        with open(replied_ids_file, "w") as f:
            json.dump(list(replied_ids), f)
        print(f"Replied user IDs saved to {replied_ids_file}")
    except:
        print(f"Failed to save replied user IDs to {replied_ids_file}")

    sys.exit()
    
