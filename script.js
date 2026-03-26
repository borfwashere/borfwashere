document.addEventListener('contextmenu', e => e.preventDefault());

function openFolder(type) {
    const desktop = document.getElementById('desktop');
    const win = document.createElement('fos-window');
    
    if (type === 'system') {
        win.setAttribute('title', 'My Computer');
        win.setAttribute('name', 'my_computer');
        win.style.width = "600px";
        win.style.height = "400px";
        
        // Aquí plasmamos tu estructura de carpetas real
        win.innerHTML = `
            <div class="folder-grid">
                <div class="item" onclick="openSubFolder('engine')">
                    <img src="https://win98icons.alexmeub.com/icons/png/directory_closed-4.png">
                    <p>01_Engine_Core</p>
                </div>
                <div class="item">
                    <img src="https://win98icons.alexmeub.com/icons/png/directory_closed-4.png">
                    <p>02_Frameworks_Render</p>
                </div>
                <div class="item">
                    <img src="https://win98icons.alexmeub.com/icons/png/directory_closed-4.png">
                    <p>03_Desktop_Shell</p>
                </div>
                <div class="item">
                    <img src="https://win98icons.alexmeub.com/icons/png/directory_closed-4.png">
                    <p>04_Machine_Learning</p>
                </div>
            </div>
        `;
    } else if (type === 'readme') {
        win.setAttribute('title', 'About Borsec OS');
        win.innerHTML = `<div style="padding:20px; background:#fff; height:100%; font-size:12px;">
            <h3>Francisco Borsec - Workstation</h3>
            <hr>
            <p>Sistema de gestión de proyectos 3D y visualización.</p>
        </div>`;
    }

    desktop.appendChild(win);
}

// Función para abrir la subcarpeta de Engine Core
function openSubFolder(folder) {
    const desktop = document.getElementById('desktop');
    const win = document.createElement('fos-window');
    
    if (folder === 'engine') {
        win.setAttribute('title', 'C:\\01_Engine_Core');
        win.style.width = "500px";
        win.style.height = "300px";
        win.innerHTML = `
            <div class="folder-grid">
                <div class="item" onclick="launchApp('https://borfwashere.github.io/matrix/', 'Matrix.exe')">
                    <img src="https://win98icons.alexmeub.com/icons/png/world-3.png" style="filter: sepia(1) hue-rotate(80deg);">
                    <p>Matrix.exe</p>
                </div>
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
    win.style.width = "90%";
    win.style.height = "85%";
    win.style.top = "5%";
    win.style.left = "5%";

    win.innerHTML = `<iframe src="${url}" style="width:100%; height:100%; border:none; background:#000;"></iframe>`;
    
    desktop.appendChild(win);
}

// Reloj
setInterval(() => {
    const now = new Date();
    const clock = document.getElementById('clock');
    if(clock) clock.innerText = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}, 1000);
