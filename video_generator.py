import cv2
import numpy as np
import os
import logging
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import time
from datetime import datetime
from pydub import AudioSegment

class VideoGenerator:
    def __init__(self):
        # Create absolute paths for directories
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, "generated_videos")
        self.background_video = os.path.join(self.base_dir, "assets", "background_videos", "subway_surfers.mp4")
        
        # Create directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Video settings
        self.width = 1080
        self.height = 1920
        self.max_file_size = 45 * 1024 * 1024  # 45MB target size
        self.total_steps = 4
        self.words_per_frame = 2
        self.max_duration = 240  # 4 minutes
        self.fps = 30  # Define FPS explicitly
        
        if not os.path.exists(self.background_video):
            logging.warning(f"Background video not found at: {self.background_video}")

    def _process_background_frame(self, frame):
        """Process background frame to fit 9:16 without stretching"""
        if frame is None:
            return None

        # Get original dimensions
        h, w = frame.shape[:2]
        
        # Calculate scaling factor to maintain aspect ratio
        scale = max(self.width/w, self.height/h)
        
        # Calculate new dimensions
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize frame maintaining aspect ratio
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Create black canvas of target size
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Calculate position to center the frame
        x_offset = (self.width - new_w) // 2
        y_offset = (self.height - new_h) // 2
        
        # Copy the resized frame onto the canvas
        if x_offset < 0:
            # Crop width if too wide
            start_x = -x_offset
            canvas[:, :] = resized[y_offset:y_offset+self.height, start_x:start_x+self.width]
        else:
            # Center if too narrow
            canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        return canvas

    def create_video(self, text_content, audio_file):
        try:
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(step_name, sub_progress=0):
                """Update overall progress bar and status"""
                total_progress = min(1.0, (self.current_step + sub_progress) / self.total_steps)
                progress_bar.progress(total_progress)
                percentage = int(total_progress * 100)
                status_text.text(f"Progress: {percentage}% - {step_name}")

            # Check audio duration
            audio_duration = self._get_audio_duration(audio_file)
            if audio_duration > self.max_duration:
                raise Exception(f"Audio duration ({audio_duration}s) exceeds maximum allowed duration ({self.max_duration}s)")

            # Generate unique filenames with absolute paths
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_output = os.path.join(self.output_dir, f"temp_{timestamp}.mp4")
            final_output = os.path.join(self.output_dir, f"final_{timestamp}.mp4")
            
            # Step 1: Initialize and prepare data (20%)
            self.current_step = 0
            update_progress("Preparing data...")
            
            cleaned_text = self._clean_text(text_content)
            word_chunks = self._chunk_into_words(cleaned_text)
            
            # Step 2: Process audio (20%)
            self.current_step = 0.2
            update_progress("Processing audio...")
            
            audio_duration = self._get_audio_duration(audio_file)
            words_per_second = len(word_chunks) / audio_duration
            frames_per_word = int(30 / words_per_second)

            # Step 3: Generate video frames (40%)
            self.current_step = 0.4
            update_progress("Generating video frames...")
            
            # Get precise audio duration
            audio_duration = self._get_audio_duration(audio_file)
            words = self._chunk_into_words(text_content)
            total_words = len(words)
            
            # Calculate precise timing
            frames_per_second = self.fps
            total_frames = int(audio_duration * frames_per_second)
            words_per_second = total_words / audio_duration
            frames_per_word = frames_per_second / words_per_second
            
            # Generate frames with precise timing
            frame_count = 0
            word_index = 0
            
            while frame_count < total_frames:
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()

                # Process frame to fit 9:16 without stretching
                frame = self._process_background_frame(frame)
                
                # Update word index based on precise timing
                word_index = min(int(frame_count / frames_per_word), total_words - 1)
                
                # Get words to display
                current_words = []
                if word_index < total_words:
                    current_word = words[word_index]
                    if len(current_word) > 10:
                        # Show long word alone
                        current_words = [current_word]
                    else:
                        # Check next word if available
                        current_words = [current_word]
                        if word_index + 1 < total_words:
                            next_word = words[word_index + 1]
                            if len(next_word) <= 10:
                                current_words.append(next_word)
                
                # Add text to frame
                if current_words:
                    display_text = ' '.join(current_words)
                    frame = self._add_text_to_frame(frame, display_text)
                
                out.write(frame)
                frame_count += 1

                # Update progress
                sub_progress = frame_count / total_frames
                update_progress("Generating video frames...", sub_progress)

            cap.release()
            out.release()

            # Step 4: Combine video and audio (15%)
            self.current_step = 0.8
            update_progress("Adding audio...")
            self._combine_video_audio(temp_output, audio_file, final_output)

            # Ensure video is web-compatible
            self._ensure_web_compatible(final_output)
            
            # Log the file location
            st.write(f"Video saved to: {final_output}")
            
            # Verify file exists and is not empty
            if not os.path.exists(final_output):
                raise Exception(f"Output video file not found at {final_output}")
            
            if os.path.getsize(final_output) == 0:
                raise Exception("Output video file is empty")

            # Clear progress indicators after successful completion
            progress_bar.empty()
            status_text.empty()
            
            return final_output

        except Exception as e:
            # Clear progress indicators on error
            if 'progress_bar' in locals():
                progress_bar.empty()
            if 'status_text' in locals():
                status_text.empty()
            raise Exception(f"Error generating video: {str(e)}")

    def _chunk_into_words(self, text):
        """Split text into word chunks"""
        words = text.split()
        return words

    def _get_audio_duration(self, audio_file):
        """Get precise audio duration"""
        try:
            audio = AudioSegment.from_mp3(audio_file)
            return len(audio) / 1000.0  # Convert to seconds
        except Exception as e:
            logging.error(f"Error getting audio duration: {str(e)}")
            # Fallback to ffprobe
            try:
                probe = os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_file}"').read()
                return float(probe)
            except:
                raise Exception("Could not determine audio duration")

    def _combine_video_audio(self, video_path, audio_path, output_path):
        """Combine video with audio using ffmpeg"""
        try:
            cmd = (
                f'ffmpeg -i "{video_path}" -i "{audio_path}" '
                f'-c:v libx264 -preset fast '
                f'-c:a aac -b:a 192k '
                f'-shortest '
                f'-pix_fmt yuv420p '  # Ensure pixel format is compatible
                f'-movflags +faststart '
                f'"{output_path}" -y'
            )
            
            result = os.system(cmd)
            
            if result != 0 or not os.path.exists(output_path):
                raise Exception("Failed to combine video and audio")
                
        except Exception as e:
            logging.error(f"Error combining video and audio: {str(e)}")
            raise

    def _add_text_to_frame(self, frame, text):
        """Add centered text overlay to frame"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        draw = ImageDraw.Draw(pil_image)

        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except:
            font = ImageFont.load_default()

        # Split text into words
        words = text.split()
        display_words = []
        
        # Process words based on length
        for word in words[:self.words_per_frame]:
            if len(word) > 10:
                # If we already have words to display, return current frame
                if display_words:
                    text = ' '.join(display_words)
                else:
                    # Show long word alone
                    text = word
                break
            display_words.append(word)
        
        if not display_words and not text:
            text = ' '.join(words[:self.words_per_frame])

        # Calculate text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position text at center of frame
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw text with outline for better visibility
        outline_color = 'black'
        text_color = 'white'
        outline_width = 4

        # Draw outline
        for dx in [-outline_width, outline_width]:
            for dy in [-outline_width, outline_width]:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)

        # Convert back to OpenCV format
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return frame

    def _clean_text(self, text):
        """Remove markdown symbols and clean text"""
        cleaned = text.replace('*', '').replace('-', '').replace('_', '')
        cleaned = ' '.join(cleaned.split())  # Normalize spaces
        return cleaned

    def _ensure_web_compatible(self, video_path):
        """Convert video to web-compatible format"""
        try:
            temp_path = video_path.replace('.mp4', '_temp.mp4')
            
            # Convert to web-compatible format
            cmd = (
                f'ffmpeg -i "{video_path}" -y '
                f'-c:v libx264 -preset fast '
                f'-c:a aac '
                f'-movflags +faststart '
                f'-pix_fmt yuv420p '  # Ensure pixel format is compatible
                f'"{temp_path}"'
            )
            
            os.system(cmd)
            
            # Replace original with web-compatible version
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                os.replace(temp_path, video_path)
            
        except Exception as e:
            logging.error(f"Error ensuring web compatibility: {str(e)}")