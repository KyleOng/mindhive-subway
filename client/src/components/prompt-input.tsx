import { BotMessageSquare, LoaderCircle } from "lucide-react";
import { useState } from "react";
import { QueryResult } from "../interfaces/query-result.interface";

const API_URL = import.meta.env.VITE_API_URL;

interface Props {
  queryResults: QueryResult[];
  setQueryResults: (queryResult: QueryResult[]) => void;
  setOpen: (open: boolean) => void;
}

const PromptInput = ({ queryResults, setQueryResults, setOpen }: Props) => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetchData() {
    try {
      setLoading(true);
      if (query === "") return;
      const params = new URLSearchParams({ input: query });
      const response = await fetch(`${API_URL}/ask?${params}`, {
        method: "POST",
      });
      if (response.ok) {
        const result = await response.json();
        setQueryResults([result, ...queryResults]);
        setQuery("");
      }
    } catch (error) {
      console.error(error);
      alert(
        "Something unusual happened while asking AI, please contact admin.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <input
        type="text"
        className="pointer-events-auto h-full w-[80%] bg-gray-50 px-4 text-sm font-light outline-none transition-all duration-200 ease-in-out focus:bg-white disabled:pointer-events-none disabled:bg-gray-50"
        placeholder="Ask something & press Enter (or click 'Send')"
        onClick={() => setOpen(true)}
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        disabled={loading}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            fetchData();
          }
        }}
      />
      <button
        className="pointer-events-auto flex h-full w-[20%] items-center justify-center gap-x-1 bg-blue-500 hover:bg-blue-600 disabled:pointer-events-none disabled:bg-blue-200"
        disabled={!open || query === "" || loading}
        onClick={() => fetchData()}
      >
        {loading ? (
          <LoaderCircle className="animate-spin stroke-white" size={18} />
        ) : (
          <>
            <BotMessageSquare className="stroke-white" size={18} />
            <span className="text-sm font-semibold text-white">Send</span>
          </>
        )}
      </button>
    </>
  );
};

export default PromptInput;
