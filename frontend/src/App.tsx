import TrackContainerView from "./components/TrackContainerView";
import DemurrageLookup from "./components/DemurrageLookup";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen p-4">
      <h1 className="text-3xl font-bold text-center mb-6">NVOCC Container Tracker</h1>
      
      <div className="max-w-3xl mx-auto space-y-8">
        <TrackContainerView />
        <DemurrageLookup />
      </div>
    </div>
  );
}

export default App;
