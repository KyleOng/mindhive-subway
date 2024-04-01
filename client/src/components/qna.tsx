import { Trash2 } from "lucide-react";
import { QueryResult } from "../interfaces/query-result.interface";
import dayjs from "dayjs";

interface Props {
  queryResult: QueryResult;
  setQueryResults: () => void;
}

const QnA = ({  queryResult, setQueryResults }: Props) => {
  return (
    <div
      className="flex flex-col gap-y-1 rounded bg-white p-4 shadow-lg"
    >
      <div className="flex items-start justify-between">
        <p className="text-sm font-medium text-blue-500">{queryResult.input}</p>
        <button onClick={setQueryResults}>
          <Trash2 size={18} />
        </button>
      </div>
      <p className="text-xs text-slate-600">
        {queryResult.output.split("\n").map((line, key) => (
          <span key={key}>
            {line}
            <br />
          </span>
        ))}
      </p>
      <div className="flex justify-end">
        <small className="text-xs text-slate-400">
          Queried at{" "}
          {dayjs(queryResult.datetime).format("YYYY MMM D, HH:mm:ss")}
        </small>
      </div>
    </div>
  );
};

export default QnA;
