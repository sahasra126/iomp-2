// import { useEffect, useState } from "react";
// import { Bar, Pie } from "react-chartjs-2";
// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   BarElement,
//   ArcElement,
//   Title,
//   Tooltip,
//   Legend,
// } from "chart.js";
// import "./Visualization.css";

// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   BarElement,
//   ArcElement,
//   Title,
//   Tooltip,
//   Legend
// );

// export default function Visualization({ result }) {
//   const [chartData, setChartData] = useState({
//     labels: ["Healthy", "PCOS Risk"],
//     datasets: [
//       {
//         label: "Probability",
//         data: [100, 0],
//         backgroundColor: ["#198754", "#dc3545"],
//       },
//     ],
//   });

//   useEffect(() => {
//     if (result) {
//       setChartData({
//         labels: ["Healthy", "PCOS Risk"],
//         datasets: [
//           {
//             label: "Probability (%)",
//             data: [(1 - result.probability) * 100, result.probability * 100],
//             backgroundColor: ["#198754", "#dc3545"],
//           },
//         ],
//       });
//     }
//   }, [result]);

//   if (!result) return null; // hide chart if no result yet

//   return (
//     <div className="visualization-container container my-4">
//       <h2 className="text-center mb-3">Your PCOS Risk Visualization</h2>
//       <p className="text-center">
//         This chart shows your probability of PCOS vs Healthy range.
//       </p>

//       <div className="row">
//         <div className="col-md-6 mb-4">
//           <Bar data={chartData} options={{ responsive: true }} />
//         </div>
//         <div className="col-md-6 mb-4">
//           <Pie data={chartData} options={{ responsive: true }} />
//         </div>
//       </div>
//     </div>
//   );
// }
import { useEffect, useState } from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "./Visualization.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

export default function Visualization({ result }) {
  const [chartData, setChartData] = useState({
    labels: ["Healthy", "PCOS Risk"],
    datasets: [
      {
        label: "Probability (%)",
        data: [100, 0],
        backgroundColor: ["#198754", "#dc3545"],
        borderRadius: 6, // rounded bars
      },
    ],
  });

  useEffect(() => {
    if (result) {
      setChartData({
        labels: ["Healthy", "PCOS Risk"],
        datasets: [
          {
            label: "Probability (%)",
            data: [(1 - result.probability) * 100, result.probability * 100],
            backgroundColor: ["#198754", "#dc3545"],
            borderRadius: 6,
          },
        ],
      });
    }
  }, [result]);

  if (!result) return null;

  const barOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      tooltip: { enabled: true },
      title: { display: false },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 14 } },
        stacked: false,
      },
      y: {
        beginAtZero: true,
        max: 100,
        ticks: { font: { size: 14 } },
      },
    },
    barThickness: 30, // thinner bars
    maxBarThickness: 40,
  };

  const pieOptions = {
    responsive: true,
    plugins: {
      legend: { position: "bottom" },
      tooltip: { enabled: true },
    },
  };

  return (
    <div className="visualization-container container my-4">
      <h2 className="text-center mb-3">Your PCOS Risk Visualization</h2>
      <p className="text-center">
        This chart shows your probability of PCOS vs Healthy range.
      </p>

      <div className="row">
        <div className="col-md-6 mb-4 d-flex justify-content-center">
          <Bar data={chartData} options={barOptions} />
        </div>
        <div className="col-md-6 mb-4 d-flex justify-content-center">
          <Pie data={chartData} options={pieOptions} />
        </div>
      </div>
    </div>
  );
}
