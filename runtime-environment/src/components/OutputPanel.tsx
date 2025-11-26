import idleImg from "../assets/idle-laurel.png";
import outputImg from "../assets/output-laurel.png";
import inputImg from "../assets/input-laurel.png";
import errorImg from "../assets/error-laurel.png";

interface OutputPanelProps {
  output: string;
  awaitingInput?: boolean;
  isRunning?: boolean;
  isError?: boolean;

  inputState?: { prompt: string; type: string } | null;
  inputValue?: string;
  setInputValue?: (v: string) => void;
  onSubmitInput?: () => void;
  awaitingSayOutput?: boolean;
  onContinueSayOutput?: () => void;
}

const OutputPanel: React.FC<OutputPanelProps> = ({
  output,
  awaitingInput,
  isError,
  inputState,
  inputValue = "",
  setInputValue = () => {},
  onSubmitInput = () => {},
  awaitingSayOutput = false,
  onContinueSayOutput = () => {},
}) => {
  console.log("OutputPanel rendered with awaitingSayOutput:", awaitingSayOutput);
const getCharacterSprite = () => {
  if (isError) return errorImg;
  if (awaitingInput) return inputImg;
  if (output && !isError && !awaitingInput) return outputImg;
  return idleImg;
};

  return (
    <div className="flex-1 p-3 bg-gray-900 flex flex-col relative overflow-hidden">
      <h3 className="text-xl font-semibold text-gray-300 uppercase tracking-wide mb-2">
        Output
      </h3>

      <div className="flex-1 relative flex flex-col items-center justify-end">


        {/* Input field */}
        {awaitingInput && inputState && (
          <form
            className="flex flex-col gap-2 bg-gray-850 p-3 rounded-md mb-4 z-30 w-[90%]"
            onSubmit={(e) => {
              e.preventDefault();
              onSubmitInput();
            }}
          >
            <input
              className="bg-gray-800 text-gray-100 p-2 rounded-md focus:outline-none"
              value={inputValue}
              autoFocus
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={inputState.prompt}
            />

            <button
              type="submit"
              className="self-end px-4 py-1 rounded bg-blue-600 hover:bg-blue-500 transition"
              disabled={inputValue.length === 0 && inputState.type !== "string"}
            >
              Submit
            </button>
          </form>
        )}

        {/* Continue button for say() output */}
        {awaitingSayOutput && (
          <button
            onClick={onContinueSayOutput}
            className="px-6 py-2 rounded bg-green-600 hover:bg-green-500 transition text-white font-semibold mb-4 z-30"
          >
            Continue
          </button>
        )}

{/* Speech bubble (hidden on error) */}
{!isError && (
  <div className="relative bg-gray-800 text-gray-100 px-6 py-5 rounded-2xl max-w-[90%] break-words shadow-xl z-20 mb-4">
    {/* Bubble tail — always centered */}
    <div className="absolute -bottom-3 left-1/2 -translate-x-1/2 w-6 h-6 bg-gray-800 rotate-45" />

    {/* Bubble content */}
    {awaitingInput && inputState ? (
      <div className="flex flex-col gap-2">
        <span className="text-yellow-300 font-semibold">{inputState.prompt}</span>
      </div>
    ) : output ? (
      <span className="text-lg">{output}</span>
    ) : (
      <span className="text-gray-500 italic text-lg">Lets get coding!</span>
    )}
  </div>
)}

        {/* Character at bottom */}
        <img
          src={getCharacterSprite()}
          alt="Laurel character"
          className="w-64 h-64 object-contain select-none pointer-events-none z-10 mb-2"
        />

        {awaitingInput && (
          <div className="text-base text-yellow-400 italic font-semibold mb-2">
            Waiting for your input...
          </div>
        )}
      </div>
    </div>
  );
};

export default OutputPanel;
