import React from 'react';

const ChartSection = ({ data }) => {
  if (!data || !data.numerical_analysis) return null;

  const { stats_by_provider } = data.numerical_analysis;
  const providers = Object.entries(stats_by_provider);
  
  // Sort by total cost (ascending)
  providers.sort((a, b) => a[1].total_cost - b[1].total_cost);
  
  // Calculate max for scaling bars
  const maxCost = Math.max(...providers.map(p => p[1].total_cost));

  return (
    <div style={styles.section}>
      <div style={styles.header}>
        <div style={styles.title}>Total Cost Comparison (USD $1,000 transfer)</div>
        <div style={styles.legend}>
          <div style={styles.legendItem}>
            <div style={{...styles.legendDot, background: '#00ff88'}}></div>
            <span>Exchange Rate</span>
          </div>
          <div style={styles.legendItem}>
            <div style={{...styles.legendDot, background: '#ffd700'}}></div>
            <span>Fees</span>
          </div>
        </div>
      </div>

      <div style={styles.bars}>
        {providers.map(([name, stats], index) => {
          const percentage = (stats.total_cost / maxCost) * 100;
          const barColor = index === 0 ? 'green' : index === 1 ? 'yellow' : 'red';
          
          return (
            <div key={name} style={styles.barRow}>
              <div style={styles.providerName}>{name}</div>
              <div style={styles.barContainer}>
                <div style={{
                  ...styles.barFill,
                  width: `${percentage}%`,
                  background: barColor === 'green' 
                    ? 'linear-gradient(90deg, #00ff88 0%, #00cc6a 100%)'
                    : barColor === 'yellow'
                    ? 'linear-gradient(90deg, #ffd700 0%, #ffaa00 100%)'
                    : 'linear-gradient(90deg, #ff4444 0%, #cc0000 100%)',
                  color: barColor === 'red' ? '#fff' : '#000'
                }}>
                  Rate: {stats.avg_rate.toFixed(2)} • Fee: ${stats.avg_fee.toFixed(2)}
                </div>
              </div>
              <div style={styles.costLabel}>${stats.total_cost.toFixed(2)}</div>
            </div>
          );
        })}
      </div>
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
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '32px'
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#ffffff'
  },
  legend: {
    display: 'flex',
    gap: '24px',
    fontSize: '13px',
    color: '#ffffff'
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  legendDot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%'
  },
  bars: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },
  barRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  },
  providerName: {
    width: '120px',
    fontSize: '14px',
    fontWeight: '500',
    textAlign: 'right',
    color: '#ffffff'
  },
  barContainer: {
    flex: 1,
    height: '48px',
    background: '#0a0a0a',
    borderRadius: '6px',
    position: 'relative',
    overflow: 'hidden'
  },
  barFill: {
    height: '100%',
    borderRadius: '6px',
    display: 'flex',
    alignItems: 'center',
    padding: '0 16px',
    fontWeight: '600',
    fontSize: '16px',
    transition: 'width 1s ease'
  },
  costLabel: {
    width: '100px',
    textAlign: 'right',
    fontSize: '18px',
    fontWeight: '700',
    color: '#ffffff'
  }
};

export default ChartSection;