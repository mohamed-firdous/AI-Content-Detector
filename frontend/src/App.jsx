import React, { useState } from 'react';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('upload'); // 'upload' | 'results'
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    setCurrentPage('results');
  };

  const resetFlow = () => {
    setAnalysisResult(null);
    setCurrentPage('upload');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center pt-16 pb-20 px-4 font-sans text-slate-900">
      <div className="w-full max-w-5xl">
        <header className="mb-12 text-center flex flex-col items-center">
          <div className="bg-indigo-100 text-indigo-700 font-semibold px-4 py-1.5 rounded-full text-xs mb-4 tracking-wide">
            24-HOUR HACKATHON
          </div>
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-indigo-700 via-indigo-500 to-purple-600 tracking-tight">
            AI Assignment Detector
          </h1>
          <p className="text-slate-500 mt-4 text-lg max-w-xl">
            Upload your document natively to inspect plagiarism levels and AI synthesis probability down to paragraph fidelity.
          </p>
        </header>

        <main className="w-full">
          {currentPage === 'upload' && (
            <UploadPage onAnalysisComplete={handleAnalysisComplete} />
          )}

          {currentPage === 'results' && analysisResult && (
            <ResultsPage result={analysisResult} onReset={resetFlow} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
