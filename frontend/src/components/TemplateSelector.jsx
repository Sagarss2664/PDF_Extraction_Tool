// import React, { useState, useEffect } from 'react'
// import { SettingsIcon, CheckIcon } from './icons'
// import { extractService } from '../services/api'

// const TemplateSelector = ({ selectedTemplate, onTemplateSelect }) => {
//   const [templates, setTemplates] = useState([])
//   const [loading, setLoading] = useState(true)

//   useEffect(() => {
//     const fetchTemplates = async () => {
//       try {
//         const data = await extractService.getTemplates()
//         setTemplates(data.templates)
//         console.log('Loaded templates:', data.templates)
//       } catch (error) {
//         console.error('Failed to fetch templates:', error)
//         // Fallback templates
//         setTemplates([
//           { 
//             id: 1, 
//             name: 'Private Equity Fund Detailed Template', 
//             description: 'Comprehensive fund and investment data extraction including fund details, manager information, financial positions, and portfolio companies',
//             features: ['Fund Details', 'Manager Info', 'Financial Positions', 'Portfolio Companies', 'Investment History']
//           },
//           { 
//             id: 2, 
//             name: 'Portfolio Summary Template', 
//             description: 'Executive portfolio summary with investment schedules, financial statements, and company profiles',
//             features: ['Executive Summary', 'Investment Schedule', 'Financial Statements', 'Company Profiles', 'Footnotes']
//           }
//         ])
//       } finally {
//         setLoading(false)
//       }
//     }

//     fetchTemplates()
//   }, [])

//   if (loading) {
//     return (
//       <div className="card">
//         <div style={{ display: 'flex', alignItems: 'center', gap: '12px', justifyContent: 'center' }}>
//           <div className="loading-spinner"></div>
//           <span style={{ color: '#64748b' }}>Loading templates...</span>
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className="card">
//       <h2 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
//         <SettingsIcon width={20} height={20} />
//         Select Extraction Template
//       </h2>
      
//       <p style={{ marginBottom: '20px', color: '#64748b', fontSize: '14px' }}>
//         Choose the template that matches your document type for optimal extraction results
//       </p>
      
//       <div style={{ display: 'grid', gap: '16px' }}>
//         {templates.map(template => (
//           <div
//             key={template.id}
//             className={`template-card ${selectedTemplate?.id === template.id ? 'selected' : ''}`}
//             onClick={() => {
//               console.log('Selected template:', template)
//               onTemplateSelect(template)
//             }}
//             style={{ 
//               cursor: 'pointer',
//               border: selectedTemplate?.id === template.id ? '2px solid #3b82f6' : '2px solid #e2e8f0',
//               backgroundColor: selectedTemplate?.id === template.id ? '#f0f9ff' : '#ffffff',
//               padding: '16px',
//               borderRadius: '8px',
//               transition: 'all 0.2s ease'
//             }}
//           >
//             <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
//               <div style={{ 
//                 width: '20px', 
//                 height: '20px', 
//                 border: '2px solid #cbd5e1', 
//                 borderRadius: '4px',
//                 display: 'flex',
//                 alignItems: 'center',
//                 justifyContent: 'center',
//                 flexShrink: 0,
//                 marginTop: '2px',
//                 backgroundColor: selectedTemplate?.id === template.id ? '#3b82f6' : 'transparent',
//                 borderColor: selectedTemplate?.id === template.id ? '#3b82f6' : '#cbd5e1'
//               }}>
//                 {selectedTemplate?.id === template.id && (
//                   <CheckIcon width={14} height={14} color="white" />
//                 )}
//               </div>
              
//               <div style={{ flex: 1 }}>
//                 <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
//                   <h3 style={{ 
//                     margin: 0, 
//                     color: selectedTemplate?.id === template.id ? '#1e40af' : '#1e293b',
//                     fontSize: '16px',
//                     fontWeight: '600'
//                   }}>
//                     {template.name}
//                   </h3>
//                   <span style={{ 
//                     fontSize: '12px', 
//                     padding: '2px 8px', 
//                     backgroundColor: selectedTemplate?.id === template.id ? '#dbeafe' : '#f1f5f9',
//                     color: selectedTemplate?.id === template.id ? '#1e40af' : '#64748b',
//                     borderRadius: '12px',
//                     fontWeight: '500'
//                   }}>
//                     Template {template.id}
//                   </span>
//                 </div>
                
