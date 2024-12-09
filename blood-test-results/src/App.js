import './App.css';
import Carousel from './components/Carousel';
import logo from './components/insightmedlogo.jpeg'; 
import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function App() {
  const [data, setData] = useState({ data: [], overview: "" }); // Storing both parts in one state
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!input.trim()) {
      setError("Please enter a valid Subject ID.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:5000/subject/${input}`);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const result = await res.json();
      setData({ data: result.data, overview: result.overview });
      setInput("");
    } catch (error) {
      console.error("Fetch error:", error);
      setError("Failed to fetch data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <header>
          <img src={logo} alt="Logo" className="logo" />
        </header>
        <h1>Simple Search Box</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            className="text-black"
            placeholder="Enter Subject ID"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Go"}
          </button>
        </form>
        {error && <p className="error-message">{error}</p>}

        {data.overview && (
          <Card
            sx={{
              maxWidth: 1100,
              mx: 'auto',
              mt: 4,
              p: 3,
              background: 'white', 
              borderRadius: 2,
              boxShadow: 1,
            }}
          >
            <CardContent>
              <Typography 
                variant="h6" 
                component="div" 
                color="primary" 
                gutterBottom
              >
              </Typography>
              <Typography 
                variant="body1" 
                color="text.primary" 
                sx={{
                  textAlign: 'justify', 
                  mx: 'auto',
                  fontSize: '18px',      // Adjust font size
                  fontFamily: 'arial', // Adjust font family
                  fontWeight: '400',     // Adjust font weight
                  lineHeight: '1.6',            
                }}
              >
                {data.overview}
              </Typography>
            </CardContent>
          </Card>
        )}

        {/* {data.overview && (<div className="max-w-4xl mx-auto bg-gray-200 text-left rounded-lg mt-100 p-6">
          <p className="text-base text-black leading-relaxed text-gray-800">
            {data.overview}</p></div>)} */}
x 
        {/* Render Data */}
        {data.data && data.data.length > 0 ? (
          <Carousel data={data.data} />
        ) : (
          data.data && <p>No results found.</p>
        )}
      </header>
    </div>
  );
}

export default App;

