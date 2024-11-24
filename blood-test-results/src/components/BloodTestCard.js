import * as React from 'react';
import TestHistoryGraph from './TestHistoryGraph';

// const BloodTestCard = ({ testData }) => {
//   return (
//     <div className="flex border-4 rounded-lg shadow-xl shadow-white p-6 space-x-8">
//       {/* Text Section */}
//       <div className="flex flex-col space-y-4 text-black">
//         {/* Blood Test Label */}
//         <h1 className="text-4xl font-extrabold">{testData.label}</h1>
        
//         {/* Test Value */}
//         <p className={`text-7xl font-bold ${testData.flag === "abnormal" ? "text-red-500" : "text-green-500"}`}>
//           {testData.valuenum}{testData.valueuom}
//         </p>

//         {/* Interpretation */}
//         <p className="text-lg">
//           <span className="font-bold">Interpretation: </span>
//           {testData.metric_interpretation}
//         </p>
        
//         {/* Standard Range */}
//         <p className="text-xl">
//           <span className="font-semibold">Standard range: </span>
//           {testData.ref_range_lower}{testData.valueuom} - {testData.ref_range_upper}{testData.valueuom}
//         </p>


//         {/* Definition */}
//         <p className="text-lg">
//           <span className="font-bold">Definition: </span>
//           {testData.metric_description}
//         </p>

//       </div>

//       {/* Graph Section */}
//       <div className="flex-grow">
//         <TestHistoryGraph testValues={testData.history} />
//       </div>
//     </div>
//   );
// };


const BloodTestCard = ({ testData }) => {
  return (
    <div
      className={`flex border-4 rounded-lg p-6 space-x-8 ${
        testData.flag === "abnormal" ? "bg-red-100" : "bg-green-100"
      }`}
    >
      {/* Text Section */}
      <div className="flex flex-col space-y-4 text-black">
        {/* Blood Test Label */}
        <h1 className="text-4xl font-extrabold">{testData.label}</h1>

        {/* Test Value */}
        <p
          className={`text-7xl font-bold ${
            testData.flag === "abnormal" ? "text-red-500" : "text-green-500"
          }`}
        >
          {testData.valuenum}
          {testData.valueuom}
        </p>

        {/* Interpretation */}
        <p className="text-lg">
          <span className="font-bold">Interpretation: </span>
          {testData.metric_interpretation}
        </p>

        {/* Standard Range */}
        <p className="text-xl">
          <span className="font-semibold">Standard range: </span>
          {testData.ref_range_lower}
          {testData.valueuom} - {testData.ref_range_upper}
          {testData.valueuom}
        </p>

        {/* Definition */}
        <p className="text-lg">
          <span className="font-bold">Definition: </span>
          {testData.metric_description}
        </p>
      </div>

      {/* Graph Section */}
      <div className="flex-grow">
        <TestHistoryGraph testValues={testData.history} />
      </div>
    </div>
  );
};

export default BloodTestCard;



