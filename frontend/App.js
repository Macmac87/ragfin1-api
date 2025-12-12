import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatsGrid from './components/StatsGrid';
import ChartSection from './components/ChartSection';
import DataTable from './components/DataTable';
import AIInsights from './components/AIInsights';
import Actions from './components/Actions';
import { getCompetitiveInsight } from './services/api';
import { DEFAULT_CORRIDOR } from './config';

function App() {
  const [corridor, setCorridor] = useState(DEFAULT_CORRIDOR);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState('');

  const fetchData = async (dest) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await getCompetitiveInsight(dest);
      setData(result);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      setError(err.message);
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(corridor);
  }, [corridor]);

  const handleCorridorChange = (newCorridor) => {
    setCorridor(newCorridor);
  };

  const handleRefresh = () => {
    fetchData(corridor);
  };

  return (
    <div style={styles.app}>
      <div style={styles.container}>
        <Header 
          corridor={corridor}
          onCorridorChange={handleCorridorChange}
          lastUpdated={lastUpdated || 'Loading...'}
        />

        {loading && !data && (
          <div style={styles.loading}>Loading data...</div>
        )}

        {error && (
          <div style={styles.error}>
            Error: {error}
            <button onClick={handleRefresh} style={styles.retryBtn}>Retry</button>
          </div>
        )}

        {data && !loading && (
          <>
            <StatsGrid data={data} />
            <ChartSection data={data} />
            <DataTable data={data} />
            <AIInsights data={data} />
            <Actions onRefresh={handleRefresh} loading={loading} />
          </>
        )}

        <div style={styles.footer}>
          Powered by <strong style={styles.footerBrand}>RAGFIN1</strong> • 
          Real-time competitive intelligence for cross-border payments • 
          Data updated every 2 hours
        </div>
      </div>
    </div>
  );
}

const styles = {
  app: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    background: '#0a0a0a',
    color: '#ffffff',
    minHeight: '100vh',
    padding: '40px 20px'
  },
  container: {
    maxWidth: '1400px',
    margin: '0 auto'
  },
  loading: {
    textAlign: 'center',
    padding: '60px',
    fontSize: '18px',
    color: '#888'
  },
  error: {
    textAlign: 'center',
    padding: '60px',
    fontSize: '18px',
    color: '#ff4444'
  },
  retryBtn: {
    marginTop: '20px',
    padding: '12px 24px',
    background: '#00ff88',
    color: '#000',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  footer: {
    textAlign: 'center',
    marginTop: '64px',
    paddingTop: '32px',
    borderTop: '1px solid #1a1a1a',
    color: '#555',
    fontSize: '13px'
  },
  footerBrand: {
    color: '#00ff88'
  }
};

export default App;
