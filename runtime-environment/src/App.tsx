import { useState, useEffect, useRef } from "react";
import Header from "./components/Header";
import RunButton from "./components/Editor/RunButton";
import OutputPanel from "./components/OutputPanel";
import ConsolePanel from "./components/ConsolePanel";
import Editor from "./components/Editor/Editor";

export default function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [consoleLog, setConsoleLog] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const stopRequestedRef = useRef(false);
  const [currentFilePath, setCurrentFilePath] = useState<string | null>(null);

  const [inputState, setInputState] = useState<{ prompt: string; type: string } | null>(null);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    if (!window.electron?.onLaurelInput) return;

    const unsubscribe = window.electron.onLaurelInput(({ prompt, type }) => {
      setInputState({ prompt, type });
      setInputValue("");
      setConsoleLog(`Awaiting ${type} input${prompt ? `: ${prompt}` : ""}`);
    });

    return unsubscribe;
  }, []);

  const handleInputSubmit = () => {
    if (!inputState) return;

    window.electron?.sendLaurelInput(inputValue);
    setConsoleLog(`Submitted ${inputState.type} input`);
    setInputState(null);
    setInputValue("");
  };

  const handleRun = async () => {
    stopRequestedRef.current = false;
    setIsRunning(true);
    setConsoleLog("Running...");
    setOutput("");
    setInputState(null);
    setInputValue("");

    try {
      const result = await window.api.runLaurel(code);
      if (!stopRequestedRef.current) {
        setOutput(result || "No output");
        setConsoleLog("Execution completed successfully");
      }
    } catch (err: unknown) {
      if (!stopRequestedRef.current) {
        setOutput("");
        let message = err instanceof Error ? err.message : String(err);
        setConsoleLog(message.replace("Error invoking remote method 'laurel:run': ", ""));
      }
    } finally {
      setIsRunning(false);
      stopRequestedRef.current = false;
    }
  };

  const handleStop = () => {
    // Fire-and-forget stop signal to main process. main can decide how to interrupt execution.
    try {
      (window.api as any).stopLaurel?.();
    } catch (e) {
      // ignore if not available
    }
    // Immediately clear output and update UI so user can run again
    setIsRunning(false);
    setOutput("");
    stopRequestedRef.current = true;
    setConsoleLog("Execution stopped by user");
    // Clear any pending input state
    setInputState(null);
    setInputValue("");
  };

  return (
    <>
  <Header code={code} onChangeCode={setCode} setConsoleLog={setConsoleLog} currentFilePath={currentFilePath} setCurrentFilePath={setCurrentFilePath} />
      <div className="flex h-screen bg-gray-800 text-gray-100 font-mono overflow-hidden">
        {/* Left Panel - Editor */}
        <div className="flex-[2]">
          <Editor value={code} onChange={setCode} />
        </div>

        {/* Center - Run Button */}
  <RunButton onClick={handleRun} disabled={isRunning || !!inputState} onStop={handleStop} isRunning={isRunning} />

        {/* Right Panel */}
        <div className="flex-[1.2] flex flex-col border-l border-gray-700 relative">

          {/* Output Panel now handles input too */}
          <OutputPanel
            output={output}
            awaitingInput={!!inputState}
            isRunning={isRunning}
            isError={consoleLog.startsWith("Error")}
            inputState={inputState}
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSubmitInput={handleInputSubmit}
          />

          <ConsolePanel logs={consoleLog} />
        </div>
      </div>
    </>
  );
}
