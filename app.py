import streamlit as st
from pdf_processor import PDFProcessor
from video_generator import VideoGenerator
from llm_handler import LLMHandler
from tts_handler import TTSHandler
from storage_manager import StorageManager
import os
import logging

class EducationalContentApp:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.video_generator = VideoGenerator()
        self.llm_handler = LLMHandler()
        self.tts_handler = TTSHandler()
        self.storage = StorageManager()
        
        # Initialize session state
        if 'text_content' not in st.session_state:
            st.session_state.text_content = None
    
    def main(self):
        st.set_page_config(page_title="GenZify", page_icon="🚽", layout="wide")
        
        st.title("🧠 GenZify")
        st.markdown("Turning brain rot into straight A's—learning made fun with memes, slang, and parkour videos.")
        
        # Add custom CSS for dark theme and answer formatting
        st.markdown("""
            <style>
            /* Button styles */
            .stButton > button {
                background-color: #1E1E1E !important;
                color: white !important;
                border: 1px solid #333333 !important;
                border-radius: 8px !important;
                padding: 10px 20px !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
                width: auto !important;
                display: inline-flex !important;
                align-items: center !important;
                margin-right: 10px !important;
                white-space: nowrap !important;
            }
            
            /* Dark theme for input and expander */
            .stExpander {
                background-color: #0E1117 !important;
                border-color: #262730 !important;
            }
            
            .stTextInput > div > div {
                background-color: #262730 !important;
                color: white !important;
            }
            
            /* Answer container styling */
            .answer-container {
                background-color: #1E1E1E !important;
                border-radius: 8px !important;
                padding: 15px !important;
                margin-top: 10px !important;
                color: #FFFFFF !important;
                line-height: 1.5 !important;
            }
            
            /* Remove default streamlit margins */
            .element-container {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .stMarkdown {
                background-color: transparent !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # File upload section
        uploaded_file = st.file_uploader(
            "Upload your PDF notes", 
            type=['pdf'],
            key="pdf_uploader"
        )
        
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                try:
                    st.session_state.text_content = self.pdf_processor.extract_text(uploaded_file)
                    st.success("PDF processed successfully!")
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
        
        if st.session_state.text_content:
            with st.expander("💭 Ask a question about your notes"):
                question = st.text_input("Your question:", key="question_input")
                
                # Use a single row for buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    normal_answer = st.button("🤖 Answer", key="answer_button")
                    
                    if normal_answer:
                        with st.spinner("Generating answer..."):
                            try:
                                answer = self.llm_handler.generate_answer(
                                    question, 
                                    st.session_state.text_content, 
                                    genzify=False
                                )
                                st.markdown(
                                    f'''
                                    <div class="answer-container">
                                        💡 Question: {question}
                                        <br><br>
                                        {answer}
                                    </div>
                                    ''', 
                                    unsafe_allow_html=True
                                )
                            except Exception as e:
                                st.error(f"Error generating answer: {str(e)}")
                
                with col2:
                    genzify_answer = st.button("🚽 Genzify!", key="genzify_button")
                    
                    if genzify_answer:
                        with st.spinner("Generating Gen Z style answer..."):
                            try:
                                answer = self.llm_handler.generate_answer(
                                    question, 
                                    st.session_state.text_content, 
                                    genzify=True
                                )
                                st.markdown(
                                    f'''
                                    <div class="answer-container">
                                        🔥 Question: {question}
                                        <br><br>
                                        {answer}
                                    </div>
                                    ''', 
                                    unsafe_allow_html=True
                                )
                            except Exception as e:
                                st.error(f"Error generating answer: {str(e)}")
            
            # Video generation
            if st.button("🚽 PDF to Brainrot", key="video_button"):
                try:
                    with st.spinner("Generating summary..."):
                        summary = self.llm_handler.generate_summary(st.session_state.text_content)
                    
                    with st.spinner("Converting to speech..."):
                        audio_file = self.tts_handler.generate_speech(summary)
                    
                    with st.spinner("Creating video..."):
                        video_file = self.video_generator.create_video(summary, audio_file)
                    
                    if os.path.exists(video_file):
                        st.success("🎥 Your video is ready!")
                        with open(video_file, 'rb') as video_bytes:
                            st.video(video_bytes.read())
                        
                except Exception as e:
                    st.error(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    app = EducationalContentApp()
    app.main()

