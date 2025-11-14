import React from "react";

interface LineNumbersProps {
  lineCount: number;
}

const LineNumbers: React.FC<LineNumbersProps> = ({ lineCount }) => {
  return (
    <div className="bg-gray-800 text-gray-500 text-md font-mono text-right select-none overflow-hidden py-3">
      {Array.from({ length: Math.max(lineCount, 1) }, (_, i) => (
        <div key={i} className="px-3 h-6">
          {i + 1}
        </div>
      ))}
    </div>
  );
};

export default LineNumbers;
