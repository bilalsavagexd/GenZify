from supabase import create_client
from utils import get_env_variable
import os
import logging

class StorageManager:
    def __init__(self):
        self.url = get_env_variable("SUPABASE_URL")
        self.key = get_env_variable("SUPABASE_KEY")
        self.supabase = create_client(self.url, self.key)
        self.bucket_name = 'videos'
    
    def upload_video(self, video_path):
        try:
            # Upload to Supabase storage
            with open(video_path, 'rb') as f:
                file_name = os.path.basename(video_path)
                self.supabase.storage.from_(self.bucket_name).upload(
                    path=file_name,
                    file=f,
                    file_options={"content-type": "video/mp4"}
                )
            
            # Get public URL
            url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_name)
            
            # Clean up local file
            os.remove(video_path)
            logging.info(f"Successfully uploaded video: {file_name}")
            
            return url
            
        except Exception as e:
            logging.error(f"Error uploading video: {str(e)}")
            raise Exception(f"Error uploading video: {str(e)}")
