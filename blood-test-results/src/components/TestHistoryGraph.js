import * as React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';

const arrayRange = (stop) => {
  return Array.from(
  { length: stop },
  (value, index) => 1 + index
  );
}

const TestHistoryGraph = ({ testValues }) => {
    return (
      <LineChart 
        xAxis = {[{ data: arrayRange(testValues.length)}]}
        series = {[{ data: testValues}]}
        width = {500}
        height={300}
      />
    )
}

export default TestHistoryGraph