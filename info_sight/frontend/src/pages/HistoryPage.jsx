import { useState, useEffect } from 'react';
import { DownloadCloud, Trash2, Search, Lock } from 'lucide-react';
import { getAllInvoices, deleteInvoice, clearAllInvoices } from '../db';
import ResultCard from '../components/ResultCard';
import LoginModal from '../components/LoginModal';

export default function HistoryPage() {
  const [invoices, setInvoices] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedId, setExpandedId] = useState(null);
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
    loadInvoices();
  }, []);

  const loadInvoices = async () => {
    const data = await getAllInvoices();
    setInvoices(data.reverse()); // Newest first
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    await deleteInvoice(id);
    loadInvoices();
  };

  const handleClearAll = async () => {
    if (window.confirm("Are you sure you want to clear all history? This cannot be undone.")) {
      await clearAllInvoices();
      loadInvoices();
    }
  };

  const handleExport = (type) => {
    // Export Limit Logic hook
    const exportCount = parseInt(localStorage.getItem('exportCount') || '0', 10);
    
    // Check if user is logged in (mocked)
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

    if (!isLoggedIn && exportCount >= 2) {
      setShowLoginModal(true);
      return;
    }

    if (!isLoggedIn) {
      localStorage.setItem('exportCount', String(exportCount + 1));
    }

    // Perform the actual export
    if (type === 'csv') exportCSV();
    if (type === 'json') exportJSON();
  };

  const exportCSV = () => {
    const headers = ["Invoice Number", "Date", "Total", "Vendor", "Address"];
    const csvRows = [headers.join(",")];
    
    invoices.forEach(inv => {
      // Escape commas in address and vendor
      const cleanVendor = `"${(inv.vendor || '').replace(/"/g, '""')}"`;
      const cleanAddress = `"${(inv.address || '').replace(/"/g, '""')}"`;
      csvRows.push([inv.invoice_number, inv.date, inv.total, cleanVendor, cleanAddress].join(","));
    });
    
    downloadBlob(csvRows.join("\n"), "InfoSight_History.csv", "text/csv");
  };

  const exportJSON = () => {
    const jsonStr = JSON.stringify(invoices, null, 2);
    downloadBlob(jsonStr, "InfoSight_History.json", "application/json");
  };

  const downloadBlob = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
  };

  const filteredInvoices = invoices.filter(inv => 
    (inv.vendor || "").toLowerCase().includes(searchTerm.toLowerCase()) || 
    (inv.invoice_number || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem' }}>Extraction History</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn-secondary" onClick={() => handleExport('csv')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <DownloadCloud size={18} /> Export CSV
          </button>
          <button className="btn-secondary" onClick={() => handleExport('json')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <DownloadCloud size={18} /> Export JSON
          </button>
          {invoices.length > 0 && (
            <button className="btn-secondary" onClick={handleClearAll} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--error)', borderColor: 'var(--border)' }}>
              <Trash2 size={18} /> Clear Data
            </button>
          )}
        </div>
      </div>

      <div style={{ position: 'relative', marginBottom: '2rem' }}>
        <Search size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
        <input 
          type="text" 
          placeholder="Search by vendor or invoice number..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '1rem 1rem 1rem 3rem',
            borderRadius: '8px',
            border: '1px solid var(--border)',
            backgroundColor: 'var(--surface)',
            color: 'var(--text)',
            fontSize: '1rem',
            fontFamily: 'inherit'
          }}
        />
      </div>

      {invoices.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>No invoices processed yet. Head over to the Upload page to get started!</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredInvoices.map(inv => (
            <div key={inv.id}>
              <div 
                className="card" 
                style={{ 
                  display: 'grid', 
                  gridTemplateColumns: '2fr 1.5fr 1fr 1.5fr auto', 
                  alignItems: 'center', 
                  gap: '1rem',
                  cursor: 'pointer',
                  padding: '1rem 1.5rem',
                  backgroundColor: expandedId === inv.id ? 'var(--background)' : 'var(--surface)',
                }}
                onClick={() => setExpandedId(expandedId === inv.id ? null : inv.id)}
              >
                <div>
                  <h4 style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.85rem' }}>VENDOR</h4>
                  <p style={{ margin: 0, fontWeight: '600' }}>{inv.vendor || 'Unknown'}</p>
                </div>
                <div>
                  <h4 style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.85rem' }}>INVOICE #</h4>
                  <p style={{ margin: 0 }}>{inv.invoice_number}</p>
                </div>
                <div>
                  <h4 style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.85rem' }}>DATE</h4>
                  <p style={{ margin: 0 }}>{inv.date}</p>
                </div>
                <div>
                  <h4 style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.85rem' }}>TOTAL</h4>
                  <p style={{ margin: 0, fontWeight: 'bold', color: 'var(--primary)' }}>{inv.total}</p>
                </div>
                <button 
                  onClick={(e) => handleDelete(inv.id, e)} 
                  style={{ color: 'var(--text-muted)', padding: '0.5rem' }} 
                  title="Delete record"
                >
                  <Trash2 size={20} />
                </button>
              </div>
              
              {expandedId === inv.id && (
                <div style={{ marginTop: '-0.5rem', marginBottom: '1rem' }}>
                  <ResultCard data={inv} />
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {showLoginModal && <LoginModal onClose={() => setShowLoginModal(false)} />}
    </div>
  );
}
