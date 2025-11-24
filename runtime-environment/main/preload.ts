import { contextBridge, ipcRenderer, IpcRendererEvent } from "electron";

export type LaurelInputPayload = {
  type: string;
  prompt: string;
};

const electronApi = {
  getVersion: () => ipcRenderer.sendSync("app/version"),
  maximize: () => ipcRenderer.send("app/maximize"),
  minimize: () => ipcRenderer.send("app/minimize"),
  onToggleTitlebar: (callback: (show: boolean) => void) => {
    const listener = (_event: IpcRendererEvent, show: boolean) => callback(show);
    ipcRenderer.on("toggle-titlebar", listener);
    return () => {
      ipcRenderer.removeListener("toggle-titlebar", listener);
    };
  },
  close: () => ipcRenderer.send("app/close"),
  onLaurelInput: (callback: (payload: LaurelInputPayload) => void) => {
    const listener = (_event: IpcRendererEvent, payload: LaurelInputPayload) => {
      callback(payload);
    };
    ipcRenderer.on("laurel:input", listener);
    return () => {
      ipcRenderer.removeListener("laurel:input", listener);
    };
  },
  sendLaurelInput: (value: string) => {
    ipcRenderer.send("laurel:send-input", value);
  },
};

const laurelApi = {
  runLaurel: (code: string) => ipcRenderer.invoke("laurel:run", code),
  stopLaurel: () => ipcRenderer.send("laurel:stop"),
  openFile: () => ipcRenderer.invoke("file:open"),
  saveFile: (opts: { content: string; defaultPath?: string }) => ipcRenderer.invoke("file:save", opts),
};

contextBridge.exposeInMainWorld("electron", electronApi);
contextBridge.exposeInMainWorld("api", laurelApi);

export type ElectronApi = typeof electronApi;
export type LaurelApi = typeof laurelApi;
