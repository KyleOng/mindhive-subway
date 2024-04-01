import { APIProvider, Map } from "@vis.gl/react-google-maps";
import { useEffect, useRef, useState } from "react";
import Marker from "./components/marker";
import QnAs from "./components/qnas";
import { Outlet } from "./interfaces/outlet.interface";
import { useHighlightedMarkersStore } from "./store/highlighted-markers";
import { useInfoWindowStore } from "./store/info-window";
import Select from "./components/select";

const API_URL = import.meta.env.VITE_API_URL;
const GOOGLE_GEOCODING_API_KEY = import.meta.env.VITE_GOOGLE_GEOCODING_API_KEY;
const GOOGLE_MAP_ID = import.meta.env.VITE_GOOGLE_MAP_ID;
const KUALA_LUMPUR_POSITION = { lat: 3.1319, lng: 101.6841 };

const App = () => {
  const [outlets, setOutlets] = useState<Outlet[]>([]);
  const { setInfoWindow } = useInfoWindowStore();
  const { setHighlightedMarkers } = useHighlightedMarkersStore();
  const selectRef = useRef<HTMLSelectElement>(null);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    try {
      const response = await fetch(`${API_URL}/outlets`);
      if (response.ok) {
        const outlets = await response.json();
        setOutlets(outlets);
      }
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="relative">
      <APIProvider apiKey={GOOGLE_GEOCODING_API_KEY}>
        <Map
          style={{ width: "100vw", height: "100vh" }}
          defaultCenter={KUALA_LUMPUR_POSITION}
          defaultZoom={13}
          disableDefaultUI={true}
          mapId={GOOGLE_MAP_ID}
          disableDoubleClickZoom
          onClick={() => {
            setHighlightedMarkers([]);
            setInfoWindow({ id: "", open: false });
            if (selectRef.current) {
              selectRef.current.selectedIndex = 0;
            }
          }}
        >
          {outlets.map((outlet, key) => (
            <Marker key={key} outlet={outlet} />
          ))}
        </Map>
      </APIProvider>
      <div className="fixed right-0 top-0 m-5">
        <QnAs />
      </div>

      <div className="fixed left-0 top-0 m-5">
        <Select selectRef={selectRef} outlets={outlets}/>
      </div>
    </div>
  );
};

export default App;
