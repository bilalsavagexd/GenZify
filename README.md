# GenZify

## 🌟 **Introduction**  
Imagine a world where your lecture notes are so entertaining, You forget your studying.

## 📦 **Tech Stack:**

### Frontend 🎨
- **Streamlit**

### Backend/Processing 🔄
- **Python 3.8+**
  - Core programming language
  - Async operations
  - File handling

### AI/ML Services 🤖
- **Groq AI**
  - Text generation
  - Question answering
  - Summary generation
  - Gen Z style conversion

### File Processing 📄
- **PyPDF2**
  - PDF text extraction
  - Document parsing
  - Content extraction

### Text-to-Speech 🗣️
- **gTTS (Google Text-to-Speech)**
  - Text to audio conversion
  - Multiple language support
  - Speech synthesis

### Video Processing 🎥
- **OpenCV (cv2)**
  - Video frame manipulation
  - Image processing
  - Frame composition
- **PIL (Python Imaging Library)**
  - Image creation
  - Text overlay
  - Image manipulation
- **NumPy**
  - Frame manipulation

### Storage 💾
- **Supabase**
  - Video storage

### Environment/Configuration ⚙️
- **python-dotenv**

## **Data Flow Diagram:**
```
User Uploads PDF
      │
      ▼
PDF Processor
  │
  ▼
User Choice ─────────────────────┐
  │                              │
  ▼                              ▼
LLM Generates Ans.         Video Generation
  │                              │
  ▼                              ▼
Display Answer              1. LLM Summary
                                 │
                                 ▼
                            2. TTS Engine
                                 │
                                 ▼
Background Video ──►       3. Video Generator
                                 │
                                 ▼
                           4. Storage Manager
                                 │
                                 ▼
                           5. Display Video
```
## 📅 **Future Tasks**  
- [ ] 🔄 **Change Entire TechStack**  
- [ ] 🤔 **Allow Users to Ask Follow-Up Questions** and Implement a **History Feature**  
- [ ] 📤 **Allow Users to Share and Download Generated Videos**
