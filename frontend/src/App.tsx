// src/App.tsx

import TrackContainerView from "./components/TrackContainerView";
import DemurrageLookup from "./components/DemurrageLookup";
import DemurrageRiskReport from "./components/DemurrageRiskReport";
import DemurrageSummary from "./components/DemurrageSummary";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen p-4 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-6">NVOCC Container Dashboard</h1>
      <TrackContainerView />
      <DemurrageLookup />
      <DemurrageSummary />
      <DemurrageRiskReport />
    </div>
  );
}

export default App;
