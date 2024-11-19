import * as React from 'react';
import TestHistoryGraph from './TestHistoryGraph';

const BloodTestCard = ({ testData }) => {
    return (
      <div className='border-4 border-black'>
        <h1>{testData.label}</h1>
        <TestHistoryGraph testValues={testData.history} />
        <p>Test Value: {testData.valuenum + testData.valueuom}</p>
        <p>Ref range: {testData.ref_range_lower +" - "+ testData.ref_range_upper}</p>
        <p>{testData.metric_description}</p>
        <p>{testData.metric_interpretation}</p>
      </div>
    )
}

export default BloodTestCard

