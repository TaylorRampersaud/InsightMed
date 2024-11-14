import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';
import TestHistoryGraph from './components/TestHistoryGraph';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Button variant='Contained'>Submit!</Button>
        <TestHistoryGraph testValues={[1,2,3]} />
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
