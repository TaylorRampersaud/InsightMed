import './App.css';
import Button from '@mui/material/Button';
import TestHistoryGraph from './components/TestHistoryGraph';
import Carousel from './components/Carousel';

const data = [
  {
        "label": "Red Blood Cells",
        "valuenum": 3.33,
        "valueuom": "m/uL",
        "ref_range_lower": 3.9,
        "ref_range_upper": 5.2,
        "charttime": "2184-07-21 06:20:00",
        "flag": "abnormal",
        "subject_id": 10037928,
        "gender": "F",
        "anchor_age": 78,
        "history": [3.72, 3.63, 3.13, 2.76, 3.63, 3.68, 3.65,3.55, 3.07, 3.6, 3.67, 3.72, 3.41, 3.33],
        "metric_description": "Counts the total number of red blood cells in your blood.",
        "metric_interpretation": "This level is low, which can indicate anemia."
    },
    {
        "label": "Reticulocyte Count, Automated",
        "valuenum": 1.9,
        "valueuom": "%",
        "ref_range_lower": 1.2,
        "ref_range_upper": 3.2,
        "charttime": "2177-07-15 02:48:00",
        "flag": NaN,
        "subject_id": 10037928,
        "gender": "F",
        "anchor_age": 78,
        "history": [1.9],
        "metric_description": "Counts new red blood cells being made.",
        "metric_interpretation": "This is within normal limits, suggesting your body is making red blood cells appropriately."
    },
    {
        "label": "Sedimentation Rate",
        "valuenum": 65.0,
        "valueuom": "mm/hr",
        "ref_range_lower": 0.0,
        "ref_range_upper": 20.0,
        "charttime": "2178-09-28 20:45:00",
        "flag": "abnormal",
        "subject_id": 10037928,
        "gender": "F",
        "anchor_age": 78,
        "history": [74.0, 65.0],
        "metric_description": "Measures how quickly red blood cells settle at the bottom of a test tube, which can indicate inflammation.",
        "metric_interpretation": "This rate is high, suggesting there might be some inflammation or other issues in the body."
    }
];

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Button variant='Contained'>Submit!</Button>
        <Carousel data={data} />
      </header>
    </div>
  );
}

export default App;
