import React from 'react';

const StatsGrid = ({ data }) => {
  if (!data || !data.numerical_analysis) return null;

  const { numerical_analysis } = data;
  const mostCompetitive = numerical_analysis.most_competitive;
  const providers = numerical_analysis.stats_by_provider;
  
  // Calculate market average
  const avgCost = Object.values(providers).reduce((sum, p) => sum + p.total_cost, 0) / Object.keys(providers).length;
  
  // Calculate price gap (most expensive - cheapest)
  const costs = Object.values(providers).map(p => p.total_cost);
  const priceGap = Math.max(...costs) - Math.min(...costs);

  return (
    <div style={styles.grid}>
      <div style={{...styles.card, ...styles.leaderCard}}>
        <div style={styles.label}>Most Competitive</div>
        <div style={{...styles.value, color: '#00ff88'}}>
          ${mostCompetitive.total_cost.toFixed(2)}
        </div>
        <div style={styles.detail}>{mostCompetitive.provider} • Total Cost</div>
        <span style={styles.badge}>LEADER</span>
      </div>

      <div style={styles.card}>
        <div style={styles.label}>Market Average</div>
        <div style={styles.value}>${avgCost.toFixed(2)}</div>
        <div style={styles.detail}>Across {Object.keys(providers).length} providers</div>
      </div>

      <div style={styles.card}>
        <div style={styles.label}>Price Gap</div>
        <div style={styles.value}>${priceGap.toFixed(2)}</div>
        <div style={styles.detail}>Most vs Least expensive</div>
      </div>

      <div style={styles.card}>
        <div style={styles.label}>Data Points</div>
        <div style={styles.value}>{numerical_analysis.data_points}</div>
        <div style={styles.detail}>Real-time records</div>
      </div>
    </div>
  );
};

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '20px',
    marginBottom: '48px'
  },
  card: {
    background: '#111',
    border: '1px solid #1a1a1a',
    borderRadius: '12px',
    padding: '24px',
    transition: 'all 0.3s ease'
  },
  leaderCard: {
    borderColor: '#00ff88',
    background: 'linear-gradient(135deg, #001a0f 0%, #111 100%)'
  },
  label: {
    fontSize: '12px',
    textTransform: 'uppercase',
    letterSpacing: '1px',
    color: '#666',
    marginBottom: '12px'
  },
  value: {
    fontSize: '36px',
    fontWeight: '700',
    marginBottom: '8px',
    color: '#ffffff'
  },
  detail: {
    fontSize: '14px',
    color: '#888'
  },
  badge: {
    display: 'inline-block',
    padding: '4px 12px',
    background: '#00ff88',
    color: '#000',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    marginTop: '8px'
  }
};

export default StatsGrid;