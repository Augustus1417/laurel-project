import { app, BrowserWindow, ipcMain, dialog } from "electron";
import fs from "fs/promises";
import serve from "electron-serve";
import path, { join } from "path";
import { spawn } from "child_process";

import { getURL } from "./lib/getUrl";
import isDev from "./lib/isDev";

if (!isDev) {
  serve({ directory: join(__dirname, "renderer"), hostname: "example" });
}

const CODE_END_MARKER = "__LAUREL_END_OF_CODE__";
const INPUT_REQUEST_PREFIX = "INPUT_REQUEST:";

let win: BrowserWindow;
let pythonProcess: ReturnType<typeof spawn> | null = null;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 800,
    minHeight: 600,
    titleBarStyle: "hidden",
    icon: path.join(__dirname, "renderer", "icon.png"),
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: true,
      contextIsolation: true,
      webSecurity: false,
      allowRunningInsecureContent: true,
    },
  });

  win.on("enter-full-screen", () => {
    win.webContents.send("toggle-titlebar", false);
  });

  win.on("leave-full-screen", () => {
    win.webContents.send("toggle-titlebar", true);
  });

  const url = getURL("/");
  win.loadURL(url);
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

ipcMain.on("app/minimize", () => {
  win.minimize();
});

ipcMain.on("app/maximize", () => {
  if (!win.isMaximized()) {
    win.maximize();
  } else {
    win.unmaximize();
  }
});

ipcMain.on("app/close", () => {
  app.quit();
});

ipcMain.handle("laurel:run", async (_event, code: string) => {
  if (pythonProcess) {
    pythonProcess.stdout?.removeAllListeners();
    pythonProcess.stderr?.removeAllListeners();
    pythonProcess.removeAllListeners();
    pythonProcess.kill();
    pythonProcess = null;
  }

  return new Promise<string>((resolve, reject) => {
    const interpreterPath = path.join(__dirname, "..", "interpreter", "laurel_interpreter.py");
    pythonProcess = spawn("python3", [interpreterPath], { stdio: "pipe" });

    let output = "";
    let stderrBuffer = "";
    let stdoutBuffer = "";
    let settled = false;

    const finalize = (err?: string | Error) => {
      if (settled) return;
      settled = true;
      if (pythonProcess) {
        pythonProcess.stdout?.removeAllListeners();
        pythonProcess.stderr?.removeAllListeners();
        pythonProcess.removeAllListeners();
        pythonProcess = null;
      }
      if (err) {
        const message = typeof err === "string" ? err : err.message;
        reject(new Error(message));
      } else {
        resolve(output);
      }
    };

    const flushStdout = () => {
      if (stdoutBuffer.length > 0) {
        output += stdoutBuffer;
        stdoutBuffer = "";
      }
    };

    const stdout = pythonProcess.stdout;
    const stderr = pythonProcess.stderr;
    const stdin = pythonProcess.stdin;

    if (!stdout || !stderr || !stdin) {
      finalize("Python process streams unavailable");
      return;
    }

    stdout.on("data", (data: Buffer) => {
      stdoutBuffer += data.toString();

      let newlineIndex = stdoutBuffer.indexOf("\n");
      while (newlineIndex !== -1) {
        const rawLine = stdoutBuffer.slice(0, newlineIndex);
        stdoutBuffer = stdoutBuffer.slice(newlineIndex + 1);
        const line = rawLine.replace(/\r$/, "");

        if (line.startsWith(INPUT_REQUEST_PREFIX)) {
          const payload = line.slice(INPUT_REQUEST_PREFIX.length);
          const [type = "string", ...rest] = payload.split(":");
          const prompt = rest.join(":");
          _event.sender.send("laurel:input", { type, prompt });
        } else {
          output += line + "\n";
        }

        newlineIndex = stdoutBuffer.indexOf("\n");
      }
    });

    stderr.on("data", (data: Buffer) => {
      stderrBuffer += data.toString();
    });

    pythonProcess.on("error", (procError) => {
      finalize(procError);
    });

    pythonProcess.on("close", () => {
      flushStdout();
      if (stderrBuffer.trim().length > 0) {
        finalize(stderrBuffer.trim());
      } else {
        finalize();
      }
    });

    const normalizedCode = code.endsWith("\n") ? code : `${code}\n`;
    stdin.write(normalizedCode);
    stdin.write(`${CODE_END_MARKER}\n`);
  });
});

ipcMain.on("laurel:send-input", (_event, value: string) => {
  if (
    pythonProcess &&
    !pythonProcess.killed &&
    pythonProcess.stdin &&
    !pythonProcess.stdin.destroyed
  ) {
    pythonProcess.stdin.write(`${value}\n`);
  }
});

// Allow renderer to request an immediate stop of the running interpreter
ipcMain.on("laurel:stop", () => {
  if (pythonProcess) {
    try {
      pythonProcess.stdout?.removeAllListeners();
      pythonProcess.stderr?.removeAllListeners();
      pythonProcess.removeAllListeners();
      pythonProcess.kill();
    } catch (e) {
      // ignore
    }
    pythonProcess = null;
  }
  // Notify renderer that we've processed the stop request
  try {
    win?.webContents?.send("laurel:stopped");
  } catch (e) {
    // ignore
  }
});

// Open a .lrl file and return its content
ipcMain.handle("file:open", async () => {
  if (!win) return { canceled: true };
  const res = await dialog.showOpenDialog(win, {
    title: "Open Laurel file",
    properties: ["openFile"],
    filters: [{ name: "Laurel", extensions: ["lrl"] }],
  });
  if (res.canceled || !res.filePaths || res.filePaths.length === 0) return { canceled: true };
  const filePath = res.filePaths[0];
  const content = await fs.readFile(filePath, "utf8");
  return { canceled: false, filePath, content };
});

// Save content to a .lrl file. If defaultPath provided it's used, otherwise ask user.
ipcMain.handle("file:save", async (_event, { content, defaultPath }: { content: string; defaultPath?: string }) => {
  if (!win) return { canceled: true };
  let filePath = defaultPath;
  if (!filePath) {
    const res = await dialog.showSaveDialog(win, {
      title: "Save Laurel file",
      defaultPath: defaultPath || "untitled.lrl",
      filters: [{ name: "Laurel", extensions: ["lrl"] }],
    });
    if (res.canceled || !res.filePath) return { canceled: true };
    filePath = res.filePath;
  }
  await fs.writeFile(filePath, content, "utf8");
  return { canceled: false, filePath };
});