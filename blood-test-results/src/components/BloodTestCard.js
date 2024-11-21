import * as React from 'react';
import TestHistoryGraph from './TestHistoryGraph';

const BloodTestCard = ({ testData }) => {
    return (
      <div className={`text-black border-4 shadow-xl shadow-white p-4` }>
        <h1>{testData.label}</h1>
        <TestHistoryGraph testValues={testData.history} />
        <p className={`${testData.flag === "abnormal" ? "text-red-500" : "text-green-500"}`}>
          Test Value: {testData.valuenum + testData.valueuom}
        </p>
        <p>Standard range: {testData.ref_range_lower + testData.valueuom + " - " + testData.ref_range_upper + testData.valueuom}</p>
        <p>{"Definition: " + testData.metric_description}</p>
        <p>{"Interpretation: " + testData.metric_interpretation}</p>
      </div>
    );
}

export default BloodTestCard;


