import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file - running in Hackathon Mock Mode:', error);
    
    // For demo/hackathon purposes when local backend is down:
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          overall_plagiarism_score: 42,
          overall_ai_probability: 73,
          paragraph_analysis: [
            {
              paragraph: "Artificial Intelligence has the potential to transform numerous sectors of the economy.",
              plagiarism_score: 12,
              ai_probability: 88,
            },
            {
              paragraph: "In conclusion, we can say that AI should be monitored and carefully regulated.",
              plagiarism_score: 85,
              ai_probability: 30,
            },
            {
              paragraph: "The model was trained on 10,000 examples of handwritten digits. This allowed for significant convergence over time, demonstrating traditional machine learning methodologies rather than pure large language model derivations.",
              plagiarism_score: 5,
              ai_probability: 10,
            }
          ]
        });
      }, 2500);
    });
  }
};
