import {
  APIProvider,
  AdvancedMarker,
  InfoWindow,
  Map,
  Pin,
} from "@vis.gl/react-google-maps";
import { useEffect, useState } from "react";
import QueryResults from "./components/query-results";
import { Outlet } from "./interfaces/outlet.interface";

const API_URL = import.meta.env.VITE_API_URL;
const GOOGLE_GEOCODING_API_KEY = import.meta.env.VITE_GOOGLE_GEOCODING_API_KEY;
const GOOGLE_MAP_ID = import.meta.env.VITE_GOOGLE_MAP_ID;

const App = () => {
  const position = { lat: 3.1319, lng: 101.6841 };
  const [outlets, setOutlets] = useState<Outlet[]>([]);

  const [open, setOpen] = useState(false);
  const [outlet, setOutlet] = useState<Outlet>();

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
          defaultCenter={position}
          defaultZoom={14}
          disableDefaultUI={true}
          mapId={GOOGLE_MAP_ID}
          onClick={() => {
            setOpen(false);
          }}
          disableDoubleClickZoom
        >
          {outlets.map((outlet, key) => (
            <AdvancedMarker
              key={key}
              position={{ lat: outlet.latitude, lng: outlet.longitude }}
              onClick={() => {
                setOpen(true);
                setOutlet(outlet);
              }}
            >
              <Pin />
            </AdvancedMarker>
          ))}
          {open && outlet !== undefined && (
            <InfoWindow
              position={{ lat: outlet.latitude, lng: outlet.longitude }}
              onCloseClick={() => setOpen(false)}
            >
              <p>{outlet.name}</p>
              <p>{outlet.address}</p>
            </InfoWindow>
          )}
        </Map>
      </APIProvider>
      <div className="fixed right-0 top-0 m-5">
        <QueryResults />
      </div>
    </div>
  );
};

export default App;
