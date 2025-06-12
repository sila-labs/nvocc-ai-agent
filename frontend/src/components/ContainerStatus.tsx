// src/components/ContainerStatus.tsx

import React from 'react';

interface Props {
  data: {
    container_number: string;
    carrier: string;
    status: string;
    location: string;
    eta: string;
  } | null;
  error?: string;
}

const ContainerStatus: React.FC<Props> = ({ data, error }) => {
  if (error) {
    return <div className="mt-4 text-red-500">{error}</div>;
  }

  if (!data) {
    return null;
  }

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h2 className="text-xl font-bold mb-2">Container Status</h2>
      <p><strong>Container #:</strong> {data.container_number}</p>
      <p><strong>Status:</strong> {data.status}</p>
      <p><strong>Location:</strong> {data.location}</p>
      <p><strong>ETA:</strong> {new Date(data.eta).toLocaleString()}</p>
    </div>
  );
};

export default ContainerStatus;
