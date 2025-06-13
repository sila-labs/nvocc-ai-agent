import React, { useEffect, useState } from "react";

const DemurrageSummary = () => {
  const [summary, setSummary] = useState("Loading summary...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/demurrage-risk-summary")
      .then((res) => res.json())
      .then((data) => setSummary(data.summary))
      .catch(() => setSummary("Failed to load summary."));
  }, []);

  return (
    <div className="p-4 bg-yellow-100 border-l-4 border-yellow-500 rounded mt-6">
      <h2 className="text-lg font-semibold mb-2">📋 AI Risk Summary</h2>
      <p className="text-gray-800">{summary}</p>
    </div>
  );
};

export default DemurrageSummary;
