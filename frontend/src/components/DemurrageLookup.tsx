import React, { useState } from 'react';
import axios from 'axios';

const DemurrageLookup = () => {
  const [chargeType, setChargeType] = useState<'DMR' | 'DET'>('DMR');
  const [bol, setBol] = useState('');
  const [endDate, setEndDate] = useState('');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleLookup = async () => {
    setResult(null);
    setError(null);

    try {
      const params = new URLSearchParams({
        billOfLadingNumber: bol,
      });
      if (endDate) {
        params.append('chargesEndDate', endDate);
      }

      const res = await axios.get(
        `http://localhost:8000/api/v1/demurrage-detention/${chargeType}?${params.toString()}`
      );
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Something went wrong.');
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h2 className="text-xl font-bold mb-2">Import Demurrage & Detention Lookup</h2>

      <div className="mb-2">
        <label className="block font-semibold">Charge Type</label>
        <select
          value={chargeType}
          onChange={(e) => setChargeType(e.target.value as 'DMR' | 'DET')}
          className="border p-1 rounded w-full"
        >
          <option value="DMR">Demurrage</option>
          <option value="DET">Detention</option>
        </select>
      </div>

      <div className="mb-2">
        <label className="block font-semibold">Bill of Lading Number</label>
        <input
          type="text"
          value={bol}
          onChange={(e) => setBol(e.target.value)}
          className="border p-1 rounded w-full"
          placeholder="e.g., VAS000001"
        />
      </div>

      <div className="mb-4">
        <label className="block font-semibold">Charges End Date (optional)</label>
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border p-1 rounded w-full"
        />
      </div>

      <button
        onClick={handleLookup}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Search
      </button>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {result && (
        <pre className="bg-gray-100 text-sm mt-4 p-2 rounded overflow-auto max-h-96">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default DemurrageLookup;
