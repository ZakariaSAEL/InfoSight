import { useState, useRef } from 'react';
import { UploadCloud, FileImage } from 'lucide-react';
import Loader from '../components/Loader';
import ResultCard from '../components/ResultCard';
import { saveInvoice } from '../db';
import axios from 'axios';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResult(null);
      setError(null);
      
      // Create preview for images
      if (selectedFile.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onloadend = () => setPreview(reader.result);
        reader.readAsDataURL(selectedFile);
      } else {
        setPreview(null); // Reset for PDFs
      }
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    
    setIsProcessing(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/analyze", formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      const data = response.data;
      if (data.status === 'error') throw new Error(data.message);
      
      // The backend returns the expected IndexedDB schema payload
      setResult(data);
      
      // Automatically save to IndexedDB
      await saveInvoice(data);
      
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || err.message || "An error occurred during verification.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Extract Invoice Data</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>
          Powered by Gemini 3 AI & Moroccan Address Normalization
        </p>
      </div>

      <div 
        className="card"
        style={{ 
          maxWidth: '800px', 
          margin: '0 auto', 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center',
          borderStyle: 'dashed',
          borderWidth: '2px',
          padding: '3rem 2rem'
        }}
        onClick={() => !isProcessing && fileInputRef.current?.click()}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          style={{ display: 'none' }} 
          accept="image/*,application/pdf"
        />
        
        {preview ? (
          <img src={preview} alt="Preview" style={{ maxHeight: '300px', maxWidth: '100%', borderRadius: '8px', marginBottom: '1.5rem', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }} />
        ) : file ? (
          <FileImage size={64} color="var(--primary)" style={{ marginBottom: '1rem' }} />
        ) : (
          <UploadCloud size={64} color="var(--text-muted)" style={{ marginBottom: '1rem' }} />
        )}
        
        <h3 style={{ marginBottom: '0.5rem' }}>{file ? file.name : "Click or drag file to upload"}</h3>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>Supports JPG, PNG, and PDF.</p>
        
        <button 
          className="btn-primary" 
          onClick={(e) => {
            e.stopPropagation();
            if (file) handleAnalyze();
            else fileInputRef.current?.click();
          }}
          disabled={isProcessing}
          style={{ width: '100%', maxWidth: '300px', display: 'flex', justifyContent: 'center', gap: '0.5rem', opacity: isProcessing ? 0.7 : 1 }}
        >
          {isProcessing ? 'Processing...' : (file ? 'Analyze Document' : 'Select File')}
        </button>
      </div>

      {error && (
        <div style={{ maxWidth: '800px', margin: '2rem auto', padding: '1rem', backgroundColor: '#FEE2E2', color: 'var(--error)', borderRadius: '8px', border: '1px solid #FCA5A5' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {isProcessing && <Loader />}
      
      {result && <ResultCard data={result} />}
    </div>
  );
}