//                 <p style={{ 
//                   marginBottom: '12px', 
//                   color: '#64748b', 
//                   fontSize: '14px',
//                   lineHeight: '1.5'
//                 }}>
//                   {template.description}
//                 </p>
                
//                 {template.features && (
//                   <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
//                     {template.features.map((feature, index) => (
//                       <span 
//                         key={index}
//                         style={{
//                           fontSize: '12px',
//                           padding: '4px 8px',
//                           backgroundColor: '#f8fafc',
//                           color: '#475569',
//                           borderRadius: '6px',
//                           border: '1px solid #e2e8f0'
//                         }}
//                       >
//                         {feature}
//                       </span>
//                     ))}
//                   </div>
//                 )}
//               </div>
//             </div>
//           </div>
//         ))}
//       </div>

//       {selectedTemplate && (
//         <div style={{ 
//           marginTop: '16px',
//           padding: '12px',
//           backgroundColor: '#f0f9ff',
//           border: '1px solid #bae6fd',
//           borderRadius: '8px',
//           fontSize: '14px',
//           color: '#0369a1'
//         }}>
//           <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
//             <strong>Selected:</strong> {selectedTemplate.name}
//           </div>
//         </div>
//       )}
//     </div>
//   )
// }

// export default TemplateSelector
import React, { useState, useEffect } from 'react';

// Icons
const SettingsIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="3" />
    <path d="M12 1v6m0 6v6m0-18a9 9 0 0 1 9 9h-6m6 0a9 9 0 0 1-9 9v-6m0 6a9 9 0 0 1-9-9h6m-6 0a9 9 0 0 1 9-9v6" />
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
  </svg>
);

const CheckIcon = ({ width = 24, height = 24, color = 'currentColor' }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const LayersIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 2 7 12 12 22 7 12 2" />
    <polyline points="2 17 12 22 22 17" />
    <polyline points="2 12 12 17 22 12" />
  </svg>
);

const ZapIcon = ({ width = 24, height = 24 }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
  </svg>
);

