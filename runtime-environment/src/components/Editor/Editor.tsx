import React, { useRef } from "react";
import LineNumbers from "./LineNumbers";

interface EditorProps {
  value: string;
  onChange: (value: string) => void;
}

const Editor: React.FC<EditorProps> = ({ value, onChange }) => {
  const lines = value.split("\n");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Tab") {
      e.preventDefault();
      const textarea = e.currentTarget;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const tab = "  ";
      const newValue = value.substring(0, start) + tab + value.substring(end);
      onChange(newValue);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + tab.length;
      }, 0);
    }
  };

  const handleScroll = (e: React.UIEvent<HTMLTextAreaElement>) => {
    const lineNumbers = e.currentTarget.previousElementSibling as HTMLElement;
    if (lineNumbers) {
      lineNumbers.scrollTop = e.currentTarget.scrollTop;
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".lrl")) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        const text = ev.target?.result as string;
        onChange(text);
      };
      reader.readAsText(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  return (
    <div
      className="flex flex-col h-full p-3 border-r border-gray-700"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xl font-semibold text-gray-300 uppercase tracking-wide">
          Editor
        </h3>
        <span className="text-xl text-gray-500">Laurel</span>
      </div>
      <div className="flex-1 flex border border-gray-700 rounded-md overflow-hidden bg-gray-900">
        <LineNumbers lineCount={lines.length} />
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onScroll={handleScroll}
          onKeyDown={handleKeyDown}
          placeholder="Write your Laurel code here..."
          className="flex-1 resize-none bg-gray-900 text-gray-100 px-3 py-3 text-xl font-mono focus:outline-none"
          style={{ lineHeight: "24px" }}
          spellCheck={false}
        />
      </div>
    </div>
  );
};

export default Editor;
