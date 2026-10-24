import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';

// Mesma origem no navegador: sessão anônima HttpOnly, sem credenciais no frontend.
export default defineConfig({plugins:[react()],server:{host:'127.0.0.1',port:5173,strictPort:true,proxy:{'/api':{target:'http://127.0.0.1:8000',changeOrigin:true}}},preview:{host:'127.0.0.1',port:4173,strictPort:true,proxy:{'/api':{target:'http://127.0.0.1:8000',changeOrigin:true}}}});
