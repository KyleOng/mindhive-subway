import {
  AdvancedMarker,
  InfoWindow,
  Pin,
  useAdvancedMarkerRef,
} from "@vis.gl/react-google-maps";
import { Outlet } from "../interfaces/outlet.interface";
import { useInfoWindowStore } from "../store/info-window";
import wazeLogo from "/waze.svg";
import { Loader2 } from "lucide-react";
import { useHighlightedMarkersStore } from "../store/highlighted-markers";
import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;
const DISTANCE = 5;

interface Props {
  outlet: Outlet;
}

function Marker({ outlet }: Props) {
  const [markerRef, marker] = useAdvancedMarkerRef();
  const { infoWindow, setInfoWindow } = useInfoWindowStore();
  const { highlightedMarkers, setHighlightedMarkers } =
    useHighlightedMarkersStore();
  const [loading, setLoading] = useState(false);

  async function fetchAndHighlightOutletsWithinRadius({
    latitude,
    longitude,
  }: Outlet) {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        latitude: latitude.toString(),
        longitude: longitude.toString(),
        distance: DISTANCE.toString(),
      });
      const response = await fetch(
        `${API_URL}/outlets/within_radius?${params}`,
        {
          method: "POST",
        },
      );
      if (response.ok) {
        const results = await response.json();
        setHighlightedMarkers(
          results.map((result: Outlet) => result.id.toString()),
        );
        setInfoWindow({ id: outlet.id.toString(), open: false });
      }
    } catch (error) {
      console.error(error);
      alert(
        "Something unusual happened while fetching for outlets within radius, please contact admin.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <AdvancedMarker
        ref={markerRef}
        position={{ lat: outlet.latitude, lng: outlet.longitude }}
        onClick={() => {
          setHighlightedMarkers([]);
          setInfoWindow({
            id: outlet.id.toString(),
            open: true,
          });
        }}
        title={outlet.name}
      >
        {infoWindow.id === outlet.id.toString() ? (
          <Pin
            background={"blue"}
            borderColor={"darkblue"}
            glyphColor={"darkblue"}
            scale={1.5}
          />
        ) : highlightedMarkers.includes(outlet.id.toString()) ? (
          <Pin
            background={"green"}
            borderColor={"darkgreen"}
            glyphColor={"darkgreen"}
            scale={1.5}
          />
        ) : (
          <Pin
            background={"red"}
            borderColor={"darkred"}
            glyphColor={"darkred"}
            scale={1.5}
          />
        )}
      </AdvancedMarker>
      {infoWindow.id === outlet.id.toString() && infoWindow.open && (
        <InfoWindow
          anchor={marker}
          onCloseClick={() => setInfoWindow({ id: "", open: false })}
        >
          <div className="flex max-w-[500px] flex-col gap-y-2 p-2">
            <h1 className="text-lg font-medium">{outlet.name}</h1>
            <p className="text-sm">{outlet.address}</p>
            <div className="flex gap-x-2">
              <a target="_blank" href={outlet.waze_link}>
                <img
                  src={wazeLogo}
                  className="h-10 w-10 rounded-full bg-blue-200 p-2 hover:bg-blue-300"
                  alt="Waze logo"
                />
              </a>
              <button
                className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-200 p-2 hover:bg-blue-300"
                onClick={() => fetchAndHighlightOutletsWithinRadius(outlet)}
              >
                {loading ? (
                  <Loader2 size={24} className="animate-spin" />
                ) : (
                  <span className="font-medium">5KM</span>
                )}
              </button>
            </div>
          </div>
        </InfoWindow>
      )}
    </>
  );
}

export default Marker;
