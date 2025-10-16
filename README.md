# PDF Extraction Tool

A full-stack application that uses AI to intelligently extract structured data from PDF documents and export it to Excel format.

🔗 **Live Demo**: [https://pdf-extraction-tool-2.onrender.com](https://pdf-extraction-tool-2.onrender.com)

## 🚀 Features

- **Smart PDF Parsing**: Extract text and tables from PDF documents
- **AI-Powered Extraction**: Uses LLM (Groq) to intelligently understand and extract data
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
- **Groq API**: LLM-powered data extraction
- **pdfplumber**: PDF parsing library
- **openpyxl**: Excel file generation
- **Python 3.8+**

### Frontend
- **React 19**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **Lucide React**: Icon library
- **CSS3**: Styling

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **Groq API Key** (Get it from [Groq Console](https://console.groq.com))

## 🚦 Local Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sagarss2664/PDF_Extraction_Tool.git
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
# Add your Groq API key and other configurations
echo "GROQ_API_KEY=your_api_key_here" > .env
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
GROQ_API_KEY=your_groq_api_key_here
UPLOAD_DIR=uploads
OUTPUT_DIR=output
```

## 🎯 Local Usage

### Starting the Backend
```bash
cd backend
python run.py
```

The backend server will start at `http://localhost:8000`

**Health Check**: Visit `http://localhost:8000/api/health` to verify the server is running.

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

## 🌐 Deployment on Render

### Backend Deployment (Web Service)

1. **Create a Render Account**: Sign up at [render.com](https://render.com)

2. **Create New Web Service**:
   - Go to Dashboard → New → Web Service
   - Connect your GitHub repository
   - Select the `PDF_Extraction_Tool` repository

3. **Configure the Web Service**:
```
   Name: pdf-extraction-tool-backend (or your choice)
   Region: Choose closest to your users
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

4. **Add Environment Variables**:
   - Go to Environment tab
   - Add: `GROQ_API_KEY` = your_groq_api_key
   - Add: `UPLOAD_DIR` = uploads
   - Add: `OUTPUT_DIR` = output

5. **Deploy**: Click "Create Web Service"

6. **Verify Deployment**:
   - Your backend will be available at: `https://your-service-name.onrender.com`
   - Check health: `https://your-service-name.onrender.com/api/health`
   - Example: `https://pdf-extraction-tool-1.onrender.com/api/health`

### Frontend Deployment (Static Site)

1. **Build the Frontend Locally**:
```bash
   cd frontend
   npm run build
```
   This creates a `dist` folder with production-ready files.

2. **Create New Static Site**:
   - Go to Dashboard → New → Static Site
   - Connect your GitHub repository
   - Select the `PDF_Extraction_Tool` repository

3. **Configure the Static Site**:
```
   Name: pdf-extraction-tool-frontend (or your choice)
   Region: Choose closest to your users
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
```

4. **Update API URL**:
   - Before deploying, update the API base URL in `frontend/src/services/api.js`:
```javascript
   const API_BASE_URL = 'https://pdf-extraction-tool-1.onrender.com';
```

5. **Deploy**: Click "Create Static Site"

6. **Access Your App**:
   - Frontend URL: `https://your-static-site-name.onrender.com`
   - Example: `https://pdf-extraction-tool-2.onrender.com`

### Important Render Notes

- **Free Tier Limitations**: 
  - Web services spin down after 15 minutes of inactivity
  - First request after inactivity may take 30-60 seconds (cold start)
  - Consider upgrading to paid plan for production use

- **Environment Variables**: Always keep your API keys secure in Render's environment variables, never commit them to GitHub

- **Custom Domains**: You can add custom domains in the Settings tab of your Render service

## 🔌 API Endpoints

**Base URL**: `https://pdf-extraction-tool-1.onrender.com` (Production) or `http://localhost:8000` (Local)

### Health Check
```http
GET /api/health
```

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
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pydantic==2.9.2
pdfplumber==0.10.3
openpyxl==3.1.2
pandas==2.2.3
python-dotenv==1.0.0
openai==1.3.7
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
requests>=2.31.0
groq
```

### Frontend (package.json)
```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "lucide-react": "^0.545.0",
    "react": "^19.1.1",
    "react-dom": "^19.1.1"
  },
  "devDependencies": {
    "@eslint/js": "^9.36.0",
    "@types/react": "^19.1.16",
    "@types/react-dom": "^19.1.9",
    "@vitejs/plugin-react": "^5.0.4",
    "eslint": "^9.36.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.22",
    "globals": "^16.4.0",
    "vite": "^7.1.7"
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Authors

- Sagar Shegunashi - [GitHub Profile](https://github.com/Sagarss2664)

## 🙏 Acknowledgments

- Groq for providing the LLM API
- FastAPI community
- React and Vite teams
- Render for hosting services

## 📧 Contact

For questions or support, please open an issue on GitHub or contact sagarshegunasi2664@gmail.com

## 🐛 Known Issues

- Large PDF files (>10MB) may take longer to process
- Some PDF formats with complex layouts may require manual review
- First request on Render free tier may experience cold start delay

## 🗺️ Roadmap

- [x] Deploy backend to Render
- [x] Deploy frontend to Render
- [ ] Support for multiple PDF formats
- [ ] Batch processing capabilities
- [ ] Custom template builder UI
- [ ] User authentication and file management
- [ ] Docker containerization
- [ ] Upgrade to paid hosting for better performance

## 🔒 Security Notes

- Never commit API keys or sensitive credentials to the repository
- Always use environment variables for configuration
- Keep dependencies updated to patch security vulnerabilities

---

**Note**: Make sure to add your Groq API key to the `.env` file (local) or Render environment variables (production) before running the application.

**Live Application**: 
- Frontend: [https://pdf-extraction-tool-2.onrender.com](https://pdf-extraction-tool-2.onrender.com)
- Backend API: [https://pdf-extraction-tool-1.onrender.com](https://pdf-extraction-tool-1.onrender.com)
- Health Check: [https://pdf-extraction-tool-1.onrender.com/api/health](https://pdf-extraction-tool-1.onrender.com/api/health)
