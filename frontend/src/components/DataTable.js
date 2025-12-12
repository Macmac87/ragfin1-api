import React from 'react';

const DataTable = ({ data }) => {
  if (!data || !data.numerical_analysis) return null;

  const { stats_by_provider } = data.numerical_analysis;
  const providers = Object.entries(stats_by_provider);
  
  // Sort by total cost
  providers.sort((a, b) => a[1].total_cost - b[1].total_cost);

  return (
    <div style={styles.section}>
      <div style={styles.title}>Detailed Breakdown</div>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Provider</th>
            <th style={styles.th}>Exchange Rate</th>
            <th style={styles.th}>Transfer Fee</th>
            <th style={styles.th}>Total Cost</th>
            <th style={styles.th}>Sample Size</th>
          </tr>
        </thead>
        <tbody>
          {providers.map(([name, stats], index) => (
            <tr 
              key={name} 
              style={{
                ...styles.tr,
                background: index === 0 ? 'rgba(0, 255, 136, 0.05)' : 'transparent'
              }}
            >
              <td style={{...styles.td, fontWeight: '600'}}>{name}</td>
              <td style={{...styles.td, color: '#00ff88'}}>
                {stats.avg_rate.toFixed(4)}
              </td>
              <td style={{...styles.td, color: '#ffd700'}}>
                ${stats.avg_fee.toFixed(2)}
              </td>
              <td style={{...styles.td, fontWeight: '700', fontSize: '17px'}}>
                ${stats.total_cost.toFixed(2)}
              </td>
              <td style={styles.td}>{stats.sample_size} records</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
  section: {
    background: '#111',
    border: '1px solid #1a1a1a',
    borderRadius: '12px',
    padding: '32px',
    marginBottom: '48px'
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '24px',
    color: '#ffffff'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  th: {
    textAlign: 'left',
    padding: '16px',
    fontSize: '12px',
    textTransform: 'uppercase',
    letterSpacing: '1px',
    color: '#666',
    borderBottom: '1px solid #1a1a1a'
  },
  tr: {
    borderBottom: '1px solid #0a0a0a'
  },
  td: {
    padding: '20px 16px',
    fontSize: '15px',
    color: '#ffffff'
  }
};

export default DataTable;