import React from "react";

interface ComputerCharacterProps {
  speech?: string | null;
  awaitingInput?: boolean;
}

const ComputerCharacter: React.FC<ComputerCharacterProps> = ({ speech, awaitingInput }) => {
  return (
    <div className="relative w-32 h-32 flex flex-col items-center justify-end m-4">
      {/* Speech bubble */}
      {speech && (
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-full bg-gray-200 text-gray-900 p-2 rounded-md shadow-md w-40 text-sm text-center">
          {speech}
        </div>
      )}

      {/* Input indicator */}
      {awaitingInput && (
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 text-xs text-blue-400 animate-pulse">
          Awaiting input...
        </div>
      )}
    </div>
  );
};

export default ComputerCharacter;
