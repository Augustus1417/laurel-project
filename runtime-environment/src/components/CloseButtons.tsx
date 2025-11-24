const CloseButtons = () => {
  return (
    <div className="flex items-center h-full gap-2 no-drag">
      {/* MINIMIZE */}
      <button
        onClick={() => window?.electron?.minimize()}
        className="w-8 h-8 flex items-center justify-center rounded-md tileStyleButton"
      >
        <svg
          stroke="currentColor"
          fill="currentColor"
          strokeWidth="0"
          viewBox="0 0 16 16"
          height="14"
          width="14"
        >
          <path d="M15 8H1V7h14v1z"></path>
        </svg>
      </button>

      {/* MAXIMIZE */}
      <button
        onClick={() => window?.electron?.maximize()}
        className="w-8 h-8 flex items-center justify-center rounded-md tileStyleButton"
      >
        <svg
          stroke="currentColor"
          fill="currentColor"
          strokeWidth="0"
          viewBox="0 0 16 16"
          height="14"
          width="14"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M3.5 4l.5-.5h8l.5.5v8l-.5.5H4l-.5-.5V4zm1 .5v7h7v-7h-7z"
          ></path>
        </svg>
      </button>

      {/* CLOSE */}
      <button
        onClick={() => window?.electron?.close()}
        className="w-8 h-8 flex items-center justify-center rounded-md tileStyleButton 
                   hover:bg-red-600 hover:text-white"
      >
        <span className="text-lg leading-none">&times;</span>
      </button>
    </div>
  );
};

export default CloseButtons;
