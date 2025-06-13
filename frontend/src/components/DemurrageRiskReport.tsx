// src/components/DemurrageRiskReport.tsx

import React, { useEffect, useState } from "react";

type RiskEntry = {
  bill_of_lading: string;
  charge_type: string;
  charges_end_date: string;
  days_remaining: number;
  risk_level: string;
};

type ReportResponse = {
  report_date: string;
  report: RiskEntry[];
};

const DemurrageRiskReport = () => {
  const [report, setReport] = useState<RiskEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/demurrage-risk-report")
      .then((res) => res.json())
      .then((data: ReportResponse) => {
        setReport(data.report);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load risk report:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-gray-600">Loading risk report...</p>;

  return (
    <div className="p-4 bg-white rounded shadow mt-6">
      <h2 className="text-2xl font-bold mb-4">Demurrage Risk Report</h2>
      {report.length === 0 ? (
        <p className="text-gray-500">No active risk entries today 🎉</p>
      ) : (
        <table className="w-full text-left border-collapse">
          <thead>
            <tr>
              <th className="border-b py-2">BOL #</th>
              <th className="border-b py-2">Type</th>
              <th className="border-b py-2">End Date</th>
              <th className="border-b py-2">Days Left</th>
              <th className="border-b py-2">Risk</th>
            </tr>
          </thead>
          <tbody>
            {report.map((entry, idx) => (
              <tr key={idx}>
                <td className="py-2">{entry.bill_of_lading}</td>
                <td className="py-2">{entry.charge_type}</td>
                <td className="py-2">{entry.charges_end_date}</td>
                <td className="py-2">{entry.days_remaining}</td>
                <td
                  className={`py-2 font-semibold ${
                    entry.risk_level === "High"
                      ? "text-red-600"
                      : entry.risk_level === "Medium"
                      ? "text-yellow-600"
                      : "text-green-600"
                  }`}
                >
                  {entry.risk_level}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DemurrageRiskReport;
