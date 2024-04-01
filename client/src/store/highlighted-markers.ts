import { create } from "zustand";

interface HighlightedMarkersStore {
  highlightedMarkers: string[];
  setHighlightedMarkers: (highlightedMarkers: string[]) => void;
}

export const useHighlightedMarkersStore = create<HighlightedMarkersStore>(
  (set) => ({
    highlightedMarkers: [],
    setHighlightedMarkers: (highlightedMarkers) => set({ highlightedMarkers }),
  }),
);
