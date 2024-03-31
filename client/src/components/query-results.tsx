import { BotMessageSquare, LoaderCircle } from "lucide-react";
import { useState } from "react";
import { cn } from "../lib/utils";
import { QueryResult as IQueryResult } from "../interfaces/query-result.interface";
import { useLocalStorage } from "usehooks-ts";

const API_URL = import.meta.env.VITE_API_URL;

function QueryResults() {
  const [open, setOpen] = useState(false);
  const [queryResults, setQueryResults] = useLocalStorage<IQueryResult[]>(
    "queryResults",
    [],
  );
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetchData() {
    try {
      setLoading(true);
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
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="group flex w-[32rem] flex-col overflow-hidden">
      <div className="z-10 flex h-14 w-full items-center">
        <input
          type="text"
          className="pointer-events-auto h-full w-[80%] bg-gray-50 px-4 font-light outline-none transition-all duration-200 ease-in-out focus:bg-white disabled:pointer-events-none disabled:bg-gray-50"
          placeholder="Ask something & press Enter (or click 'Send')"
          onClick={() => setOpen(true)}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          disabled={loading}
        />
        <button
          className="pointer-events-auto flex h-full w-[20%] items-center justify-center gap-x-1 bg-blue-500 hover:bg-blue-600 disabled:pointer-events-none disabled:bg-blue-200"
          disabled={!open || query === "" || loading}
          onClick={() => query !== "" && fetchData()}
        >
          {loading ? (
            <LoaderCircle className="animate-spin stroke-white" size={24} />
          ) : (
            <>
              <BotMessageSquare className="stroke-white" size={24} />
              <span className="font-semibold text-white">Send</span>
            </>
          )}
        </button>
      </div>
      <div
        className={cn(
          "flex h-[800px] w-full -translate-y-[100%] flex-col gap-y-2 bg-blue-100 px-6 pb-8 pt-2 transition-all",
          open && "translate-y-0",
        )}
      >
        <div className="flex justify-end">
          <button
            className="hover:font-medium hover:text-blue-600 hover:underline"
            onClick={() => setOpen(false)}
          >
            Hide
          </button>
        </div>
        <div className="flex flex-grow flex-col gap-y-6 overflow-y-auto">
          {queryResults.map((queryResult, key) => (
            <div className="rounded bg-white p-4 shadow-lg" key={key}>
              <p className="font-medium text-blue-500">{queryResult.input}</p>
              <p className="text-sm text-slate-600">
                {queryResult.output.split("\n").map((line, key) => (
                  <>
                    <span key={key}>{line}</span>
                    <br />
                  </>
                ))}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default QueryResults;
