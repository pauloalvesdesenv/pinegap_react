import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Registrar os componentes do Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const GruposAtivosBarChart = () => {
  // Dados para o gráfico
  const data = {
    labels: ['Ativo A', 'Ativo B', 'Ativo C', 'Ativo D', 'Ativo E'],
    datasets: [
      {
        label: 'Score',
        data: [75, 85, 90, 60, 95], // Scores para cada ativo
        backgroundColor: 'rgba(54, 162, 235, 0.6)', // Cor das barras
        borderColor: 'rgba(54, 162, 235, 1)', // Cor da borda das barras
        borderWidth: 1,
      },
    ],
  };

  // Opções do gráfico
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Grupos de Ativos',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Nome', // Eixo X é o Nome dos ativos
        },
      },
      y: {
        title: {
          display: true,
          text: 'Score', // Eixo Y é o Score
        },
        beginAtZero: true,
      },
    },
  };

  return <Bar data={data} options={options} />;
};

export default GruposAtivosBarChart;
