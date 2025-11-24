import { useEffect, useRef } from "react";
import CloseButtons from "./CloseButtons";

interface HeaderProps {
  code: string;
  onChangeCode: (value: string) => void;
  setConsoleLog: (value: string) => void;
  currentFilePath?: string | null;
  setCurrentFilePath: (path: string | null) => void;
}

const Header: React.FC<HeaderProps> = ({ code, onChangeCode, setConsoleLog, currentFilePath, setCurrentFilePath }) => {
  const header = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!window.electron) return;
    const unsubscribe = window.electron.onToggleTitlebar((show: boolean) => {
      if (show) {
        header.current?.classList.remove("hidden");
      } else {
        header.current?.classList.add("hidden");
      }
    });
    return unsubscribe;
  }, []);

  const handleOpen = async () => {
    try {
      const res = await (window.api as any).openFile?.();
      if (res && !res.canceled && typeof res.content === "string") {
        onChangeCode(res.content);
        setCurrentFilePath(res.filePath || null);
        setConsoleLog(res.filePath ? `Opened ${res.filePath}` : "File opened");
      } else {
        setConsoleLog("Open cancelled");
      }
    } catch (e) {
      setConsoleLog("Failed to open file");
    }
  };

  const handleSave = async () => {
    try {
      let res;
      if (currentFilePath) {
        // overwrite last-opened file without prompting
        res = await (window.api as any).saveFile?.({ content: code, defaultPath: currentFilePath });
      } else {
        // no known path — behave like Save As
        res = await (window.api as any).saveFile?.({ content: code });
      }
      if (res && !res.canceled && res.filePath) {
        setCurrentFilePath(res.filePath);
        setConsoleLog(`Saved ${res.filePath}`);
      } else {
        setConsoleLog("Save cancelled");
      }
    } catch (e) {
      setConsoleLog("Failed to save file");
    }
  };

  const handleSaveAs = async () => {
    try {
      const res = await (window.api as any).saveFile?.({ content: code });
      if (res && !res.canceled && res.filePath) {
        setCurrentFilePath(res.filePath);
        setConsoleLog(`Saved ${res.filePath}`);
      } else {
        setConsoleLog("Save As cancelled");
      }
    } catch (e) {
      setConsoleLog("Failed to Save As file");
    }
  };

  return (
    <nav ref={header} className="h-9 dark:bg-main-dark bg-[#f7f7f7] z-10 drag p-1">
      <div className="flex items-center justify-between h-full px-2">
        <div className="flex items-center gap-2 no-drag">
          <button onClick={handleOpen} className="tileStyleButton no-drag" title="Open .lrl file">
            Open
          </button>
          <button onClick={handleSave} className="tileStyleButton no-drag" title="Save .lrl file">
            Save
          </button>
          <button onClick={handleSaveAs} className="tileStyleButton no-drag" title="Save As .lrl file">
            Save As
          </button>
        </div>

        <div className="no-drag">
          {window.electron && <CloseButtons />}
        </div>
      </div>
    </nav>
  );
};

export default Header;
