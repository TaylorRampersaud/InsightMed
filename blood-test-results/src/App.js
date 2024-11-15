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
      </header>
    </div>
  );
}

export default App;
