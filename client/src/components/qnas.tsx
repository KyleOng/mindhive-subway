import { useState } from "react";
import { useLocalStorage } from "usehooks-ts";
import { QueryResult as IQueryResult } from "../interfaces/query-result.interface";
import { cn } from "../lib/utils";
import PromptInput from "./prompt-input";
import QnA from "./qna";

function QnAs() {
  const [open, setOpen] = useState(false);
  const [queryResults, setQueryResults] = useLocalStorage<IQueryResult[]>(
    "queryResults",
    [],
  );

  return (
    <div className="group flex w-[28rem] flex-col overflow-hidden shadow-lg">
      <div className="z-10 flex h-14 w-full items-center">
        <PromptInput
          queryResults={queryResults}
          setQueryResults={setQueryResults}
          setOpen={setOpen}
        />
      </div>
      <div
        className={cn(
          "flex h-0 w-full -translate-y-[100%] flex-col gap-y-4 bg-blue-100 p-0 transition-all",
          open && "h-[600px] translate-y-0 px-6 pb-4 pt-6",
        )}
      >
        <div className="flex flex-grow flex-col gap-y-6 overflow-y-auto">
          {queryResults.length === 0 && (
            <div className="flex h-full items-center justify-center">
              <h1 className="text-lg text-slate-500">
                There's nothing to show here. Start asking the AI!
              </h1>
            </div>
          )}
          {queryResults.map((queryResult, key) => (
            <QnA
              key={key}
              queryResult={queryResult}
              setQueryResults={() =>
                setQueryResults([
                  ...queryResults.slice(0, key),
                  ...queryResults.slice(key + 1, queryResults.length),
                ])
              }
            />
          ))}
        </div>

        <div className="flex justify-end">
          <button
            className="text-sm hover:font-medium hover:text-blue-600 hover:underline"
            onClick={() => setOpen(false)}
          >
            Hide
          </button>
        </div>
      </div>
    </div>
  );
}

export default QnAs;
