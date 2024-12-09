import * as React from 'react';
import { ChartContainer } from '@mui/x-charts/ChartContainer';
import { ChartsReferenceLine } from '@mui/x-charts/ChartsReferenceLine';
import { LinePlot, MarkPlot } from '@mui/x-charts/LineChart';
import { ChartsXAxis } from '@mui/x-charts/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts/ChartsYAxis';

const TestHistoryGraph = ({ testValues, ref_range_lower, ref_range_upper }) => {
  const xLabels = Array.from({ length: testValues.length }, (_, i) => i + 1);

  return (
    <ChartContainer
      width={500}
      height={300}
      series={[
        { data: testValues, label: 'Test Values', type: 'line' },
      ]}
      xAxis={[
        {
          scaleType: 'point',
          data: xLabels,
          min: 0, // Ensure x-axis starts from 0
        },
      ]}
      yAxis={[
        {
          min: 0, // Ensure y-axis starts from 0
        },
      ]}
      background="white" // White background for the chart
      grid={{ x: true, y: true }} // Add gridlines
    >
      {/* Smooth Line */}
      <LinePlot
        lineStyle={{ stroke: '#4A90E2', strokeWidth: 2 }} // Smooth line style
        tension={0.5} // Adjust for a smoother curve
      />

      {/* Point for the Most Recent Value */}
      <MarkPlot
        data={[{ x: xLabels[testValues.length - 1], y: testValues[testValues.length - 1] }]} // Show only the last point
        markerStyle={{
          fill: '#FF5722',
          stroke: 'white',
          r: 6, // Radius of the point
        }}
      />

      {/* Reference Lines */}
      {ref_range_lower !== ref_range_upper ? (
        <>
          <ChartsReferenceLine
            y={ref_range_lower}
            label="Lower Range"
            lineStyle={{ stroke: 'blue', strokeDasharray: '4 4' }}
          />
          <ChartsReferenceLine
            y={ref_range_upper}
            label="Upper Range"
            lineStyle={{ stroke: 'blue', strokeDasharray: '4 4' }}
          />
        </>
      ) : (
        <ChartsReferenceLine
          y={ref_range_upper}
          label="Upper Range"
          lineStyle={{ stroke: 'blue', strokeDasharray: '4 4' }}
        />
      )}

      {/* X-Axis */}
      <ChartsXAxis
        label="Time Point"
        tickStyle={{
          stroke: 'gray',
          strokeWidth: 1,
        }}
      />

      {/* Y-Axis */}
      <ChartsYAxis
        label="Test Values"
        tickStyle={{
          stroke: 'gray',
          strokeWidth: 1,
        }}
      />
    </ChartContainer>
  );
};

export default TestHistoryGraph;
