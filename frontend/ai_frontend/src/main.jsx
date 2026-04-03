import { StrictMode } from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { createRoot } from 'react-dom/client'
import Upload from './routes/upload'
import './index.css'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
)
