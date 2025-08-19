import { useEffect, useState } from 'preact/hooks'
// import { useEffect, useState } from 'react';
import './app.css'
import { Routes, Route } from 'react-router-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from './components/header.jsx';
import Footer from './components/footer.jsx';
import Home from './components/Home.jsx';
import Tools from './components/Tools.jsx';
import NewJob from './components/jobs/New.jsx';
import SearchJobs from './components/jobs/Search.jsx';

// const VITE_TEXT_PROCESSOR_API_URL = import.meta.env.VITE_TEXT_PROCESSOR_API_URL
const VITE_TEXT_PROCESSOR_API_URL = 'http://localhost:8000'

export function App() {
  
  return (
    <Router>
      <div>
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/new-job" element={<NewJob />} />
            <Route path="/search-jobs" element={<SearchJobs />} />
            <Route path="/tools" element={<Tools />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
