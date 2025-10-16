import React, { useState } from 'react'
import { CheckCircleIcon, DownloadIcon, FileTextIcon } from './icons'
import { extractService } from '../services/api'

const ResultsPanel = ({ result, files, template, onReset }) => {
  const [downloading, setDownloading] = useState(false)

  const handleDownload = async () => {
    if (!result?.job_id) return

    setDownloading(true)
    try {
      const response = await extractService.downloadFile(result.job_id)
      
      // Create blob and download
      const blob = new Blob([response.data], { 
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      
      // Generate better filename
      const timestamp = new Date().toISOString().split('T')[0]
      const templateSuffix = template?.id === 1 ? 'Private_Equity' : 'Portfolio_Summary'
      link.download = `Extracted_Data_${templateSuffix}_${timestamp}.xlsx`
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download file. Please try again.')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="card">
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <CheckCircleIcon width={48} height={48} color="#10b981" style={{ margin: '0 auto 16px' }} />
        <h2 style={{ marginBottom: '8px', color: '#1e293b' }}>
          Extraction Complete!
        </h2>
        <p style={{ color: '#64748b' }}>
          Your data has been successfully extracted and formatted using {template?.name}
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gap: '16px',
        marginBottom: '24px'
      }}>
        <div style={{ 
          backgroundColor: '#f0f9ff', 
          border: '1px solid #bae6fd',
          borderRadius: '8px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
            <FileTextIcon width={20} height={20} color="#0369a1" />
            <h3 style={{ color: '#0369a1', margin: 0 }}>Extraction Summary</h3>
          </div>
          <div style={{ display: 'grid', gap: '8px', fontSize: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#475569' }}>Job ID:</span>
              <span style={{ color: '#1e293b', fontFamily: 'monospace' }}>{result.job_id}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#475569' }}>Status:</span>
              <span style={{ color: '#10b981', fontWeight: '600' }}>{result.status}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#475569' }}>Template:</span>
              <span style={{ color: '#1e293b', fontWeight: '500' }}>{template?.name}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#475569' }}>Files Processed:</span>
              <span style={{ color: '#1e293b' }}>{files.length} PDF{files.length !== 1 ? 's' : ''}</span>
            </div>
            {result.message && (
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#475569' }}>Message:</span>
                <span style={{ color: '#1e293b' }}>{result.message}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
        <button 
          className="btn btn-success"
          onClick={handleDownload}
          disabled={downloading}
          style={{ minWidth: '200px' }}
        >
          {downloading ? (
            <>
              <div className="loading-spinner" style={{ width: '16px', height: '16px' }}></div>
              Downloading Excel...
            </>
          ) : (
            <>
              <DownloadIcon width={18} height={18} />
              Download Excel File
            </>
          )}
        </button>
        
        <button 
          className="btn btn-secondary"
          onClick={onReset}
          style={{ minWidth: '160px' }}
        >
          Extract More Files
        </button>
      </div>

      <div style={{ 
        marginTop: '24px', 
        padding: '12px', 
        backgroundColor: '#f1f5f9', 
        borderRadius: '8px',
        textAlign: 'center',
        fontSize: '14px',
        color: '#64748b'
      }}>
        <strong>Template Used:</strong> {template?.name} • 
        <strong> Generated:</strong> {new Date().toLocaleString()}
      </div>
    </div>
  )
}
//Final one
export default ResultsPanel
