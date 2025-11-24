const RunButton = ({
  onClick,
  disabled,
  onStop,
  isRunning,
}: {
  onClick: () => void;
  disabled: boolean;
  onStop?: () => void;
  isRunning?: boolean;
}) => {
  return (
    <div className="flex flex-col items-center justify-center px-4 gap-2">
      <button
        onClick={onClick}
        disabled={disabled}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors duration-150 shadow-lg hover:shadow-xl flex items-center gap-2"
      >
        <span className="text-xl">▶</span>
        <span className="text-xl">Run</span>
      </button>

      <button
        onClick={() => onStop && onStop()}
        disabled={!isRunning}
        className="px-6 py-3 bg-red-600 hover:bg-red-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors duration-150 shadow-lg hover:shadow-xl flex items-center gap-2"
        title="Stop execution"
      >
        <span className="text-xl">■</span>
        <span className="text-xl">Stop</span>
      </button>
    </div>
  );
};

export default RunButton;