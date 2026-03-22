// src/api.js 생성
import axios from 'axios';

const api = axios.create({
  // Vercel에 배포된 본인의 fi2 백엔드 주소를 입력하세요
  baseURL: 'https://fi2-beryl.vercel.app',   
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;