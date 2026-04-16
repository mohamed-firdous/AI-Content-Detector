import React, { useCallback, useRef, useState } from 'react';
import { UploadCloud, File, X } from 'lucide-react';

const FileUpload = ({ onFileSelect, selectedFile, onClear }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];
    const extension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (validTypes.includes(file.type) || validExtensions.includes(extension)) {
      onFileSelect(file);
    } else {
      alert("Please upload a .pdf or .docx file");
    }
  };

  return (
    <div className="w-full">
      {!selectedFile ? (
        <div 
          onClick={() => fileInputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-3 border-dashed rounded-[2.5rem] p-12 text-center cursor-pointer transition-all duration-300 flex flex-col items-center justify-center ${
            isDragging 
              ? 'border-indigo-500 bg-indigo-50/50 scale-[1.02]' 
              : 'border-slate-200 hover:border-indigo-400 hover:bg-slate-50 bg-white hover:shadow-xl hover:shadow-indigo-900/5'
          }`}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            accept=".pdf,.docx" 
            onChange={handleFileChange} 
          />
          <div className={`p-5 rounded-3xl mb-6 transition-colors ${isDragging ? 'bg-indigo-100' : 'bg-slate-100'}`}>
            <UploadCloud className={`w-12 h-12 ${isDragging ? 'text-indigo-600' : 'text-slate-400'}`} />
          </div>
          <h3 className="text-2xl font-bold mb-3 text-slate-800">Drag & Drop your file here</h3>
          <p className="text-slate-500 mb-8 font-medium text-lg">or click to browse from your computer</p>
          <div className="flex gap-3 text-xs font-bold text-slate-500 uppercase tracking-widest">
            <span className="bg-slate-100 px-4 py-2 rounded-lg">.PDF</span>
            <span className="bg-slate-100 px-4 py-2 rounded-lg">.DOCX</span>
          </div>
        </div>
      ) : (
        <div className="bg-white border border-slate-200 p-6 rounded-[2rem] shadow-sm flex items-center justify-between group hover:shadow-md transition-shadow">
          <div className="flex items-center space-x-5 overflow-hidden">
            <div className="bg-gradient-to-br from-indigo-100 to-purple-100 p-4 rounded-2xl text-indigo-600 flex-shrink-0">
               <File className="w-8 h-8" />
            </div>
            <div className="truncate">
              <p className="font-bold text-slate-800 text-lg truncate">{selectedFile.name}</p>
              <p className="text-slate-500 text-sm font-medium mt-1">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
          <button 
            onClick={onClear}
            className="p-3 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors flex-shrink-0"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
