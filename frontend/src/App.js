import React, { useState, useEffect } from 'react';
import { 
  getCompetitiveAnalysis, 
  getCompetitiveInsight, 
  getBinanceP2P,
  getCryptoRates,
  getCardPremiums
} from './services/api';
import './App.css';

function App() {
  const [corridor, setCorridor] = useState('MX');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  
  const [competitiveData, setCompetitiveData] = useState(null);
  const [insightData, setInsightData] = useState(null);
  const [binanceData, setBinanceData] = useState(null);
  const [cryptoData, setCryptoData] = useState(null);
  const [cardPremiums, setCardPremiums] = useState(null);

  const corridors = [
  { code: 'MX', name: 'Mexico', currency: 'MXN', flag: '🇲🇽' },
  { code: 'CO', name: 'Colombia', currency: 'COP', flag: '🇨🇴' },
  { code: 'BR', name: 'Brasil', currency: 'BRL', flag: '🇧🇷' },
  { code: 'AR', name: 'Argentina', currency: 'ARS', flag: '🇦🇷' },
  { code: 'VE', name: 'Venezuela', currency: 'VES', flag: '🇻🇪' },
  { code: 'CL', name: 'Chile', currency: 'CLP', flag: '🇨🇱' },
  { code: 'PE', name: 'Peru', currency: 'PEN', flag: '🇵🇪' },
  { code: 'BO', name: 'Bolivia', currency: 'BOB', flag: '🇧🇴' },
  { code: 'GT', name: 'Guatemala', currency: 'GTQ', flag: '🇬🇹' },
  { code: 'DO', name: 'Dominican Republic', currency: 'DOP', flag: '🇩🇴' },
  { code: 'SV', name: 'El Salvador', currency: 'USD', flag: '🇸🇻' },
  { code: 'HN', name: 'Honduras', currency: 'HNL', flag: '🇭🇳' },
  { code: 'NI', name: 'Nicaragua', currency: 'NIO', flag: '🇳🇮' },
  { code: 'CR', name: 'Costa Rica', currency: 'CRC', flag: '🇨🇷' },
  { code: 'PY', name: 'Paraguay', currency: 'PYG', flag: '🇵🇾' },
  { code: 'UY', name: 'Uruguay', currency: 'UYU', flag: '🇺🇾' },
  { code: 'EC', name: 'Ecuador', currency: 'USD', flag: '🇪🇨' },
  { code: 'PA', name: 'Panama', currency: 'PAB', flag: '🇵🇦' }
];

  const currentCorridor = corridors.find(c => c.code === corridor);

  useEffect(() => {
    let cancelled = false;
    
    setLoading(true);

    const amountValue = amount === '' ? 1000 : parseFloat(amount);
    const curr = corridors.find(c => c.code === corridor);

    Promise.all([
      getCompetitiveAnalysis(corridor).catch(() => null),
      getCompetitiveInsight(corridor).catch(() => null),
      getBinanceP2P(corridor, amountValue).catch(() => null),
      getCryptoRates(curr?.currency || 'MXN').catch(() => null),
      getCardPremiums(corridor, amountValue).catch(() => null)
    ]).then(([comp, insight, binance, crypto, premiums]) => {
      if (!cancelled) {
        setCompetitiveData(comp);
        setInsightData(insight);
        setBinanceData(binance);
        setCryptoData(crypto);
        setCardPremiums(premiums);
        setLoading(false);
      }
    });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [corridor, amount]);

  const handleRefresh = () => {
    setLoading(true);
    const amountValue = amount === '' ? 1000 : parseFloat(amount);
    const curr = corridors.find(c => c.code === corridor);

    Promise.all([
      getCompetitiveAnalysis(corridor).catch(() => null),
      getCompetitiveInsight(corridor).catch(() => null),
      getBinanceP2P(corridor, amountValue).catch(() => null),
      getCryptoRates(curr?.currency || 'MXN').catch(() => null),
      getCardPremiums(corridor, amountValue).catch(() => null)
    ]).then(([comp, insight, binance, crypto, premiums]) => {
      setCompetitiveData(comp);
      setInsightData(insight);
      setBinanceData(binance);
      setCryptoData(crypto);
      setCardPremiums(premiums);
      setLoading(false);
    });
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo-container">
          <div className="logo">
            RAGFIN<span className="accent">1</span>
          </div>
          <div className="version">v3.2.0</div>
        </div>
        
        <div className="controls">
          <div className="corridor-selector">
            <span className="label">CORRIDOR:</span>
            <span className="flag">🇺🇸</span>
            <span className="arrow">→</span>
            <select 
              value={corridor} 
              onChange={(e) => setCorridor(e.target.value)}
              className="select"
              onWheel={(e) => e.target.blur()}
            >
              {corridors.map(c => (
                <option key={c.code} value={c.code}>
                  {c.flag} {c.name} ({c.currency})
                </option>
              ))}
            </select>
          </div>

          <div className="amount-input">
            <span className="label">AMOUNT USD:</span>
            <input 
              type="text"
              pattern="[0-9]*\.?[0-9]*" 
              value={amount} 
              onChange={(e) => {
                const val = e.target.value.replace(/[^0-9.]/g, '');
                if (val === '' || !isNaN(val)) setAmount(val);
              }}
              className="input"
              placeholder="1000.00"
            />
          </div>

          <button onClick={handleRefresh} className="refresh-btn" disabled={loading}>
            {loading ? '⏳' : '🔄'} {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
      </header>

      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner">⏳</div>
          <div className="loading-text">Loading all endpoints for {currentCorridor?.name}...</div>
        </div>
      ) : (
        <div className="dashboard">
          
          <section className="endpoint-section">
            <div className="section-header">
              <h2>ENDPOINT: /api/v1/competitive-analysis/{corridor}</h2>
              <span className="badge">NUMERICAL DATA</span>
            </div>
            
            {!competitiveData ? (
              <div className="no-data">NO DATA AVAILABLE</div>
            ) : competitiveData?.most_competitive ? (
              <div className="content">
                <div className="stats-row">
                  <div className="stat-box leader">
                    <div className="stat-label">MOST COMPETITIVE</div>
                    <div className="stat-value">
                      ${competitiveData.most_competitive.total_cost.toFixed(2)}
                    </div>
                    <div className="stat-provider">{competitiveData.most_competitive.provider}</div>
                  </div>
                  
                  <div className="stat-box">
                    <div className="stat-label">PROVIDERS ANALYZED</div>
                    <div className="stat-value">{competitiveData.providers_analyzed.length}</div>
                    <div className="stat-detail">
                      {competitiveData.providers_analyzed.join(', ')}
                    </div>
                  </div>
                  
                  <div className="stat-box">
                    <div className="stat-label">DATA POINTS</div>
                    <div className="stat-value">{competitiveData.data_points}</div>
                    <div className="stat-detail">Real-time records</div>
                  </div>
                </div>

                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>PROVIDER</th>
                        <th>AVG RATE</th>
                        <th>AVG FEE</th>
                        <th>TOTAL COST</th>
                        <th>SAMPLES</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(competitiveData.stats_by_provider)
                        .sort((a, b) => a[1].total_cost - b[1].total_cost)
                        .map(([provider, stats]) => (
                          <tr key={provider}>
                            <td className="provider-cell">{provider}</td>
                            <td className="rate-cell">{stats.avg_rate.toFixed(4)}</td>
                            <td className="fee-cell">${stats.avg_fee.toFixed(2)}</td>
                            <td className="total-cell">${stats.total_cost.toFixed(2)}</td>
                            <td>{stats.sample_size}</td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div className="no-data">NO DATA AVAILABLE</div>
            )}
          </section>

          <section className="endpoint-section">
            <div className="section-header">
              <h2>ENDPOINT: /api/v1/card-premiums/{corridor}?amount={amount || 1000}</h2>
              <span className="badge premium">CARD PREMIUMS</span>
            </div>
            
            {!cardPremiums ? (
              <div className="no-data">NO DATA AVAILABLE</div>
            ) : cardPremiums?.providers ? (
              <div className="content">
                <div className="premiums-container">
                  {cardPremiums.providers.map((provider, idx) => (
                    <div key={idx} className="provider-premium-card">
                      <div className="provider-name">{provider.name}</div>
                      
                      <div className="payment-methods-grid">
                        <div className="payment-method bank">
                          <div className="method-label">Bank Transfer</div>
                          <div className="method-cost">${provider.bank_transfer.total_cost.toFixed(2)}</div>
                          <div className="method-detail">{provider.bank_transfer.method}</div>
                        </div>
                        
                        <div className="payment-method debit">
                          <div className="method-label">Debit Card</div>
                          <div className="method-cost">${provider.debit_card.total_cost.toFixed(2)}</div>
                          <div className="premium-badge debit">
                            +{provider.debit_card.premium_pct}% ({provider.debit_card.vs_bank})
                          </div>
                        </div>
                        
                        <div className="payment-method credit">
                          <div className="method-label">Credit Card</div>
                          <div className="method-cost">${provider.credit_card.total_cost.toFixed(2)}</div>
                          <div className="premium-badge credit">
                            +{provider.credit_card.premium_pct}% ({provider.credit_card.vs_bank})
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="no-data">NO DATA AVAILABLE</div>
            )}
          </section>

          <section className="endpoint-section">
            <div className="section-header">
              <h2>ENDPOINT: /api/v1/binance-p2p/{corridor}?amount={amount || 1000}</h2>
              <span className="badge crypto">CRYPTO P2P</span>
            </div>
            
            {!binanceData ? (
              <div className="no-data">NO DATA AVAILABLE</div>
            ) : binanceData?.data?.p2p_rate ? (
              <div className="content">
                <div className="stats-row">
                  <div className="stat-box crypto">
                    <div className="stat-label">BINANCE P2P RATE</div>
                    <div className="stat-value">{binanceData.data.p2p_rate.price} {currentCorridor?.currency}</div>
                    <div className="stat-detail">1 USD = {binanceData.data.p2p_rate.price} {currentCorridor?.currency}</div>
                  </div>
                  
                  <div className="stat-box">
                    <div className="stat-label">CRYPTO RECEIVED</div>
                    <div className="stat-value">
                      {binanceData.data.p2p_rate.crypto_received ? binanceData.data.p2p_rate.crypto_received.toFixed(4) : '0'} {binanceData.data.p2p_rate.crypto}
                    </div>
                    <div className="stat-detail">For ${amount || 1000} USD</div>
                  </div>
                  
                  <div className="stat-box">
                    <div className="stat-label">FEE</div>
                    <div className="stat-value">${binanceData.data.p2p_rate.fee || 0}</div>
                    <div className="stat-detail">No transfer fee</div>
                  </div>
                </div>
              </div>
            ) : binanceData?.data?.error ? (
              <div className="no-data">BINANCE P2P: {binanceData.data.error}</div>
            ) : (
              <div className="no-data">NO DATA AVAILABLE</div>
            )}
          </section>

          <section className="endpoint-section">
            <div className="section-header">
              <h2>ENDPOINT: /api/v1/crypto-rates?currencies={currentCorridor?.currency}</h2>
              <span className="badge crypto">STABLECOIN RATES</span>
            </div>
            
            {!cryptoData ? (
              <div className="no-data">NO DATA AVAILABLE</div>
            ) : cryptoData?.data?.rates ? (
              <div className="content">
                <div className="crypto-grid">
                  {Object.entries(cryptoData.data.rates).map(([coin, currencies]) => (
                    <div key={coin} className="crypto-card">
                      <div className="crypto-coin">{coin}</div>
                      {Object.entries(currencies).map(([curr, data]) => (
                        <div key={curr} className="crypto-rate-row">
                          <span className="curr-label">{curr}:</span>
                          <span className="rate-value">
                            {data.rate ? `${data.rate.toFixed(4)}` : 'N/A'}
                          </span>
                          <span className="source-label">({data.source})</span>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="no-data">NO DATA AVAILABLE</div>
            )}
          </section>

          <section className="endpoint-section ai">
            <div className="section-header">
              <h2>ENDPOINT: /api/v1/rag/competitive-insight/{corridor}</h2>
              <span className="badge ai">AI ANALYSIS</span>
            </div>
            
            {!insightData ? (
              <div className="no-data">NO DATA AVAILABLE</div>
            ) : insightData?.strategic_analysis ? (
              <div className="content">
                <div className="ai-analysis-container">
                  <pre className="ai-analysis">{insightData.strategic_analysis}</pre>
                </div>
                
                {insightData.metadata && (
                  <div className="ai-metadata">
                    <span>Model: {insightData.metadata.model}</span>
                    <span>•</span>
                    <span>Tokens: {insightData.metadata.total_tokens}</span>
                    <span>•</span>
                    <span>Query #{insightData.metadata.query_number}</span>
                  </div>
                )}
              </div>
            ) : (
              <div className="no-data">NO DATA AVAILABLE</div>
            )}
          </section>

        </div>
      )}

      <footer className="footer">
        <span>RAGFIN<span className="accent">1</span></span> • 
        API Base: <code>https://ragfin1.onrender.com</code> • 
        Real-time competitive intelligence
      </footer>
    </div>
  );
}

export default App;