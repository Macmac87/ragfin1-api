import React from 'react';

const Actions = ({ onRefresh, loading }) => {
  const handleExportPDF = () => {
    alert('PDF export would be generated here');
  };

  const handleExportExcel = () => {
    alert('Excel export would be generated here');
  };

  return (
    <div style={styles.actions}>
      <button style={{...styles.btn, ...styles.btnPrimary}} onClick={handleExportPDF}>
        <span>📄</span>
        <span>Export Full Report (PDF)</span>
      </button>
      
      <button style={{...styles.btn, ...styles.btnSecondary}} onClick={handleExportExcel}>
        <span>📊</span>
        <span>Download Data (Excel)</span>
      </button>
      
      <button 
        style={{...styles.btn, ...styles.btnSecondary}} 
        onClick={onRefresh}
        disabled={loading}
      >
        <span>🔄</span>
        <span>{loading ? 'Refreshing...' : 'Refresh Data'}</span>
      </button>
    </div>
  );
};

const styles = {
  actions: {
    display: 'flex',
    gap: '16px',
    justifyContent: 'center',
    marginBottom: '48px'
  },
  btn: {
    padding: '16px 32px',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  btnPrimary: {
    background: 'linear-gradient(135deg, #00ff88 0%, #00cc6a 100%)',
    color: '#000'
  },
  btnSecondary: {
    background: '#1a1a1a',
    color: '#fff',
    border: '1px solid #333'
  }
};

export default Actions;