export {};
import type { ElectronApi, LaurelApi } from "../main/preload";

declare global {
  interface Window {
    electron: ElectronApi;
    api: LaurelApi;
  }
}