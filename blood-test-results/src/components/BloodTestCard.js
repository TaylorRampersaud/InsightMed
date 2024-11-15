import * as React from 'react';
import TestHistoryGraph from './TestHistoryGraph';

const BloodTestCard = ({ testHistory,  }) => {
    return (
      <div>
        <h1>{testHistory.label}</h1>
        <TestHistoryGraph testValues={testHistory.testValues} />
        <p></p>
      </div>
    )
}

export default TestHistoryGraph
