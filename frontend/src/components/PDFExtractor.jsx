import React, { useState, useCallback } from 'react'
import { 
  UploadIcon, 
  FileTextIcon, 
  DownloadIcon, 
  SettingsIcon, 
  CheckCircleIcon, 
  AlertCircleIcon, 
  ClockIcon 
} from './icons'
import FileUpload from './FileUpload'
import TemplateSelector from './TemplateSelector'
import ExtractionProgress from './ExtractionProgress'
import ResultsPanel from './ResultsPanel'
import { extractService } from '../services/api'

const PDFExtractor = () => {
  const [files, setFiles] = useState([])
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [extractionStatus, setExtractionStatus] = useState('idle')
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleFilesSelect = useCallback((selectedFiles) => {
    setFiles(selectedFiles)
    setError('')
  }, [])

  const handleTemplateSelect = useCallback((template) => {
    setSelectedTemplate(template)
    setError('')
  }, [])

  const handleExtract = async () => {
    if (files.length === 0) {
      setError('Please select at least one PDF file')
      return
    }

    if (!selectedTemplate) {
      setError('Please select a template')
      return
    }

    setExtractionStatus('uploading')
    setProgress(0)
    setError('')
    setResult(null)

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 80) {
            clearInterval(progressInterval)
            return 80
          }
          return prev + 10
        })
      }, 1000)

      console.log('Starting extraction with:', {
        files: files.map(f => f.name),
        templateId: selectedTemplate.id,
        templateName: selectedTemplate.name
      })

      // Make API call
      const response = await extractService.extractData(files, selectedTemplate.id)
      
      clearInterval(progressInterval)
      setProgress(100)
      setExtractionStatus('completed')
      setResult(response.data)

      console.log('Extraction completed:', response.data)

    } catch (err) {
      console.error('Extraction error:', err)
      setExtractionStatus('error')
      setError(err.message || 'Extraction failed. Please try again.')
      setProgress(0)
    }
  }

  const handleReset = () => {
    setFiles([])
    setSelectedTemplate(null)
    setExtractionStatus('idle')
    setProgress(0)
    setResult(null)
    setError('')
  }

  const canExtract = files.length > 0 && selectedTemplate && extractionStatus === 'idle'

  return (
    <div>
      <header className="app-header">
        <div className="container">
          <h1>PDF Extraction Tool</h1>
          <p>Extract financial data from PDFs using AI-powered extraction</p>
        </div>
      </header>

      <main className="container">
        {extractionStatus === 'idle' && (
          <div style={{ display: 'grid', gap: '24px' }}>
            <FileUpload 
              files={files} 
              onFilesSelect={handleFilesSelect} 
            />
            
            <TemplateSelector 
              selectedTemplate={selectedTemplate}
              onTemplateSelect={handleTemplateSelect}
            />

            {error && (
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '8px', 
                color: '#ef4444',
                backgroundColor: '#fef2f2',
                padding: '12px 16px',
                borderRadius: '8px',
                border: '1px solid #fecaca'
              }}>
                <AlertCircleIcon width={20} height={20} />
                <span>{error}</span>
              </div>
            )}

            <div style={{ textAlign: 'center' }}>
              <button 
                className={`btn ${canExtract ? 'btn-primary' : 'btn-disabled'}`}
                onClick={handleExtract}
                disabled={!canExtract}
                style={{ 
                  opacity: canExtract ? 1 : 0.6,
                  cursor: canExtract ? 'pointer' : 'not-allowed'
                }}
              >
                <FileTextIcon width={18} height={18} />
                Extract Data from {files.length} File{files.length !== 1 ? 's' : ''}
                {selectedTemplate && ` using ${selectedTemplate.name}`}
              </button>
            </div>
          </div>
        )}

        {(extractionStatus === 'uploading' || extractionStatus === 'processing') && (
          <ExtractionProgress 
            status={extractionStatus}
            progress={progress}
            files={files}
            template={selectedTemplate}
          />
        )}

        {extractionStatus === 'completed' && result && (
          <ResultsPanel 
            result={result}
            files={files}
            template={selectedTemplate}
            onReset={handleReset}
          />
        )}

        {extractionStatus === 'error' && (
          <div className="card" style={{ textAlign: 'center' }}>
            <AlertCircleIcon width={48} height={48} color="#ef4444" style={{ margin: '0 auto 16px' }} />
            <h2 style={{ marginBottom: '8px', color: '#1e293b' }}>Extraction Failed</h2>
            <p style={{ marginBottom: '16px', color: '#64748b' }}>{error}</p>
            <div style={{ 
              backgroundColor: '#f8fafc', 
              padding: '12px', 
              borderRadius: '8px',
              marginBottom: '24px',
              textAlign: 'left',
              fontSize: '14px'
            }}>
              <strong>Troubleshooting tips:</strong>
              <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
                <li>Check if the PDF files contain extractable text</li>
                <li>Try with smaller PDF files first</li>
                <li>Ensure you have a stable internet connection</li>
                <li>Try selecting a different template</li>
              </ul>
            </div>
            <button className="btn btn-primary" onClick={handleReset}>
              Try Again
            </button>
          </div>
        )}
      </main>
    </div>
  )
}

export default PDFExtractor