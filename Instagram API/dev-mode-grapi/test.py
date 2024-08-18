import asyncio
from hikerapi import AsyncClient

# Initialize the client with the access key
access_key = "SfrK6SEWniXNQrypTi7vnfdc2uT0K7WN"
cl = AsyncClient(access_key)

async def fetch_followers(user_id, total_followers_wanted):
    followers = []
    next_end_cursor = None
    
    try:
        while len(followers) < total_followers_wanted:
            # Fetch the next chunk of followers
            response = await cl.user_followers_chunk_gql(user_id=user_id, end_cursor=next_end_cursor)
            
            # If the response is a list of followers (older API format)
            if isinstance(response, list):
                chunk_followers = response
                next_end_cursor = None  # No cursor in this case
            else:
                # Extract followers and the end cursor for pagination
                chunk_followers = response.get("response", {}).get("items", [])
                next_end_cursor = response.get("end_cursor")
            
            # Accumulate followers
            for follower_list in chunk_followers:
                if isinstance(follower_list, list):
                    for follower in follower_list:
                        if isinstance(follower, dict):
                            followers.append(follower['username'])
                            # Stop if we have reached the desired number of followers
                            if len(followers) >= total_followers_wanted:
                                return followers
            
            # If there is no more data to fetch, break the loop
            if not next_end_cursor:
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return followers

def save_followers_to_file(followers, filename="followers.txt"):
    try:
        with open(filename, "w") as f:
            for username in followers:
                f.write(f"{username}\n")
        print(f"Followers saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to file: {e}")

# Example usage
user_id = "34259953"
total_followers_wanted = 1000  # Specify the number of followers you want to fetch

# Run the async function to fetch followers
followers = asyncio.run(fetch_followers(user_id, total_followers_wanted))

# Print out the result and save to file
if followers:
    print(f"{len(followers)} followers retrieved successfully:")
    for username in followers:
        print(username)
    
    # Save followers to a text file
    save_followers_to_file(followers)
else:
    print("Failed to retrieve followers.")
