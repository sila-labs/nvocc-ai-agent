// src/components/TrackContainerView.tsx

import { useState } from "react";
import ContainerSearch from "./ContainerSearch";
import ContainerStatus from "./ContainerStatus";

export default function TrackContainerView() {
  const [trackingData, setTrackingData] = useState<any>(null);
  const [error, setError] = useState("");

  const handleSearch = async (containerId: string) => {
    setError("");
    setTrackingData(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/track/${containerId}`);
      if (!res.ok) throw new Error("Failed to fetch container data");
      const data = await res.json();
      setTrackingData(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-8">
      <ContainerSearch onSearch={handleSearch} />
      <ContainerStatus data={trackingData} error={error} />
    </div>
  );
}
