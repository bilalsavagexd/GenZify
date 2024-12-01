# GenZify 🧠

## 🌟 **Introduction**  
Imagine a world where your lecture notes are so entertaining, You forget your studying!

## 📦 **Tech Stack:**
- **Frontend - Streamlit**

- **Backend - Python**

- **AI/ML Services - Groq AI**
  
- **File Processing - PyPDF2**
  
- **Text-to-Speech - Eleven Lab**

- **Video Processing - OpenCV (cv2)**
  
- **PIL (Python Imaging Library)**
  
- **NumPy**

- **Storage - Supabase**

- **Environment/Configuration - python-dotenv**

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
