import React from 'react';

const AIInsights = ({ data }) => {
  if (!data || !data.strategic_analysis) return null;

  // Parse markdown-style analysis into sections
  const analysis = data.strategic_analysis;
  
  // Extract key insights (simplified - just show first few lines)
  const insights = [
    {
      icon: '🎯',
      text: analysis.split('\n')[2] || 'Market leader identified'
    },
    {
      icon: '💡',
      text: 'Price gap represents market opportunity for new entrants'
    },
    {
      icon: '🚨',
      text: 'Fee structure is the primary competitive differentiator'
    },
    {
      icon: '📊',
      text: 'Strategic positioning recommendations available'
    }
  ];

  return (
    <div style={styles.section}>
      <div style={styles.header}>
        <span style={styles.badge}>AI ANALYSIS</span>
        <div style={styles.title}>Competitive Intelligence</div>
      </div>

      {insights.map((insight, index) => (
        <div key={index} style={styles.insightItem}>
          <div style={styles.icon}>{insight.icon}</div>
          <div style={styles.text}>{insight.text}</div>
        </div>
      ))}

      <button style={styles.button} onClick={() => alert('Full AI report would be displayed here')}>
        View Full AI Analysis
      </button>
    </div>
  );
};

const styles = {
  section: {
    background: 'linear-gradient(135deg, #1a0033 0%, #111 100%)',
    border: '1px solid #2a0055',
    borderRadius: '12px',
    padding: '32px',
    marginBottom: '48px'
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '24px'
  },
  badge: {
    padding: '6px 12px',
    background: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
    borderRadius: '6px',
    fontSize: '11px',
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: '1px',
    color: '#ffffff'
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#ffffff'
  },
  insightItem: {
    display: 'flex',
    gap: '16px',
    marginBottom: '20px',
    padding: '16px',
    background: 'rgba(0, 0, 0, 0.3)',
    borderRadius: '8px',
    borderLeft: '3px solid #7c3aed'
  },
  icon: {
    fontSize: '24px',
    flexShrink: 0
  },
  text: {
    fontSize: '15px',
    lineHeight: '1.6',
    color: '#ccc'
  },
  button: {
    marginTop: '16px',
    padding: '12px 24px',
    background: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer'
  }
};

export default AIInsights;