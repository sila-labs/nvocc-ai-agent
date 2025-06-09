import React, { useEffect, useState } from 'react';
import client from '../api/client';
import ContainerSearch from '../components/ContainerSearch';
import ContainerStatus from '../components/ContainerStatus';

const Dashboard = () => {
  const [health, setHealth] = useState('');

  useEffect(() => {
    client.get('/health').then((res) => setHealth(res.data.status));
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-4">NVOCC AI Agent Dashboard</h1>
      <p>Backend Health: {health}</p>
      <ContainerSearch />
      <ContainerStatus />
    </div>
  );
};

export default Dashboard;
