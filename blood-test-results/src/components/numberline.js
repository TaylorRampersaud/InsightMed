import * as React from 'react';

const NumberLine = ({ start, end, interval }) => {
    const numbers = [];
    for (let i = start; i <= end; i += interval) {
      numbers.push(i);
    }
  
    return (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        {numbers.map((num) => (
          <div key={num} style={{ margin: '0 10px' }}>
            <div style={{ width: '2px', height: '10px', backgroundColor: 'black' }} />
            <span>{num}</span>
          </div>
        ))}
      </div>
    );
  };
  
  export default NumberLine;