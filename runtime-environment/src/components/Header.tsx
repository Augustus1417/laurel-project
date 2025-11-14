import { useEffect, useRef } from "react";
import CloseButtons from "./CloseButtons";

const Header = () => {
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

  return (
    <nav ref={header} className="h-9 dark:bg-main-dark bg-[#f7f7f7] z-10 drag p-1">
      {window.electron && <CloseButtons />}
    </nav>
  );
};

export default Header;
