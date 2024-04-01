import { create } from "zustand";

interface InfoWindow {
  id: string;
  open: boolean;
}

interface InfoWindowStore {
  infoWindow: InfoWindow;
  setInfoWindow: (infoWindow: InfoWindow) => void;
}

export const useInfoWindowStore = create<InfoWindowStore>((set) => ({
  infoWindow: {
    id: "",
    open: false,
  },
  setInfoWindow: (infoWindow) => set({ infoWindow }),
}));
