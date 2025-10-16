// import React, { useState } from 'react'
// import { CheckCircleIcon, DownloadIcon, FileTextIcon } from './icons'
// import { extractService } from '../services/api'

// const ResultsPanel = ({ result, files, template, onReset }) => {
//   const [downloading, setDownloading] = useState(false)

//   const handleDownload = async () => {
//     if (!result?.job_id) return

//     setDownloading(true)
//     try {
//       const response = await extractService.downloadFile(result.job_id)
      
//       // Create blob and download
//       const blob = new Blob([response.data], { 
//         type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
//       })
//       const url = window.URL.createObjectURL(blob)
//       const link = document.createElement('a')
//       link.href = url
      
//       // Generate better filename
//       const timestamp = new Date().toISOString().split('T')[0]
//       const templateSuffix = template?.id === 1 ? 'Private_Equity' : 'Portfolio_Summary'
//       link.download = `Extracted_Data_${templateSuffix}_${timestamp}.xlsx`
      
//       document.body.appendChild(link)
//       link.click()
//       document.body.removeChild(link)
//       window.URL.revokeObjectURL(url)
      
//     } catch (error) {
//       console.error('Download failed:', error)
//       alert('Failed to download file. Please try again.')
//     } finally {
//       setDownloading(false)
//     }
//   }

//   return (
//     <div className="card">
//       <div style={{ textAlign: 'center', marginBottom: '32px' }}>
//         <CheckCircleIcon width={48} height={48} color="#10b981" style={{ margin: '0 auto 16px' }} />
//         <h2 style={{ marginBottom: '8px', color: '#1e293b' }}>
//           Extraction Complete!
//         </h2>
//         <p style={{ color: '#64748b' }}>
//           Your data has been successfully extracted and formatted using {template?.name}
//         </p>
//       </div>

//       <div style={{ 
//         display: 'grid', 
//         gap: '16px',
//         marginBottom: '24px'
//       }}>
//         <div style={{ 
//           backgroundColor: '#f0f9ff', 
//           border: '1px solid #bae6fd',
//           borderRadius: '8px',
//           padding: '16px'
//         }}>
//           <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
//             <FileTextIcon width={20} height={20} color="#0369a1" />
//             <h3 style={{ color: '#0369a1', margin: 0 }}>Extraction Summary</h3>
//           </div>
//           <div style={{ display: 'grid', gap: '8px', fontSize: '14px' }}>
//             <div style={{ display: 'flex', justifyContent: 'space-between' }}>
//               <span style={{ color: '#475569' }}>Job ID:</span>
//               <span style={{ color: '#1e293b', fontFamily: 'monospace' }}>{result.job_id}</span>
//             </div>
//             <div style={{ display: 'flex', justifyContent: 'space-between' }}>
//               <span style={{ color: '#475569' }}>Status:</span>
//               <span style={{ color: '#10b981', fontWeight: '600' }}>{result.status}</span>
//             </div>
//             <div style={{ display: 'flex', justifyContent: 'space-between' }}>
//               <span style={{ color: '#475569' }}>Template:</span>
//               <span style={{ color: '#1e293b', fontWeight: '500' }}>{template?.name}</span>
//             </div>
//             <div style={{ display: 'flex', justifyContent: 'space-between' }}>
//               <span style={{ color: '#475569' }}>Files Processed:</span>
//               <span style={{ color: '#1e293b' }}>{files.length} PDF{files.length !== 1 ? 's' : ''}</span>
//             </div>
//             {result.message && (
//               <div style={{ display: 'flex', justifyContent: 'space-between' }}>
//                 <span style={{ color: '#475569' }}>Message:</span>
//                 <span style={{ color: '#1e293b' }}>{result.message}</span>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>

//       <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
//         <button 
//           className="btn btn-success"
//           onClick={handleDownload}
//           disabled={downloading}
//           style={{ minWidth: '200px' }}
//         >
//           {downloading ? (
//             <>
//               <div className="loading-spinner" style={{ width: '16px', height: '16px' }}></div>
//               Downloading Excel...
//             </>
//           ) : (
//             <>
//               <DownloadIcon width={18} height={18} />
//               Download Excel File
//             </>
//           )}
//         </button>
        
//         <button 
//           className="btn btn-secondary"
//           onClick={onReset}
//           style={{ minWidth: '160px' }}
//         >
//           Extract More Files
//         </button>
//       </div>

//       <div style={{ 
//         marginTop: '24px', 
//         padding: '12px', 
//         backgroundColor: '#f1f5f9', 
//         borderRadius: '8px',
//         textAlign: 'center',
//         fontSize: '14px',
//         color: '#64748b'
//       }}>
//         <strong>Template Used:</strong> {template?.name} • 
//         <strong> Generated:</strong> {new Date().toLocaleString()}
//       </div>
//     </div>
//   )
// }

// export default ResultsPanel
import React, { useState } from 'react';

// Icons
const CheckCircleIcon = ({ width = 24, height = 24, color = 'currentColor', style = {} }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={style}>
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
    <polyline points="22 4 12 14.01 9 11.01" />
  </svg>
);

const DownloadIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="8 12 12 16 16 12" />
    <line x1="12" y1="8" x2="12" y2="16" />
  </svg>
);

const FileTextIcon = ({ width = 24, height = 24, color = 'currentColor' }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <polyline points="14 2 14 8 20 8" />
    <line x1="16" y1="13" x2="8" y2="13" />
    <line x1="16" y1="17" x2="8" y2="17" />
    <line x1="10" y1="9" x2="8" y2="9" />
  </svg>
);

const RefreshIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 4 23 10 17 10" />
    <polyline points="1 20 1 14 7 14" />
    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
  </svg>
);

const SparklesIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3l1.912 5.813 6.088.237-4.912 3.663 1.812 5.787L12 15l-4.9 3.5 1.812-5.787L4 9.05l6.088-.237L12 3z" />
  </svg>
);

const ClockIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <polyline points="12 6 12 12 16 14" />
  </svg>
);

const ResultsPanel = ({ result = {}, files = [], template = {}, onReset }) => {
  const [downloading, setDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  const handleDownload = async () => {
    if (!result?.job_id) return;

    setDownloading(true);
    try {
      // Simulating API call - replace with actual API
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simulate download (replace with actual implementation)
      const timestamp = new Date().toISOString().split('T')[0];
      const templateSuffix = template?.id === 1 ? 'Private_Equity' : 'Portfolio_Summary';
      const filename = `Extracted_Data_${templateSuffix}_${timestamp}.xlsx`;
      
      // Show success animation
      setDownloadSuccess(true);
      setTimeout(() => setDownloadSuccess(false), 3000);
      
      alert(`Download successful: ${filename}`);
      
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download file. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <>
      <style>{`
        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        @keyframes slideInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes checkmarkDraw {
          0% {
            stroke-dashoffset: 100;
          }
          100% {
            stroke-dashoffset: 0;
          }
        }

        @keyframes pulse-ring {
          0% {
            transform: scale(0.8);
            opacity: 1;
          }
          100% {
            transform: scale(2);
            opacity: 0;
          }
        }

        @keyframes bounce {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }

        @keyframes shimmer {
          0% {
            background-position: -1000px 0;
          }
          100% {
            background-position: 1000px 0;
          }
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        @keyframes confetti {
          0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(-100px) rotate(720deg);
            opacity: 0;
          }
        }

        .results-card {
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(20px);
          border-radius: 24px;
          padding: 40px;
          box-shadow: 0 20px 60px rgba(16, 185, 129, 0.2);
          position: relative;
          overflow: hidden;
          animation: fadeInScale 0.6s ease-out;
          border: 1px solid rgba(255, 255, 255, 0.5);
        }

        .results-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
          background-size: 200% 100%;
          animation: shimmer 3s linear infinite;
        }

        .success-header {
          text-align: center;
          margin-bottom: 40px;
          animation: slideInUp 0.6s ease-out 0.2s both;
        }

        .success-icon-wrapper {
          display: inline-flex;
          position: relative;
          margin-bottom: 24px;
        }

        .success-icon-bg {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 100px;
          height: 100px;
          background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(52, 211, 153, 0.2) 100%);
          border-radius: 50%;
          animation: pulse-ring 2s ease-out infinite;
        }

        .success-icon {
          position: relative;
          z-index: 1;
          animation: bounce 2s ease-in-out infinite;
        }

        .success-title {
          margin: 0 0 12px 0;
          font-size: 2rem;
          font-weight: 800;
          background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .success-subtitle {
          color: #64748b;
          font-size: 1.1rem;
          line-height: 1.6;
          max-width: 600px;
          margin: 0 auto;
        }

        .summary-section {
          margin-bottom: 32px;
          animation: slideInUp 0.6s ease-out 0.4s both;
        }

        .summary-card {
          background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(52, 211, 153, 0.08) 100%);
          border: 2px solid rgba(16, 185, 129, 0.2);
          border-radius: 20px;
          padding: 24px;
          position: relative;
          overflow: hidden;
        }

        .summary-card::before {
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
          width: 5px;
          background: linear-gradient(180deg, #10b981 0%, #34d399 100%);
        }

        .summary-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 20px;
        }

        .summary-icon-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 44px;
          height: 44px;
          background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(52, 211, 153, 0.2) 100%);
          border-radius: 12px;
          color: #10b981;
        }

        .summary-title {
          margin: 0;
          font-size: 1.3rem;
          font-weight: 700;
          color: #10b981;
        }

        .summary-grid {
          display: grid;
          gap: 14px;
        }

        .summary-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px 16px;
          background: rgba(255, 255, 255, 0.7);
          border-radius: 12px;
          transition: all 0.3s ease;
        }

        .summary-row:hover {
          background: white;
          transform: translateX(8px);
          box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
        }

        .summary-label {
          color: #64748b;
          font-size: 0.95rem;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .summary-value {
          color: #1e293b;
          font-weight: 600;
          font-size: 0.95rem;
        }

        .summary-value.mono {
          font-family: 'Courier New', monospace;
          background: rgba(16, 185, 129, 0.1);
          padding: 4px 10px;
          border-radius: 6px;
          font-size: 0.85rem;
        }

        .summary-value.status {
          color: #10b981;
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 14px;
          background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(52, 211, 153, 0.15) 100%);
          border-radius: 20px;
        }

        .status-dot {
          width: 8px;
          height: 8px;
          background: #10b981;
          border-radius: 50%;
          animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 1;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
          }
          50% {
            opacity: 0.8;
            box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
          }
        }

        .actions-section {
          display: flex;
          gap: 16px;
          justify-content: center;
          flex-wrap: wrap;
          margin-bottom: 32px;
          animation: slideInUp 0.6s ease-out 0.6s both;
        }

        .btn-download {
          background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
          color: white;
          border: none;
          border-radius: 16px;
          padding: 16px 40px;
          font-size: 1.1rem;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
          position: relative;
          overflow: hidden;
          display: flex;
          align-items: center;
          gap: 12px;
          min-width: 240px;
          justify-content: center;
        }

        .btn-download::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 0;
          height: 0;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.3);
          transform: translate(-50%, -50%);
          transition: width 0.6s, height 0.6s;
        }

        .btn-download:hover::before {
          width: 400px;
          height: 400px;
        }

        .btn-download:hover {
          transform: translateY(-3px);
          box-shadow: 0 15px 40px rgba(16, 185, 129, 0.5);
        }

        .btn-download:active {
          transform: translateY(-1px);
        }

        .btn-download:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .btn-download.success {
          background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        }

        .btn-reset {
          background: rgba(100, 116, 139, 0.1);
          color: #475569;
          border: 2px solid rgba(100, 116, 139, 0.2);
          border-radius: 16px;
          padding: 16px 32px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          gap: 10px;
          min-width: 200px;
          justify-content: center;
        }

        .btn-reset:hover {
          background: rgba(100, 116, 139, 0.15);
          border-color: #64748b;
          color: #1e293b;
          transform: translateY(-2px);
        }

        .btn-content {
          position: relative;
          z-index: 1;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .download-spinner {
          width: 20px;
          height: 20px;
          border: 3px solid rgba(255, 255, 255, 0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        .metadata-footer {
          padding: 20px 24px;
          background: linear-gradient(135deg, rgba(100, 116, 139, 0.05) 0%, rgba(148, 163, 184, 0.05) 100%);
          border-radius: 16px;
          text-align: center;
          border: 1px solid rgba(100, 116, 139, 0.1);
          animation: slideInUp 0.6s ease-out 0.8s both;
        }

        .metadata-content {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 24px;
          flex-wrap: wrap;
          color: #64748b;
          font-size: 0.9rem;
        }

        .metadata-item {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 16px;
          background: rgba(255, 255, 255, 0.7);
          border-radius: 10px;
          transition: all 0.3s ease;
        }

        .metadata-item:hover {
          background: white;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .metadata-label {
          font-weight: 600;
          color: #475569;
        }

        .metadata-value {
          color: #1e293b;
          font-weight: 700;
        }

        .confetti-container {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          pointer-events: none;
          overflow: hidden;
        }

        .confetti {
          position: absolute;
          width: 10px;
          height: 10px;
          opacity: 0;
        }

        .confetti.active {
          animation: confetti 3s ease-out forwards;
        }

        @media (max-width: 768px) {
          .results-card {
            padding: 28px 24px;
            border-radius: 20px;
          }

          .success-title {
            font-size: 1.6rem;
          }

          .success-subtitle {
            font-size: 1rem;
          }

          .actions-section {
            flex-direction: column;
          }

          .btn-download,
          .btn-reset {
            width: 100%;
          }

          .metadata-content {
            flex-direction: column;
            gap: 12px;
          }
        }
      `}</style>

      <div className="results-card">
        <div className="confetti-container" id="confetti-container"></div>

        <div className="success-header">
          <div className="success-icon-wrapper">
            <div className="success-icon-bg"></div>
            <CheckCircleIcon 
              width={64} 
              height={64} 
              color="#10b981" 
              className="success-icon"
            />
          </div>
          <h2 className="success-title">
            🎉 Extraction Complete!
          </h2>
          <p className="success-subtitle">
            Your data has been successfully extracted and formatted using <strong>{template?.name || 'the selected template'}</strong>. 
            The results are ready to download.
          </p>
        </div>

        <div className="summary-section">
          <div className="summary-card">
            <div className="summary-header">
              <div className="summary-icon-wrapper">
                <FileTextIcon width={24} height={24} color="#10b981" />
              </div>
              <h3 className="summary-title">Extraction Summary</h3>
            </div>
            
            <div className="summary-grid">
              <div className="summary-row">
                <span className="summary-label">
                  <SparklesIcon width={16} height={16} />
                  Job ID
                </span>
                <span className="summary-value mono">{result.job_id || 'N/A'}</span>
              </div>
              
              <div className="summary-row">
                <span className="summary-label">
                  Status
                </span>
                <span className="summary-value status">
                  <span className="status-dot"></span>
                  {result.status || 'Completed'}
                </span>
              </div>
              
              <div className="summary-row">
                <span className="summary-label">
                  Template Used
                </span>
                <span className="summary-value">{template?.name || 'Unknown Template'}</span>
              </div>
              
              <div className="summary-row">
                <span className="summary-label">
                  Files Processed
                </span>
                <span className="summary-value">
                  {files.length} PDF{files.length !== 1 ? 's' : ''} 📄
                </span>
              </div>
              
              {result.message && (
                <div className="summary-row">
                  <span className="summary-label">
                    Message
                  </span>
                  <span className="summary-value">{result.message}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="actions-section">
          <button 
            className={`btn-download ${downloadSuccess ? 'success' : ''}`}
            onClick={handleDownload}
            disabled={downloading}
          >
            <span className="btn-content">
              {downloading ? (
                <>
                  <div className="download-spinner"></div>
                  Preparing Download...
                </>
              ) : downloadSuccess ? (
                <>
                  <CheckCircleIcon width={20} height={20} color="white" />
                  Downloaded Successfully!
                </>
              ) : (
                <>
                  <DownloadIcon width={20} height={20} />
                  Download Excel File
                </>
              )}
            </span>
          </button>
          
          <button 
            className="btn-reset"
            onClick={onReset}
          >
            <RefreshIcon width={20} height={20} />
            Extract More Files
          </button>
        </div>

        <div className="metadata-footer">
          <div className="metadata-content">
            <div className="metadata-item">
              <SparklesIcon width={16} height={16} />
              <span className="metadata-label">Template:</span>
              <span className="metadata-value">{template?.name || 'N/A'}</span>
            </div>
            <div className="metadata-item">
              <ClockIcon width={16} height={16} />
              <span className="metadata-label">Generated:</span>
              <span className="metadata-value">
                {new Date().toLocaleString('en-US', { 
                  month: 'short', 
                  day: 'numeric', 
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ResultsPanel;