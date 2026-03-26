// Desactivar menú contextual para mantener la estética
document.addEventListener('contextmenu', e => e.preventDefault());

function openFolder(type) {
    const desktop = document.getElementById('desktop');
    const win = document.createElement('fos-window');
    
    if (type === 'projects') {
        win.setAttribute('title', 'C:\\Borf\\Projects');
        win.setAttribute('name', 'projects_win');
        win.innerHTML = `
            <div class="folder-grid">
                <div class="exe-item" onclick="launchApp('https://borfwashere.github.io/matrix/', 'Matrix.exe')">
                    <img src="https://win98icons.alexmeub.com/icons/png/world-3.png" style="filter: sepia(1) hue-rotate(80deg);">
                    <p>Matrix.exe</p>
                </div>
                <div class="exe-item" onclick="launchApp('https://borfwashere.github.io/matrix/gifsweeper.html', 'Sweeper.exe')">
                    <img src="https://win98icons.alexmeub.com/icons/png/game_minesweeper-0.png">
                    <p>Sweeper.exe</p>
                </div>
            </div>
        `;
    } else if (type === 'system') {
        win.setAttribute('title', 'System Information');
        win.setAttribute('name', 'sys_win');
        win.innerHTML = `
            <div style="padding:20px; background:#fff; height:100%; font-size:12px;">
                <h3 style="margin-top:0;">Borsec Station v1.0</h3>
                <hr>
                <p><strong>Root Structure:</strong></p>
                <ul>
                    <li>01_Engine_Core</li>
                    <li>02_Frameworks_Render</li>
                    <li>03_Desktop_Shell</li>
                    <li>04_Machine_Learning</li>
                </ul>
                <p>User: Francisco Borsec</p>
            </div>
        `;
    }

    desktop.appendChild(win);
}

function launchApp(url, name) {
    const desktop = document.getElementById('desktop');
    const win = document.createElement('fos-window');
    
    win.setAttribute('title', name);
    win.setAttribute('name', name.toLowerCase().replace('.', '_'));
    
    // Configuración de tamaño para apps
    win.style.width = "1000px";
    win.style.height = "750px";
    win.style.top = "50px";
    win.style.left = "50px";

    win.innerHTML = `<iframe src="${url}" style="width:100%; height:100%; border:none; background:#000;"></iframe>`;
    
    desktop.appendChild(win);
}

// Reloj en tiempo real
setInterval(() => {
    const now = new Date();
    const clock = document.getElementById('clock');
    if(clock) {
        clock.innerText = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
}, 1000);
