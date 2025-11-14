const ConsolePanel = ({ logs }: { logs: string }) => {
  return (
    <div className="flex-1 p-3 bg-gray-950">
      <h3 className="text-xl font-semibold text-gray-300 uppercase tracking-wide mb-2">
        Console
      </h3>
      <pre className="text-md text-gray-100 font-mono whitespace-pre-wrap">
        {logs || <span className="text-gray-600 italic">Ready</span>}
      </pre>
    </div>
  );
};

export default ConsolePanel