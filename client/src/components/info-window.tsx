import { InfoWindow as GInfoWindow } from "@vis.gl/react-google-maps";
import { Loader2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Outlet } from "../interfaces/outlet.interface";
import { useHighlightedMarkersStore } from "../store/highlighted-markers";
import { useInfoWindowStore } from "../store/info-window";
import wazeLogo from "/waze.svg";
import { OperatingHour } from "../interfaces/operating-hours.interface";

const API_URL = import.meta.env.VITE_API_URL;
const DISTANCE = 5;
const DAYS_OF_WEEK = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

interface Props {
  outlet: Outlet;
  marker: google.maps.marker.AdvancedMarkerElement | null;
}

const InfoWindow = ({ outlet, marker }: Props) => {
  const { infoWindow, setInfoWindow } = useInfoWindowStore();
  const { setHighlightedMarkers } = useHighlightedMarkersStore();
  const [loading, setLoading] = useState(false);
  const [operatingHours, setOperatingHours] = useState<OperatingHour[]>([]);

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

  async function fetchOperatingHours() {
    try {
      const params = new URLSearchParams({
        outlet_id: outlet.id.toString(),
      });
      const response = await fetch(
        `${API_URL}/outlets/operating_hours?${params}`,
        {
          method: "POST",
        },
      );
      if (response.ok) {
        const results = await response.json();
        setOperatingHours(results);
      }
    } catch (error) {
      console.error(error);
      alert(
        "Something unusual happened while fetching for operating hours, please contact admin.",
      );
    }
  }

  useEffect(() => {
    if (
      infoWindow.open &&
      infoWindow.id === outlet.id.toString() &&
      operatingHours.length === 0
    ) {
      fetchOperatingHours();
    }
  }, [infoWindow.open]);

  return (
    <GInfoWindow
      anchor={marker}
      onCloseClick={() => setInfoWindow({ id: "", open: false })}
    >
      <div className="flex max-w-[500px] flex-col gap-y-2 p-2">
        <h1 className="text-lg font-medium">{outlet.name}</h1>
        <p className="text-sm">{outlet.address}</p>
        <div>
          {operatingHours.map((operatingHour, key) => (
            <div className="flex w-40 justify-between" key={key}>
              <p>{DAYS_OF_WEEK[operatingHour.day_of_week]}:</p>
              <p>
                {operatingHour.start_time.slice(0, 5)} -{" "}
                {operatingHour.end_time.slice(0, 5)}
              </p>
            </div>
          ))}
        </div>
        <div className="flex gap-x-3">
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
    </GInfoWindow>
  );
};

export default InfoWindow;
