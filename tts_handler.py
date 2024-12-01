from gtts import gTTS
import os
import streamlit as st
from pydub import AudioSegment

class TTSHandler:
    def __init__(self):
        self.temp_dir = "temp_audio"
        os.makedirs(self.temp_dir, exist_ok=True)

    def generate_speech(self, text, progress_callback=None):
        """Generate speech using Google Text-to-Speech"""
        try:
            # Create progress indicators if not provided
            if not progress_callback:
                progress_bar = st.progress(0)
                status_text = st.empty()
                def progress_callback(progress, message):
                    progress_bar.progress(progress)
                    status_text.text(message)

            # Split text into chunks
            chunks = self._split_into_chunks(text)
            total_chunks = len(chunks)
            audio_parts = []

            # Generate audio for each chunk
            for i, chunk in enumerate(chunks, 1):
                progress = (i - 1) / total_chunks
                progress_callback(progress, f"Converting to speech... ({i}/{total_chunks})")

                # Generate speech
                tts = gTTS(text=chunk, lang='en', slow=False)
                temp_file = os.path.join(self.temp_dir, f"temp_audio_{i}.mp3")
                tts.save(temp_file)
                audio_parts.append(temp_file)

            # Combine audio parts if multiple chunks
            if len(audio_parts) > 1:
                progress_callback(0.9, "Combining audio chunks...")
                combined = AudioSegment.from_mp3(audio_parts[0])
                for audio_file in audio_parts[1:]:
                    combined += AudioSegment.from_mp3(audio_file)
                
                output_file = os.path.join(self.temp_dir, "output.mp3")
                combined.export(output_file, format="mp3")
            else:
                output_file = audio_parts[0]

            # Cleanup temporary files
            for temp_file in audio_parts:
                if temp_file != output_file:
                    try:
                        os.remove(temp_file)
                    except:
                        pass

            progress_callback(1.0, "Speech conversion complete!")
            return output_file

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")

    def _split_into_chunks(self, text, max_chars=5000):
        """Split text into smaller chunks for TTS processing"""
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if not sentence.endswith('.'):
                sentence += '.'
                
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_chars:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def __del__(self):
        """Cleanup temporary directory on object destruction"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass