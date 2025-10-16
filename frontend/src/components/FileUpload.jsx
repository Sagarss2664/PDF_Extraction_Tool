// import React, { useCallback, useState, useRef } from 'react'
// import { UploadIcon, FileTextIcon, XIcon } from './icons'

// const FileUpload = ({ files, onFilesSelect }) => {
//   const [dragOver, setDragOver] = useState(false)
//   const fileInputRef = useRef(null)

//   const handleDragOver = useCallback((e) => {
//     e.preventDefault()
//     setDragOver(true)
//   }, [])

//   const handleDragLeave = useCallback((e) => {
//     e.preventDefault()
//     setDragOver(false)
//   }, [])

//   const handleDrop = useCallback((e) => {
//     e.preventDefault()
//     setDragOver(false)
    
//     const droppedFiles = Array.from(e.dataTransfer.files).filter(
//       file => file.type === 'application/pdf'
//     )
    
//     if (droppedFiles.length > 0) {
//       onFilesSelect(droppedFiles)
//     }
//   }, [onFilesSelect])

//   const handleFileSelect = useCallback((e) => {
//     const selectedFiles = Array.from(e.target.files).filter(
//       file => file.type === 'application/pdf'
//     )
    
//     if (selectedFiles.length > 0) {
//       onFilesSelect(selectedFiles)
//     }
    
//     // Reset the input to allow selecting the same file again
//     e.target.value = ''
//   }, [onFilesSelect])

//   const handleBrowseClick = useCallback(() => {
//     fileInputRef.current?.click()
//   }, [])

//   const removeFile = useCallback((indexToRemove) => {
//     const newFiles = files.filter((_, index) => index !== indexToRemove)
//     onFilesSelect(newFiles)
//   }, [files, onFilesSelect])

//   return (
//     <div className="card">
//       <h2 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
//         <UploadIcon width={20} height={20} />
//         Upload PDF Files
//       </h2>
      
//       <div
//         className={`upload-area ${dragOver ? 'drag-over' : ''}`}
//         onDragOver={handleDragOver}
//         onDragLeave={handleDragLeave}
//         onDrop={handleDrop}
//         onClick={handleBrowseClick}
//         style={{ cursor: 'pointer' }}
//       >
//         <UploadIcon width={48} height={48} color="#94a3b8" style={{ marginBottom: '16px' }} />
//         <h3 style={{ marginBottom: '8px', color: '#1e293b' }}>
//           Drag & Drop PDF Files
//         </h3>
//         <p style={{ marginBottom: '16px', color: '#64748b' }}>
//           or click to browse your files
//         </p>
        
//         <input
//           ref={fileInputRef}
//           type="file"
//           multiple
//           accept=".pdf"
//           onChange={handleFileSelect}
//           style={{ display: 'none' }}
//         />
        
//         <button 
//           type="button" 
//           className="btn btn-secondary"
//           onClick={(e) => {
//             e.stopPropagation() // Prevent triggering the div click
//             handleBrowseClick()
//           }}
//         >
//           Browse Files
//         </button>
//       </div>

//       {files.length > 0 && (
//         <div>
//           <h4 style={{ marginBottom: '12px', color: '#374151' }}>
//             Selected Files ({files.length})
//           </h4>
//           <ul className="file-list">
//             {files.map((file, index) => (
//               <li key={index} className="file-item">
//                 <div className="file-info">
//                   <FileTextIcon width={16} height={16} className="file-icon" />
//                   <span style={{ fontSize: '14px' }}>{file.name}</span>
//                   <span style={{ fontSize: '12px', color: '#6b7280' }}>
//                     ({(file.size / 1024 / 1024).toFixed(2)} MB)
//                   </span>
//                 </div>
//                 <button
//                   onClick={() => removeFile(index)}
//                   style={{ 
//                     background: 'none', 
//                     border: 'none', 
//                     cursor: 'pointer',
//                     color: '#6b7280',
//                     padding: '4px',
//                     borderRadius: '4px'
//                   }}
//                   onMouseOver={(e) => e.target.style.color = '#ef4444'}
//                   onMouseOut={(e) => e.target.style.color = '#6b7280'}
//                 >
//                   <XIcon width={16} height={16} />
//                 </button>
//               </li>
//             ))}
//           </ul>
//         </div>
//       )}

//       {files.length === 0 && (
//         <div style={{ 
//           marginTop: '16px', 
//           padding: '12px', 
//           backgroundColor: '#f8fafc', 
//           borderRadius: '8px',
//           textAlign: 'center',
//           color: '#64748b',
//           fontSize: '14px'
//         }}>
//           No files selected. Please upload PDF files to begin extraction.
//         </div>
//       )}
//     </div>
//   )
// }

// export default FileUpload
import React, { useCallback, useState, useRef } from 'react';

// Icons
const UploadIcon = ({ width = 24, height = 24, color = 'currentColor', style = {} }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={style}>
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="17 8 12 3 7 8" />
    <line x1="12" y1="3" x2="12" y2="15" />
  </svg>
);

const FileTextIcon = ({ width = 24, height = 24, className = '' }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <polyline points="14 2 14 8 20 8" />
    <line x1="16" y1="13" x2="8" y2="13" />
    <line x1="16" y1="17" x2="8" y2="17" />
    <line x1="10" y1="9" x2="8" y2="9" />
  </svg>
);

const XIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

const CheckCircleIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
    <polyline points="22 4 12 14.01 9 11.01" />
  </svg>
);

const SparklesIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3l1.912 5.813 6.088.237-4.912 3.663 1.812 5.787L12 15l-4.9 3.5 1.812-5.787L4 9.05l6.088-.237L12 3z" />
  </svg>
);

const FileUpload = ({ files = [], onFilesSelect }) => {
  const [dragOver, setDragOver] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      file => file.type === 'application/pdf'
    );
    
    if (droppedFiles.length > 0) {
      setIsProcessing(true);
      setTimeout(() => {
        onFilesSelect(droppedFiles);
        setIsProcessing(false);
      }, 500);
    }
  }, [onFilesSelect]);

  const handleFileSelect = useCallback((e) => {
    const selectedFiles = Array.from(e.target.files).filter(
      file => file.type === 'application/pdf'
    );
    
    if (selectedFiles.length > 0) {
      setIsProcessing(true);
      setTimeout(() => {
        onFilesSelect(selectedFiles);
        setIsProcessing(false);
      }, 500);
    }
    
    e.target.value = '';
  }, [onFilesSelect]);

  const handleBrowseClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const removeFile = useCallback((indexToRemove) => {
    const newFiles = files.filter((_, index) => index !== indexToRemove);
    onFilesSelect(newFiles);
  }, [files, onFilesSelect]);

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <>
      <style>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }

        @keyframes slideInRight {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
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

        .enhanced-card {
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(20px);
          border-radius: 24px;
          padding: 32px;
          box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          overflow: hidden;
          animation: fadeInUp 0.6s ease-out;
          border: 1px solid rgba(255, 255, 255, 0.5);
        }

        .enhanced-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, #2E3192, #764ba2, #f093fb);
          background-size: 200% 100%;
          animation: shimmer 3s linear infinite;
        }

        .card-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 24px;
          animation: fadeInUp 0.6s ease-out 0.1s both;
        }

        .card-header h2 {
          margin: 0;
          font-size: 1.75rem;
          font-weight: 700;
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .upload-area {
          border: 3px dashed rgba(102, 126, 234, 0.3);
          border-radius: 20px;
          padding: 48px 32px;
          text-align: center;
          cursor: pointer;
          transition: all 0.3s ease;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.03) 0%, rgba(240, 147, 251, 0.03) 100%);
          position: relative;
          overflow: hidden;
          animation: fadeInUp 0.6s ease-out 0.2s both;
        }

        .upload-area::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 0;
          height: 0;
          border-radius: 50%;
          background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
          transform: translate(-50%, -50%);
          transition: width 0.6s ease, height 0.6s ease;
        }

        .upload-area:hover::before {
          width: 400px;
          height: 400px;
        }

        .upload-area:hover {
          border-color: #2E3192;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(240, 147, 251, 0.08) 100%);
          transform: translateY(-4px);
          box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
        }

        .upload-area.drag-over {
          border-color: #2E3192;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%);
          transform: scale(1.02);
          box-shadow: 0 16px 48px rgba(102, 126, 234, 0.25);
        }

        .upload-icon-wrapper {
          display: inline-block;
          animation: bounce 2s ease-in-out infinite;
          margin-bottom: 16px;
          padding: 20px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
          border-radius: 50%;
        }

        .upload-area.drag-over .upload-icon-wrapper {
          animation: pulse 0.5s ease-in-out infinite;
        }

        .upload-title {
          margin: 0 0 8px 0;
          color: #1e293b;
          font-size: 1.5rem;
          font-weight: 700;
        }

        .upload-subtitle {
          margin: 0 0 24px 0;
          color: #64748b;
          font-size: 1rem;
        }

        .btn-browse {
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 12px;
          padding: 14px 32px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
          position: relative;
          overflow: hidden;
        }

        .btn-browse::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 0;
          height: 0;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.3);
          transform: translate(-50%, -50%);
          transition: width 0.5s, height 0.5s;
        }

        .btn-browse:hover::before {
          width: 300px;
          height: 300px;
        }

        .btn-browse:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 28px rgba(102, 126, 234, 0.4);
        }

        .btn-browse:active {
          transform: translateY(0);
        }

        .files-section {
          margin-top: 32px;
          animation: fadeInUp 0.6s ease-out 0.3s both;
        }

        .files-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 16px;
          padding: 12px 16px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
          border-radius: 12px;
        }

        .files-header h4 {
          margin: 0;
          color: #374151;
          font-size: 1.1rem;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .file-count-badge {
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          color: white;
          padding: 4px 12px;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 700;
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .file-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .file-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 16px 20px;
          background: white;
          border: 2px solid rgba(102, 126, 234, 0.15);
          border-radius: 16px;
          transition: all 0.3s ease;
          animation: slideInRight 0.4s ease-out backwards;
          position: relative;
          overflow: hidden;
        }

        .file-item::before {
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
          width: 4px;
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          transform: scaleY(0);
          transition: transform 0.3s ease;
        }

        .file-item:hover::before {
          transform: scaleY(1);
        }

        .file-item:hover {
          border-color: #2E3192;
          background: rgba(102, 126, 234, 0.05);
          transform: translateX(4px);
          box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        }

        .file-info {
          display: flex;
          align-items: center;
          gap: 12px;
          flex: 1;
        }

        .file-icon-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%);
          border-radius: 10px;
          color: #2E3192;
        }

        .file-details {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .file-name {
          font-size: 0.95rem;
          font-weight: 600;
          color: #1e293b;
          word-break: break-word;
        }

        .file-size {
          font-size: 0.85rem;
          color: #6b7280;
          font-weight: 500;
        }

        .btn-remove {
          background: rgba(239, 68, 68, 0.1);
          border: none;
          cursor: pointer;
          color: #ef4444;
          padding: 8px;
          border-radius: 8px;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .btn-remove:hover {
          background: #ef4444;
          color: white;
          transform: rotate(90deg) scale(1.1);
        }

        .empty-state {
          margin-top: 24px;
          padding: 32px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(240, 147, 251, 0.05) 100%);
          border-radius: 16px;
          text-align: center;
          border: 2px dashed rgba(102, 126, 234, 0.2);
          animation: fadeInUp 0.6s ease-out 0.3s both;
        }

        .empty-state-icon {
          margin-bottom: 12px;
          opacity: 0.5;
        }

        .empty-state-text {
          color: #64748b;
          font-size: 0.95rem;
          line-height: 1.6;
        }

        .processing-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.95);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          z-index: 10;
          backdrop-filter: blur(10px);
        }

        .spinner {
          width: 50px;
          height: 50px;
          border: 4px solid rgba(102, 126, 234, 0.2);
          border-top-color: #2E3192;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
          margin-bottom: 16px;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .processing-text {
          color: #2E3192;
          font-weight: 600;
          font-size: 1.1rem;
        }

        @media (max-width: 768px) {
          .enhanced-card {
            padding: 24px;
            border-radius: 20px;
          }

          .upload-area {
            padding: 32px 20px;
          }

          .card-header h2 {
            font-size: 1.5rem;
          }

          .file-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
          }

          .btn-remove {
            align-self: flex-end;
          }
        }
      `}</style>

      <div className="enhanced-card">
        {isProcessing && (
          <div className="processing-overlay">
            <div className="spinner"></div>
            <div className="processing-text">Processing files...</div>
          </div>
        )}

        <div className="card-header">
          <UploadIcon width={28} height={28} color="#2E3192" />
          <h2>Upload PDF Files</h2>
        </div>
        
        <div
          className={`upload-area ${dragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
        >
          <div className="upload-icon-wrapper">
            <UploadIcon width={48} height={48} color="#2E3192" />
          </div>
          <h3 className="upload-title">
            {dragOver ? '🎉 Drop your files here!' : '📄 Drag & Drop PDF Files'}
          </h3>
          <p className="upload-subtitle">
            or click the button below to browse
          </p>
          
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          
          <button 
            type="button" 
            className="btn-browse"
            onClick={(e) => {
              e.stopPropagation();
              handleBrowseClick();
            }}
          >
            <span style={{ position: 'relative', zIndex: 1 }}>
              Browse Files
            </span>
          </button>
        </div>

        {files.length > 0 && (
          <div className="files-section">
            <div className="files-header">
              <h4>
                <CheckCircleIcon width={20} height={20} />
                Selected Files
              </h4>
              <span className="file-count-badge">{files.length}</span>
            </div>
            <ul className="file-list">
              {files.map((file, index) => (
                <li 
                  key={index} 
                  className="file-item"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="file-info">
                    <div className="file-icon-wrapper">
                      <FileTextIcon width={20} height={20} />
                    </div>
                    <div className="file-details">
                      <div className="file-name">{file.name}</div>
                      <div className="file-size">{formatFileSize(file.size)}</div>
                    </div>
                  </div>
                  <button
                    className="btn-remove"
                    onClick={() => removeFile(index)}
                    title="Remove file"
                  >
                    <XIcon width={18} height={18} />
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {files.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">
              <SparklesIcon width={48} height={48} color="#94a3b8" />
            </div>
            <div className="empty-state-text">
              <strong>No files selected yet</strong>
              <br />
              Upload your PDF files to get started with extraction
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default FileUpload;