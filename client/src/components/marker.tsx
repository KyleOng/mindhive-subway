import {
  AdvancedMarker,
  Pin,
  useAdvancedMarkerRef
} from "@vis.gl/react-google-maps";
import { Outlet } from "../interfaces/outlet.interface";
import { useHighlightedMarkersStore } from "../store/highlighted-markers";
import { useInfoWindowStore } from "../store/info-window";
import InfoWindow from "./info-window";

interface Props {
  outlet: Outlet;
}

function Marker({ outlet }: Props) {
  const [markerRef, marker] = useAdvancedMarkerRef();
  const { infoWindow, setInfoWindow } = useInfoWindowStore();
  const { highlightedMarkers, setHighlightedMarkers } =
    useHighlightedMarkersStore();

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
        <InfoWindow outlet={outlet} marker={marker}/>
      )}
    </>
  );
}

export default Marker;
