import React, { useState, useEffect } from 'react';
import API from '../services/api';

const CardPremiums = ({ country, amount }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (country && amount) {
      fetchCardPremiums();
    }
  }, [country, amount]);

  const fetchCardPremiums = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await API.get(`/card-premiums/${country}?amount=${amount}`);
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error fetching card premiums');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card-premiums-section">
        <h3>💳 Card Payment Premiums</h3>
        <p>Loading card premium analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card-premiums-section">
        <h3>💳 Card Payment Premiums</h3>
        <p className="error">{error}</p>
      </div>
    );
  }

  if (!data || !data.providers || data.providers.length === 0) {
    return null;
  }

  return (
    <div className="card-premiums-section">
      <h3>💳 Card Payment Premiums Analysis</h3>
      <p className="subtitle">
        Cost comparison: Bank Transfer vs Debit Card vs Credit Card for {data.country} - ${data.amount} USD
      </p>

      <div className="card-premiums-grid">
        {data.providers.map((provider, index) => (
          <div key={index} className="provider-card-premium">
            <h4>{provider.name}</h4>
            
            <div className="payment-methods">
              <div className="payment-method bank">
                <div className="method-label">🏦 Bank Transfer</div>
                <div className="method-cost">${provider.bank_transfer.total_cost.toFixed(2)}</div>
                <div className="method-detail">{provider.bank_transfer.method}</div>
              </div>

              <div className="payment-method debit">
                <div className="method-label">💳 Debit Card</div>
                <div className="method-cost">${provider.debit_card.total_cost.toFixed(2)}</div>
                <div className="method-detail">
                  +{provider.debit_card.premium_pct}% fee (${provider.debit_card.premium_amount.toFixed(2)})
                </div>
                <div className="method-comparison">{provider.debit_card.vs_bank} vs Bank</div>
              </div>

              <div className="payment-method credit">
                <div className="method-label">💳 Credit Card</div>
                <div className="method-cost">${provider.credit_card.total_cost.toFixed(2)}</div>
                <div className="method-detail">
                  +{provider.credit_card.premium_pct}% fee (${provider.credit_card.premium_amount.toFixed(2)})
                </div>
                <div className="method-comparison">{provider.credit_card.vs_bank} vs Bank</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card-premium-summary">
        <p><strong>Key Insight:</strong> Credit cards typically cost 2-4x more than bank transfers due to payment processing fees.</p>
        <p className="endpoint-info">ENDPOINT: /api/v1/card-premiums/{data.country}?amount={data.amount}</p>
      </div>
    </div>
  );
};

export default CardPremiums;