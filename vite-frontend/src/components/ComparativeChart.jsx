/** @jsxImportSource @emotion/react */
import React from 'react';
import { Bar } from 'react-chartjs-2';
import styled from '@emotion/styled';

const ChartContainer = styled.div`
  width: 80%;
  margin-top: 40px;
`;

const ComparativeChart = ({ report }) => {
  const companies = Object.keys(report);

  // Prepare labels (quarters) and datasets for each company
  const labels = ['Q1', 'Q2', 'Q3', 'Q4'];
  const datasets = companies.map(company => {
    const data = labels.map((quarter) => {
      const summary = report[company][quarter];
      return summary.length; // For simplicity, we're using the length of the summary as a metric.
    });
    
    return {
      label: company,
      data: data,
      backgroundColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.6)`,
      borderColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 1)`,
      borderWidth: 1,
    };
  });

  const data = {
    labels: labels,
    datasets: datasets
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <ChartContainer>
      <Bar data={data} options={options} />
    </ChartContainer>
  );
};

export default ComparativeChart;
