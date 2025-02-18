import instaloader
from datetime import datetime
import os
import re
class InstagramDownloader:
    def __init__(self, username, password):
        # Create Instaloader instance
        self.L = instaloader.Instaloader(
            download_comments=False,
            save_metadata=False,
            download_video_thumbnails=False
        )
        # Login to Instagram
        try:
            self.L.login(username, password)
            print("Successfully logged in!")
        except Exception as e:
            print(f"Login failed: {e}")
            exit()

    def download_profile_posts(self, profile_username, download_reels=True, download_posts=True):
        """
        Download posts and/or reels from a specific profile
        """
        try:
            # Load profile
            profile = instaloader.Profile.from_username(self.L.context, profile_username)
            
            # Create directory for downloads
            download_dir = f"downloads/{profile_username}"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            print(f"Starting download for profile: {profile_username}")
            
            # Get all posts
            for post in profile.get_posts():
                # Check if it's a reel (video) or regular post
                is_reel = post.is_video
                
                # Download based on user preferences
                if is_reel and download_reels:
                    print(f"Downloading reel: {post.shortcode}")
                    self.L.download_post(post, target=download_dir)
                elif not is_reel and download_posts:
                    print(f"Downloading post: {post.shortcode}")
                    self.L.download_post(post, target=download_dir)
                
        except Exception as e:
            print(f"Error downloading profile content: {e}")

    def extract_shortcode(self, url):
        """
        Extract shortcode from various Instagram URL formats
        """
        # Regular expressions for different Instagram URL patterns
        patterns = [
            r'/(?:p|reel)/([A-Za-z0-9_-]+)',  # Matches both /p/ and /reel/
            r'shortcode=([A-Za-z0-9_-]+)',     # Matches shortcode parameter
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no match found, raise error
        raise ValueError("Could not extract shortcode from URL")

    def download_single_post(self, url, id):
        """
        Download a single post/reel using its URL
        """
        try:
            # Extract shortcode from URL
            shortcode = self.extract_shortcode(url)

            # Get post using shortcode
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)

            # Create a temporary directory to store the downloaded file
            download_dir = "downloads"
            os.makedirs(download_dir, exist_ok=True)  # Ensure directory exists

            print(f"Downloading post/reel: {shortcode}")
            
            # Download the post to the specified directory
            self.L.download_post(post, target=download_dir)
            print("Download completed!")
        except Exception as e:
            print(f"Error downloading single post: {e}")
            return None

    def download_by_hashtag(self, hashtag, max_count=10, download_reels=True, download_posts=True):
        """
        Download posts and reels by hashtag
        """
        try:
            download_dir = f"downloads/hashtag_{hashtag}"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            print(f"Starting download for hashtag: #{hashtag}")
            
            posts = self.L.get_hashtag_posts(hashtag)
            count = 0
            
            for post in posts:
                if count >= max_count:
                    break
                    
                is_reel = post.is_video
                
                if is_reel and download_reels:
                    print(f"Downloading reel: {post.shortcode}")
                    self.L.download_post(post, target=download_dir)
                    count += 1
                elif not is_reel and download_posts:
                    print(f"Downloading post: {post.shortcode}")
                    self.L.download_post(post, target=download_dir)
                    count += 1
            
            print(f"Finished downloading {count} posts/reels for #{hashtag}")
            
        except Exception as e:
            print(f"Error downloading hashtag content: {e}")
