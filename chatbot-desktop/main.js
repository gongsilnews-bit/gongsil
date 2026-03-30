const { app, BrowserWindow, shell, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 380,
    height: 650,
    minWidth: 320,
    minHeight: 500,
    x: 1540, // 1920 기본 모니터 해상도 기준 우측 하단 쯤 배치 (조절 가능)
    y: 100,
    alwaysOnTop: true, // 바탕화면, 엑셀, 카카오톡 등 모든 창 위에 고정 (가장 중요한 부분!)
    frame: false,      // 못생긴 기본 윈도우 창 테두리 끄기 (자체 제작한 예쁜 헤더 사용)
    transparent: true, // 뒤쪽 배경 살짝 보이는 투명 처리 허용
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // 라이브 배포된 깃허브 버전을로드해서 항상 최신 서버 동기화!
  win.loadURL('https://gongsilnews-bit.github.io/gongsil/standalone_chatbot.html');

  // 내부에서 사용자가 누르는 모든 '외부 링크'는 새 창에서 뜨도록 우회
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 화면 최소화 및 닫기 연동 신호 처리
ipcMain.on('window-controls', (event, command) => {
    const win = BrowserWindow.getFocusedWindow();
    if(!win) return;
    
    if (command === 'close') win.close();
    if (command === 'minimize') win.minimize();
});
