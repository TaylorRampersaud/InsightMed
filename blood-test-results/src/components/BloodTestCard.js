import * as React from "react";
import TestHistoryGraph from "./TestHistoryGraph";

const BloodTestCard = ({ testData }) => {
  // Calculate the position of the marker on the number line
  const calculateMarkerPosition = () => {
    const lower = testData.ref_range_lower;
    const upper = testData.ref_range_upper;
    const value = testData.valuenum;

    if (value < lower) return 0; // Marker is at the far left
    if (value > upper) return 100; // Marker is at the far right

    // Calculate percentage position within the range
    return ((value - lower) / (upper - lower)) * 100;
  };

  const markerPosition = calculateMarkerPosition();

  return (
    <div
      className={`border-4 rounded-lg p-6 space-y-8 ${
        testData.flag === "abnormal" ? "bg-red-100" : "bg-green-100"
      }`}
    >
      {/* Text Section */}
      <div className="space-y-4 text-black">
        {/* Blood Test Label */}
        <h1 className="text-4xl font-extrabold">{testData.label}</h1>

        {/* Test Value */}
        <p
          className={`text-6xl font-bold ${
            testData.flag === "abnormal" ? "text-red-500" : "text-green-500"
          }`}
        >
          {testData.valuenum}
          {testData.valueuom}
        </p>

        {/* Standard Range */}
        <p className="text-xl">
          <span className="font-semibold">Standard range: </span>
          {testData.ref_range_lower}
          {testData.valueuom} - {testData.ref_range_upper}
          {testData.valueuom}
        </p>

        {/* Number Line */}
        <div className="relative mt-4 h-3 rounded-full bg-gradient-to-r from-red-500 via-green-500 to-red-500">
          {/* Marker */}
          <div
            className="absolute top-0 -translate-x-1/2 w-5 h-5 bg-blue-500 rounded-full border-2 border-white shadow-md"
            style={{ left: `${markerPosition}%` }}
          ></div>
        </div>

        {/* Labels for the number line */}
        <div className="flex justify-between text-sm text-gray-600 mt-2">
          <span>{testData.ref_range_lower}{testData.valueuom}</span>
          <span>{testData.ref_range_upper}{testData.valueuom}</span>
        </div>

        {/* Definition */}
        <p className="text-lg text-left">
          <span className="font-bold">Definition: </span>
          {testData.metric_description}
        </p>

        {/* Interpretation */}
        <p className="text-lg text-left">
          <span className="font-bold">Interpretation: </span>
          {testData.metric_interpretation}
        </p>
      </div>

      {/* Graph Section */}
      <div>
        <TestHistoryGraph
          testValues={testData.history}
          ref_range_lower={testData.ref_range_lower}
          ref_range_upper={testData.ref_range_upper}
        />
      </div>
    </div>
  );
};

export default BloodTestCard;
