// import axios from 'axios'

// const API_BASE_URL = 'http://localhost:8000'

// const api = axios.create({
//   baseURL: API_BASE_URL,
//   timeout: 300000, // 5 minutes timeout for large files
// })

// export const extractService = {
//   async extractData(files, templateId) {
//     const formData = new FormData()
    
//     files.forEach(file => {
//       formData.append('files', file)
//     })
//     formData.append('template_id', templateId.toString())

//     const response = await api.post('/extract', formData, {
//       headers: {
//         'Content-Type': 'multipart/form-data',
//       },
//       onUploadProgress: (progressEvent) => {
//         // Progress handling can be implemented here
//       },
//     })

//     return response
//   },

//   async downloadFile(jobId) {
//     const response = await api.get(`/download/${jobId}`, {
//       responseType: 'blob',
//     })
//     return response
//   },

//   async getTemplates() {
//     const response = await api.get('/templates')
//     return response.data
//   },
// }

// export default api
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for large files
})

export const extractService = {
  async extractData(files, templateId) {
    const formData = new FormData()
    
    files.forEach(file => {
      formData.append('files', file)
    })
    formData.append('template_id', templateId.toString())

    console.log('🔄 Sending request to /api/extract with template_id:', templateId)

    const response = await api.post('/api/extract', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response
  },

  async downloadFile(jobId) {
    const response = await api.get(`/api/download/${jobId}`, {
      responseType: 'blob',
    })
    return response
  },

  async getTemplates() {
    const response = await api.get('/api/templates')
    return response.data
  },
}

export default api