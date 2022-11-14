import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('api', {
  getContext: async () => ipcRenderer.invoke('getContext'),
  getWindows: async () => ipcRenderer.invoke('getWindows'),
  setContext: async (newContext) =>
    ipcRenderer.invoke('setContext', newContext),
});
