import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Competitive Analysis
export const getCompetitiveAnalysis = async (destination) => {
  const response = await api.get(`/api/v1/competitive-analysis/${destination}`);
  return response.data;
};

// RAG Competitive Insight
export const getCompetitiveInsight = async (destination) => {
  const response = await api.get(`/api/v1/rag/competitive-insight/${destination}`);
  return response.data;
};

// Binance P2P
export const getBinanceP2P = async (destination, amount = 1000) => {
  const response = await api.get(`/api/v1/binance-p2p/${destination}`, {
    params: { amount }
  });
  return response.data;
};

// Crypto Rates
export const getCryptoRates = async (currencies) => {
  const response = await api.get('/api/v1/crypto-rates', {
    params: { currencies }
  });
  return response.data;
};

// Card Premiums
export const getCardPremiums = async (destination, amount = 1000) => {
  const response = await api.get(`/api/v1/card-premiums/${destination}`, {
    params: { amount }
  });
  return response.data;
};

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;