import { RefObject } from "react";
import { Outlet } from "../interfaces/outlet.interface";
import { useHighlightedMarkersStore } from "../store/highlighted-markers";
import { useInfoWindowStore } from "../store/info-window";

interface Props {
  outlets: Outlet[];
  selectRef: RefObject<HTMLSelectElement>;
}

const Select = ({ outlets, selectRef }: Props) => {
  const { setInfoWindow } = useInfoWindowStore();
  const { setHighlightedMarkers } = useHighlightedMarkersStore();

  return (
    <select
      ref={selectRef}
      className="h-14 min-w-[350px] p-4 text-sm text-slate-500 shadow-lg"
      onChange={(event) => {
        const outlet = outlets.find(
          (outlet) => outlet.id.toString() === event.target.value,
        );
        if (outlet) {
          setHighlightedMarkers([]);
          setInfoWindow({ id: outlet.id.toString(), open: true });
        }
      }}
    >
      <option disabled selected>
        -- Select An Outlet --
      </option>
      {outlets.map((outlet, key) => (
        <option key={key} value={outlet.id}>
          {outlet.name}
        </option>
      ))}
    </select>
  );
};

export default Select;
