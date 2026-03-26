function openFolder(type) {
    const desktop = document.getElementById('desktop');
    const win = document.createElement('fos-window');
    
    if (type === 'projects') {
        win.setAttribute('title', 'C:\\Borf\\Projects');
        win.innerHTML = `
            <div class="folder-grid">
                <div class="exe-item" onclick="launchApp('https://borfwashere.github.io/matrix/', 'Matrix.exe')">
                    <img src="https://win98icons.alexmeub.com/icons/png/world-3.png">
                    <p>Matrix.exe</p>
                </div>
                <div class="exe-item" onclick="launchApp('https://borfwashere.github.io/matrix/gifsweeper.html', 'Sweeper.exe')">
                    <img src="https://win98icons.alexmeub.com/icons/png/game_minesweeper-0.png">
                    <p>Sweeper.exe</p>
                </div>
                </div>
        `;
    } else if (type === 'system') {
        win.setAttribute('title', 'System Info');
        win.innerHTML = `<div style="padding:20px; background:white; height:100%;">
            <h3>Root Directory:</h3>
            <ul>
                <li>01_Engine_Core</li>
                <li>02_Frameworks_Render</li>
                <li>03_Desktop_Shell</li>
            </ul>
        </div>`;
    }

    desktop.appendChild(win);
}

function launchApp(url, name) {
    const desktop = document.getElementById('desktop');
    const win = document.createElement('fos-window');
    win.setAttribute('title', name);
    win.style.width = "80%";
    win.style.height = "80%";
    win.innerHTML = `<iframe src="${url}" style="width:100%; height:100%; border:none;"></iframe>`;
    desktop.appendChild(win);
}

// Reloj
setInterval(() => {
    document.getElementById('clock').innerText = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}, 1000);
