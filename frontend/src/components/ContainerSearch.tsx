
import React from 'react';

const ContainerSearch = () => {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-2">Search Container</h2>
      <input
        type="text"
        placeholder="Enter container ID"
        className="border p-2 rounded w-full"
      />
    </div>
  );
};

export default ContainerSearch;