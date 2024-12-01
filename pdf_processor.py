import PyPDF2
import tempfile
import os
import time
import logging

class PDFProcessor:
    def extract_text(self, pdf_file):
        temp_file = None
        pdf_reader = None
        try:
            # Validate file name and type
            if not pdf_file.name.lower().endswith('.pdf'):
                raise Exception("Invalid file type. Please upload a PDF file.")
            
            # Log file details
            logging.info(f"Processing file: {pdf_file.name}, size: {pdf_file.size} bytes")
            
            # Create a temporary file to handle StreamlitUploadedFile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file.write(pdf_file.getvalue())
            temp_file.close()  # Close the file explicitly
            
            # Open PDF with PyPDF2
            with open(temp_file.name, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        text += page_text + "\n"
                        logging.info(f"Successfully processed page {page_num + 1}")
                    except Exception as page_error:
                        logging.error(f"Error processing page {page_num + 1}: {str(page_error)}")
            
            if not text.strip():
                raise Exception("No text could be extracted from the PDF")
                
            return text
            
        except Exception as e:
            logging.error(f"PDF processing error: {str(e)}")
            raise Exception(f"Error processing PDF: {str(e)}")
            
        finally:
            # Clean up: Make sure to close and delete the temp file
            if pdf_reader:
                del pdf_reader  # Release the PDF reader
                
            if temp_file:
                try:
                    # Add a small delay to ensure file is released
                    time.sleep(0.1)
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                        logging.info("Temporary file cleaned up successfully")
                except Exception as e:
                    logging.warning(f"Could not delete temporary file: {str(e)}")
