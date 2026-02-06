import axios from "axios";
const BASE = "http://127.0.0.1:5001";

export const getArticles = (company) => axios.get(`${BASE}/articles/${company}`);
export const getMetrics = (company) => axios.get(`${BASE}/metrics/${company}`);
export const getTrending = (company) => axios.get(`${BASE}/trending/${company}`);
