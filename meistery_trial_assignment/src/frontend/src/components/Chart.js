import React from "react";
import { Bar } from "react-chartjs-2";

const Chart = (props) => {
  const data = props.data;

  if (!data || data === undefined) {
    return null;
  }

  const labels = data.map((row) => row["product"]);

  const state = {
    labels: labels,
    datasets: [
      {
        label: props.yAxisLabel,
        backgroundColor: "#0000FF",
        borderColor: "rgba(0,0,0,1)",
        borderWidth: 2,
        data: data.map((row) => row[props.yAxisLabel]),
      },
    ],
  };

  return (
    <div>
      <Bar
        data={state}
        options={{
          title: {
            display: true,
            text: `${props.yAxisLabel} per product`,
            fontSize: 20,
          },
          legend: {
            display: true,
            position: "right",
          },
        }}
      />
    </div>
  );
};

export default Chart;
