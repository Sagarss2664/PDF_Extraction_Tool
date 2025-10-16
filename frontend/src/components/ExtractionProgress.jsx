import React from 'react'
import { ClockIcon, FileTextIcon, SettingsIcon } from './icons'

const ExtractionProgress = ({ status, progress, files, template }) => {
  const getStatusText = () => {
    switch (status) {
      case 'uploading':
        return 'Uploading files...'
      case 'processing':
        return 'Extracting data with AI...'
      default:
        return 'Processing...'
    }
  }

  const getStatusColor = () => {
    switch (status) {
      case 'uploading':
        return '#f59e0b'
      case 'processing':
        return '#3b82f6'
      default:
        return '#6b7280'
    }
  }

  return (
    <div className="card">
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <ClockIcon width={48} height={48} color={getStatusColor()} style={{ margin: '0 auto 16px' }} />
        <h2 style={{ marginBottom: '8px', color: '#1e293b' }}>
          {getStatusText()}
        </h2>
        <p style={{ color: '#64748b' }}>
          This may take a few minutes depending on file size and complexity
        </p>
      </div>

      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontSize: '14px', color: '#374151' }}>Progress</span>
          <span style={{ fontSize: '14px', color: '#6b7280' }}>{Math.round(progress)}%</span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progress}%`, backgroundColor: getStatusColor() }}
          ></div>
        </div>
      </div>

      <div style={{ display: 'grid', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <FileTextIcon width={20} height={20} color="#6b7280" />
          <div>
            <div style={{ fontSize: '14px', color: '#374151' }}>Files</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              {files.length} PDF file{files.length !== 1 ? 's' : ''}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <SettingsIcon width={20} height={20} color="#6b7280" />
          <div>
            <div style={{ fontSize: '14px', color: '#374151' }}>Template</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              {template?.name}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExtractionProgress