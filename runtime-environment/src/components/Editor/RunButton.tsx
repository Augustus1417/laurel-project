const RunButton = ({ onClick, disabled }: { onClick: () => void; disabled: boolean }) => {
  return (
    <div className="flex items-center justify-center px-4">
      <button
        onClick={onClick}
        disabled={disabled}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors duration-150 shadow-lg hover:shadow-xl flex items-center gap-2"
      >
        <span className="text-xl">▶</span>
        <span className="text-xl">Run</span>
      </button>
    </div>
  );
};

export default RunButton;