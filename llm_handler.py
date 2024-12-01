import os
import logging
from groq import Groq
import time

class LLMHandler:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv('GROQ_API_KEY')
        )

    def generate_summary(self, text_content, timeout=30):
        """Generate summary with timeout"""
        try:
            start_time = time.time()
            
            messages = [
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                {"role": "user", "content": f"Please create a clear, concise summary of the following text, focusing on the key points: {text_content}"}
            ]
            
            while time.time() - start_time < timeout:
                try:
                    response = self.client.chat.completions.create(
                        model="llama-3.1-70b-versatile",  # or your preferred Groq model
                        messages=messages,
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    return response.choices[0].message.content
                    
                except Exception as e:
                    if time.time() - start_time >= timeout:
                        raise Exception("Request timed out. Please try again.")
                    time.sleep(1)  # Wait before retrying
            
            raise Exception("Request timed out. Please try again.")
            
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def generate_answer(self, question, context, genzify=False):
        """Generate answer with Groq"""
        try:
            system_prompt = """You are a helpful assistant."""
            if genzify:
                system_prompt = """You are a Gen Z expert who responds in Gen Z style language. 
                Use emojis, slang, and casual tone while keeping the information accurate.Make it as much Genz Language like as possible"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]

            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")