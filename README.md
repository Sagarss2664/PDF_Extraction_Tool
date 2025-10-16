# PDF Extraction Tool

A full-stack application that uses AI to intelligently extract structured data from PDF documents and export it to Excel format.

## 🚀 Features

- **Smart PDF Parsing**: Extract text and tables from PDF documents
- **AI-Powered Extraction**: Uses LLM (OpenAI) to intelligently understand and extract data
- **Template-Based Extraction**: Customizable extraction templates for different document types
- **Excel Export**: Generate structured Excel files from extracted data
- **Modern UI**: Clean, responsive React interface with real-time progress tracking
- **RESTful API**: FastAPI backend with async support

## 📁 Project Structure
```
PDF_Extraction_Tool/
│
├── backend/                    # FastAPI server
│   ├── app/
│   │   ├── api/               # API route handlers
│   │   ├── core/              # Core backend logic
│   │   │   ├── llm_client.py
│   │   │   ├── pdf_parser.py
│   │   │   └── prompt_builder.py
│   │   ├── models/            # Database/schema models
│   │   ├── services/          # Business logic services
│   │   │   ├── excel_generator.py
│   │   │   ├── llm_processor.py
│   │   │   ├── pdf_extractor.py
│   │   │   └── pdf_processor.py
│   │   ├── utils/             # Utility functions
│   │   └── main.py            # FastAPI entry point
│   │
│   ├── output/                # Generated Excel files
│   ├── uploads/               # Uploaded PDF files
│   ├── requirements.txt       # Python dependencies
│   └── run.py                 # Server launcher
│
└── frontend/                  # React + Vite application
    ├── src/
    │   ├── components/        # React components
    │   │   ├── ExtractionProgress.jsx
    │   │   ├── FileUpload.jsx
    │   │   ├── PDFExtractor.jsx
    │   │   ├── ResultsPanel.jsx
    │   │   └── TemplateSelector.jsx
    │   ├── services/          # API integration
    │   │   └── api.js
    │   ├── App.jsx
    │   └── main.jsx
    │
    ├── package.json
    └── vite.config.js
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **OpenAI API**: LLM-powered data extraction
- **PyPDF2/pdfplumber**: PDF parsing libraries
- **openpyxl**: Excel file generation
- **Python 3.8+**

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **CSS3**: Styling

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **OpenAI API Key**

## 🚦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/PDF_Extraction_Tool.git
cd PDF_Extraction_Tool
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Add your OpenAI API key and other configurations
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

## 🔧 Configuration

Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads
OUTPUT_DIR=output
```

## 🎯 Usage

### Starting the Backend
```bash
cd backend
python run.py
```

The backend server will start at `http://localhost:8000`

### Starting the Frontend
```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:5173`

### Using the Application

1. **Upload PDF**: Drag and drop or select a PDF file
2. **Select Template**: Choose an extraction template or create a custom one
3. **Extract Data**: Click extract to process the PDF
4. **Download Results**: Download the generated Excel file

## 🔌 API Endpoints

### Upload PDF
```http
POST /api/upload
Content-Type: multipart/form-data
```

### Extract Data
```http
POST /api/extract
Content-Type: application/json
Body: {
  "file_path": "string",
  "template": "string"
}
```

### Download Excel
```http
GET /api/download/{filename}
```

## 📦 Dependencies

### Backend (requirements.txt)
```txt
fastapi
uvicorn
python-multipart
openai
pdfplumber
openpyxl
python-dotenv
aiofiles
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- OpenAI for providing the LLM API
- FastAPI community
- React and Vite teams

## 📧 Contact

For questions or support, please open an issue on GitHub or contact [your.email@example.com]

## 🐛 Known Issues

- Large PDF files (>10MB) may take longer to process
- Some PDF formats with complex layouts may require manual review

## 🗺️ Roadmap

- [ ] Support for multiple file formats (DOCX, images)
- [ ] Batch processing capabilities
- [ ] Custom template builder UI
- [ ] User authentication and file management
- [ ] Cloud deployment configuration
- [ ] Docker containerization

---

**Note**: Make sure to add your OpenAI API key to the `.env` file before running the application.
