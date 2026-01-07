import React from 'react';

const Header = ({ corridor, amount, onCorridorChange, onAmountChange, lastUpdated }) => {
  const corridors = [
    { code: 'MX', flag: '🇲🇽', name: 'Mexico' },
    { code: 'CO', flag: '🇨🇴', name: 'Colombia' },
    { code: 'BR', flag: '🇧🇷', name: 'Brasil' },
    { code: 'AR', flag: '🇦🇷', name: 'Argentina' },
    { code: 'VE', flag: '🇻🇪', name: 'Venezuela' },
    { code: 'CL', flag: '🇨🇱', name: 'Chile' },
    { code: 'PE', flag: '🇵🇪', name: 'Peru' },
    { code: 'BO', flag: '🇧🇴', name: 'Bolivia' },
    { code: 'GT', flag: '🇬🇹', name: 'Guatemala' },
    { code: 'DO', flag: '🇩🇴', name: 'Dominican Republic' },
    { code: 'SV', flag: '🇸🇻', name: 'El Salvador' }
  ];

  const currentCorridor = corridors.find(c => c.code === corridor);

  return (
    <div style={styles.header}>
      <div style={styles.logo}>
        RAGFIN<span style={styles.logoAccent}>1</span>
        <div style={styles.version}>v3.1</div>
      </div>
      
      <div style={styles.controls}>
        <div style={styles.corridor}>
          <span style={styles.flag}>🇺🇸</span>
          <span style={styles.arrow}>→</span>
          <select 
            value={corridor} 
            onChange={(e) => onCorridorChange(e.target.value)}
            style={styles.select}
          >
            {corridors.map(c => (
              <option key={c.code} value={c.code}>
                {c.flag} {c.name}
              </option>
            ))}
          </select>
        </div>

        <div style={styles.amountControl}>
          <span style={styles.label}>AMOUNT USD:</span>
          <input
            type="number"
            value={amount}
            onChange={(e) => onAmountChange(parseInt(e.target.value) || 500)}
            min="100"
            max="10000"
            step="100"
            style={styles.amountInput}
          />
        </div>
      </div>

      <div style={styles.updated}>
        Updated {lastUpdated}
      </div>
    </div>
  );
};

const styles = {
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '48px',
    paddingBottom: '24px',
    borderBottom: '1px solid #1a1a1a'
  },
  logo: {
    fontSize: '28px',
    fontWeight: '700',
    letterSpacing: '-1px',
    color: '#ffffff'
  },
  logoAccent: {
    color: '#00ff88'
  },
  version: {
    fontSize: '12px',
    color: '#00ff88',
    marginTop: '4px',
    fontWeight: '400'
  },
  controls: {
    display: 'flex',
    alignItems: 'center',
    gap: '24px'
  },
  corridor: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    fontSize: '18px'
  },
  flag: {
    fontSize: '32px'
  },
  arrow: {
    color: '#00ff88',
    fontSize: '24px'
  },
  select: {
    background: '#111',
    color: '#fff',
    border: '1px solid #333',
    borderRadius: '6px',
    padding: '8px 16px',
    fontSize: '16px',
    cursor: 'pointer'
  },
  amountControl: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  label: {
    fontSize: '12px',
    color: '#888',
    fontWeight: '600',
    letterSpacing: '1px'
  },
  amountInput: {
    background: '#111',
    color: '#fff',
    border: '1px solid #333',
    borderRadius: '6px',
    padding: '8px 12px',
    fontSize: '16px',
    width: '100px',
    textAlign: 'right'
  },
  updated: {
    fontSize: '14px',
    color: '#555'
  }
};

export default Header;