const TemplateSelector = ({ selectedTemplate, onTemplateSelect }) => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hoveredTemplate, setHoveredTemplate] = useState(null);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        // Simulating API call - replace with actual API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Fallback templates with more details
        setTemplates([
          { 
            id: 1, 
            name: 'Private Equity Fund Detailed Template', 
            description: 'Comprehensive fund and investment data extraction including fund details, manager information, financial positions, and portfolio companies',
            features: ['Fund Details', 'Manager Info', 'Financial Positions', 'Portfolio Companies', 'Investment History'],
            icon: '💼',
            color: '#2E3192'
          },
          { 
            id: 2, 
            name: 'Portfolio Summary Template', 
            description: 'Executive portfolio summary with investment schedules, financial statements, and company profiles',
            features: ['Executive Summary', 'Investment Schedule', 'Financial Statements', 'Company Profiles', 'Footnotes'],
            icon: '📊',
            color: '#f093fb'
          }
        ]);
      } catch (error) {
        console.error('Failed to fetch templates:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  if (loading) {
    return (
      <>
        <style>{`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
          
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }

          .loading-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 48px 32px;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 20px;
            border: 1px solid rgba(255, 255, 255, 0.5);
          }

          .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top-color: #2E3192;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
          }

          .loading-text {
            color: #64748b;
            font-size: 1.1rem;
            font-weight: 500;
            animation: pulse 2s ease-in-out infinite;
          }
        `}</style>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <span className="loading-text">Loading templates...</span>
        </div>
      </>
    );
  }

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

        @keyframes slideInLeft {
          from {
            opacity: 0;
            transform: translateX(-30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes scaleIn {
          from {
            opacity: 0;
            transform: scale(0.95);
          }
          to {
            opacity: 1;
            transform: scale(1);
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

        @keyframes float {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }

        @keyframes checkmark {
          0% {
            transform: scale(0) rotate(-45deg);
            opacity: 0;
          }
          50% {
            transform: scale(1.2) rotate(-45deg);
          }
          100% {
            transform: scale(1) rotate(0deg);
            opacity: 1;
          }
        }

        .template-selector-card {
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(20px);
          border-radius: 24px;
          padding: 32px;
          box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
          position: relative;
          overflow: hidden;
          animation: fadeInUp 0.6s ease-out;
          border: 1px solid rgba(255, 255, 255, 0.5);
        }

        .template-selector-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, #2E3192, #764ba2, #f093fb, #4fd1c5);
          background-size: 300% 100%;
          animation: shimmer 3s linear infinite;
        }

        .selector-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
          animation: fadeInUp 0.6s ease-out 0.1s both;
        }

        .selector-header h2 {
          margin: 0;
          font-size: 1.75rem;
          font-weight: 700;
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .settings-icon-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%);
          border-radius: 12px;
          color: #2E3192;
          animation: float 3s ease-in-out infinite;
        }

        .selector-description {
          margin-bottom: 28px;
          color: #64748b;
          font-size: 1rem;
          line-height: 1.6;
          animation: fadeInUp 0.6s ease-out 0.2s both;
        }

        .templates-grid {
          display: grid;
          gap: 20px;
          animation: fadeInUp 0.6s ease-out 0.3s both;
        }

        .template-card {
          cursor: pointer;
          padding: 24px;
          border-radius: 20px;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          overflow: hidden;
          background: white;
          border: 2px solid rgba(102, 126, 234, 0.15);
          animation: slideInLeft 0.5s ease-out backwards;
        }

        .template-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(240, 147, 251, 0.05) 100%);
          opacity: 0;
          transition: opacity 0.3s ease;
        }

        .template-card:hover::before {
          opacity: 1;
        }

        .template-card:hover {
          transform: translateY(-8px) scale(1.02);
          box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
          border-color: #2E3192;
        }

        .template-card.selected {
          border-color: #2E3192;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(240, 147, 251, 0.08) 100%);
          box-shadow: 0 12px 32px rgba(102, 126, 234, 0.3);
          transform: scale(1.02);
        }

        .template-card.selected::after {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          bottom: 0;
          width: 5px;
          background: linear-gradient(180deg, #2E3192 0%, #764ba2 100%);
        }

        .template-card-content {
          display: flex;
          align-items: flex-start;
          gap: 20px;
          position: relative;
          z-index: 1;
        }

        .template-icon-section {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
        }

        .template-emoji {
          font-size: 3rem;
          transition: transform 0.3s ease;
        }

        .template-card:hover .template-emoji {
          transform: scale(1.2) rotate(5deg);
        }

        .checkbox-wrapper {
          width: 28px;
          height: 28px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
          border: 3px solid #cbd5e1;
          background: white;
        }

        .template-card.selected .checkbox-wrapper {
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          border-color: #2E3192;
          animation: checkmark 0.5s ease;
        }

        .template-info {
          flex: 1;
        }

        .template-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 8px;
          flex-wrap: wrap;
        }

        .template-name {
          margin: 0;
          font-size: 1.2rem;
          font-weight: 700;
          color: #1e293b;
          transition: color 0.3s ease;
        }

        .template-card.selected .template-name {
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .template-badge {
          font-size: 0.75rem;
          padding: 4px 10px;
          border-radius: 16px;
          font-weight: 600;
          transition: all 0.3s ease;
          background: rgba(102, 126, 234, 0.1);
          color: #2E3192;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .template-card.selected .template-badge {
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          color: white;
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .template-description {
          margin-bottom: 16px;
          color: #64748b;
          font-size: 0.95rem;
          line-height: 1.6;
        }

        .features-container {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .feature-tag {
          font-size: 0.8rem;
          padding: 6px 12px;
          background: rgba(248, 250, 252, 0.8);
          color: #475569;
          border-radius: 10px;
          border: 1px solid rgba(226, 232, 240, 0.8);
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }

        .template-card:hover .feature-tag {
          background: rgba(102, 126, 234, 0.1);
          border-color: rgba(102, 126, 234, 0.3);
          color: #2E3192;
          transform: translateY(-2px);
        }

        .template-card.selected .feature-tag {
          background: rgba(102, 126, 234, 0.15);
          border-color: rgba(102, 126, 234, 0.4);
          color: #2E3192;
          font-weight: 600;
        }

        .selection-banner {
          margin-top: 24px;
          padding: 20px 24px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
          border: 2px solid rgba(102, 126, 234, 0.3);
          border-radius: 16px;
          animation: scaleIn 0.4s ease-out;
          position: relative;
          overflow: hidden;
        }

        .selection-banner::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
          animation: shimmer 2s infinite;
        }

        .selection-content {
          display: flex;
          align-items: center;
          gap: 12px;
          position: relative;
          z-index: 1;
        }

        .success-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          background: linear-gradient(135deg, #2E3192 0%, #764ba2 100%);
          border-radius: 50%;
          color: white;
          animation: checkmark 0.5s ease;
        }

        .selection-text {
          color: #2E3192;
          font-weight: 600;
          font-size: 1rem;
        }

        .selection-name {
          color: #1e293b;
          font-weight: 700;
        }

        @media (max-width: 768px) {
          .template-selector-card {
            padding: 24px;
            border-radius: 20px;
          }

          .selector-header h2 {
            font-size: 1.5rem;
          }

          .template-card-content {
            flex-direction: column;
            gap: 16px;
          }

          .template-icon-section {
            flex-direction: row;
            width: 100%;
            justify-content: space-between;
          }

          .template-emoji {
            font-size: 2.5rem;
          }
        }
      `}</style>

      <div className="template-selector-card">
        <div className="selector-header">
          <div className="settings-icon-wrapper">
            <LayersIcon width={24} height={24} />
          </div>
          <h2>Select Extraction Template</h2>
        </div>
        
        <p className="selector-description">
          Choose the perfect template that matches your document type for optimal and accurate extraction results
        </p>
        
        <div className="templates-grid">
          {templates.map((template, index) => (
            <div
              key={template.id}
              className={`template-card ${selectedTemplate?.id === template.id ? 'selected' : ''}`}
              onClick={() => {
                console.log('Selected template:', template);
                onTemplateSelect(template);
              }}
              onMouseEnter={() => setHoveredTemplate(template.id)}
              onMouseLeave={() => setHoveredTemplate(null)}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="template-card-content">
                <div className="template-icon-section">
                  <div className="template-emoji">
                    {template.icon}
                  </div>
                  <div className="checkbox-wrapper">
                    {selectedTemplate?.id === template.id && (
                      <CheckIcon width={16} height={16} color="white" />
                    )}
                  </div>
                </div>
                
                <div className="template-info">
                  <div className="template-header">
                    <h3 className="template-name">
                      {template.name}
                    </h3>
                    <span className="template-badge">
                      <ZapIcon width={12} height={12} />
                      Template {template.id}
                    </span>
                  </div>
                  
                  <p className="template-description">
                    {template.description}
                  </p>
                  
                  {template.features && (
                    <div className="features-container">
                      {template.features.map((feature, idx) => (
                        <span 
                          key={idx}
                          className="feature-tag"
                          style={{ animationDelay: `${idx * 0.05}s` }}
                        >
                          {feature}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {selectedTemplate && (
          <div className="selection-banner">
            <div className="selection-content">
              <div className="success-icon">
                <CheckIcon width={18} height={18} color="white" />
              </div>
              <div>
                <span className="selection-text">Selected: </span>
                <span className="selection-name">{selectedTemplate.name}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default TemplateSelector;