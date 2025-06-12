// src/components/ContainerSearch.tsx

import React, { useState } from 'react';

interface Props {
  onSearch: (containerId: string) => void;
}

const ContainerSearch: React.FC<Props> = ({ onSearch }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(input);
  };

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-2">Search Container</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter container ID"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="border p-2 rounded w-full"
          required
        />
        <button type="submit" className="mt-2 bg-blue-600 text-white px-4 py-2 rounded">
          Track
        </button>
      </form>
    </div>
  );
};

export default ContainerSearch;
