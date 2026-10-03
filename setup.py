import os

package_json = '''{
  "name": "workbench-clone",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "dependencies": {
    "electron": "^30.0.0"
  }
}'''

main_js = '''const { app, BrowserWindow } = require('electron');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    title: "Electronics Workbench",
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  
  win.setMenuBarVisibility(false);
  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
'''

index_html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Electronics Workbench</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #d4d0c8;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }
    /* Title bar simulation for OS if frameless, but we use native frame here. */
    .menu-bar {
      background-color: #d4d0c8;
      padding: 2px 10px;
      font-size: 13px;
      display: flex;
      gap: 15px;
      border-bottom: 1px solid #fff;
      box-shadow: 0 1px 0 #808080;
    }
    .menu-item { cursor: default; }
    .menu-item:hover { background-color: #0a246a; color: white; }
    
    .tool-bar {
      background-color: #d4d0c8;
      padding: 4px;
      display: flex;
      gap: 4px;
      border-bottom: 1px solid #808080;
      align-items: center;
    }
    .tool-btn {
      width: 24px;
      height: 24px;
      background-color: #d4d0c8;
      border: 1px solid #d4d0c8;
      box-shadow: inset -1px -1px #404040, inset 1px 1px #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: bold;
      cursor: pointer;
    }
    .tool-btn:active {
      box-shadow: inset 1px 1px #404040, inset -1px -1px #fff;
    }
    
    .toolbar-divider {
      width: 2px;
      height: 22px;
      background-color: #808080;
      border-right: 1px solid #fff;
      margin: 0 4px;
    }

    .status-bar {
      background-color: #d4d0c8;
      padding: 2px 10px;
      font-size: 12px;
      border-top: 1px solid #808080;
      box-shadow: inset 0 1px 0 #fff;
    }

    .workspace {
      flex: 1;
      background-color: #808080;
      padding: 2px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    
    .inner-window {
      background-color: #fff;
      flex: 1;
      border: 2px inset #d4d0c8;
      position: relative;
      overflow: hidden;
    }
    
    .inner-title {
      background-color: #000080;
      color: white;
      font-weight: bold;
      font-size: 12px;
      padding: 2px 5px;
      position: absolute;
      top: 0; left: 0; right: 0;
      z-index: 10;
    }
    
    #circuitCanvas {
      width: 100%;
      height: 100%;
      display: block;
      cursor: pointer;
    }
    
    #floating-table {
      position: absolute;
      top: 80px;
      left: 30px;
      font-family: Arial, sans-serif;
      font-size: 14px;
      font-weight: bold;
      pointer-events: none;
      user-select: none;
      z-index: 5;
    }
    
    #floating-table table {
      border-collapse: collapse;
      text-align: center;
    }
    
    #floating-table th, #floating-table td {
      padding: 2px 8px;
    }

    .btn-mode {
      padding: 2px 10px;
      background: #d4d0c8;
      border: 1px solid #fff;
      box-shadow: 1px 1px 0 #404040;
      font-size: 12px;
      cursor: pointer;
      margin-left: 10px;
    }
    .btn-mode:active { box-shadow: inset 1px 1px #404040; }
  </style>
</head>
<body>
  <div class="menu-bar">
    <div class="menu-item">File</div>
    <div class="menu-item">Edit</div>
    <div class="menu-item">Circuit</div>
    <div class="menu-item">Analysis</div>
    <div class="menu-item">Window</div>
    <div class="menu-item">Help</div>
  </div>
  
  <div class="tool-bar">
    <div class="tool-btn">🗎</div>
    <div class="tool-btn">🗁</div>
    <div class="tool-btn">🖫</div>
    <div class="toolbar-divider"></div>
    <div class="tool-btn" style="color: green">▶</div>
    <div class="tool-btn" style="color: red">⏸</div>
    <div class="toolbar-divider"></div>
    <div class="tool-btn">⏚</div>
    <div class="tool-btn">--</div>
    <div class="toolbar-divider"></div>
    <button id="btn-toggle-mode" class="btn-mode">Cambiar a XS3 -> Gray</button>
  </div>
  
  <div class="workspace">
    <div class="inner-window">
      <div id="file-title" class="inner-title">convertidor de codigo gray a xs3 final.ewb</div>
      
      <div id="floating-table">
        <div style="text-align: center; margin-bottom: 15px;">TABLAS DE CONVERSIONES</div>
        <table>
          <thead>
            <tr><th colspan="4" style="padding-bottom:10px;">GRAY</th><th style="padding: 0 20px;">DEC</th><th colspan="4">X S 3</th></tr>
            <tr><th>D</th><th>C</th><th>B</th><th>A</th><th></th><th>W</th><th>X</th><th>Y</th><th>Z</th></tr>
          </thead>
          <tbody>
            <tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr>
            <tr><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr>
            <tr><td>0</td><td>0</td><td>1</td><td>1</td><td>2</td><td>0</td><td>1</td><td>0</td><td>1</td></tr>
            <tr><td>0</td><td>0</td><td>1</td><td>0</td><td>3</td><td>0</td><td>1</td><td>1</td><td>0</td></tr>
            <tr><td>0</td><td>1</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>1</td><td>1</td></tr>
            <tr><td>0</td><td>1</td><td>1</td><td>1</td><td>5</td><td>1</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>0</td><td>1</td><td>0</td><td>1</td><td>6</td><td>1</td><td>0</td><td>0</td><td>1</td></tr>
            <tr><td>0</td><td>1</td><td>0</td><td>0</td><td>7</td><td>1</td><td>0</td><td>1</td><td>0</td></tr>
            <tr><td>1</td><td>1</td><td>0</td><td>0</td><td>8</td><td>1</td><td>0</td><td>1</td><td>1</td></tr>
            <tr><td>1</td><td>1</td><td>0</td><td>1</td><td>9</td><td>1</td><td>1</td><td>0</td><td>0</td></tr>
          </tbody>
        </table>
      </div>

      <canvas id="circuitCanvas"></canvas>
    </div>
  </div>
  
  <div class="status-bar" id="status-bar">
    Ready. Current Decimal Equivalent: 0
  </div>

  <script src="renderer.js"></script>
</body>
</html>'''

renderer_js = '''const canvas = document.getElementById('circuitCanvas');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  draw();
}
window.addEventListener('resize', resize);

let mode = 'gray_to_xs3';
const inputValues = {
  X3: 0, X2: 0, X1: 1, X0: 1,
  G3: 0, G2: 0, G1: 0, G0: 0
};

// Shifting coordinates right to make room for the table (table is at x=30 to x=350)
const offsetX = 400;

const circuits = {
  xs3_to_gray: {
    inputs: [
      { id: 'X3', label: 'W (X3)', x: offsetX, y: 150 },
      { id: 'X2', label: 'X (X2)', x: offsetX, y: 250 },
      { id: 'X1', label: 'Y (X1)', x: offsetX, y: 350 },
      { id: 'X0', label: 'Z (X0)', x: offsetX, y: 450 },
    ],
    gates: [
      { id: 'g1', type: 'AND', x: offsetX + 150, y: 400, in: ['X1', 'X0'] },
      { id: 'g2', type: 'OR', x: offsetX + 300, y: 300, in: ['X2', 'g1'] },
      { id: 'g3', type: 'XOR', x: offsetX + 300, y: 200, in: ['X2', 'g1'] },
      { id: 'g4', type: 'NOT', x: offsetX + 400, y: 200, in: ['g3'] },
      { id: 'g5', type: 'XOR', x: offsetX + 400, y: 150, in: ['X3', 'g2'] },
      { id: 'g6', type: 'NOT', x: offsetX + 500, y: 150, in: ['g5'] },
      { id: 'g7', type: 'XOR', x: offsetX + 150, y: 500, in: ['X1', 'X0'] },
      { id: 'g8', type: 'XOR', x: offsetX + 600, y: 250, in: ['g6', 'g4'] },
      { id: 'g9', type: 'XOR', x: offsetX + 600, y: 350, in: ['g4', 'g7'] },
      { id: 'g10', type: 'NOT', x: offsetX + 600, y: 450, in: ['X1'] }
    ],
    outputs: [
      { id: 'G3', label: 'D (G3)', x: offsetX + 700, y: 150, in: 'g6' },
      { id: 'G2', label: 'C (G2)', x: offsetX + 700, y: 250, in: 'g8' },
      { id: 'G1', label: 'B (G1)', x: offsetX + 700, y: 350, in: 'g9' },
      { id: 'G0', label: 'A (G0)', x: offsetX + 700, y: 450, in: 'g10' }
    ]
  },
  gray_to_xs3: {
    inputs: [
      { id: 'G3', label: 'D (G3)', x: offsetX, y: 150 },
      { id: 'G2', label: 'C (G2)', x: offsetX, y: 250 },
      { id: 'G1', label: 'B (G1)', x: offsetX, y: 350 },
      { id: 'G0', label: 'A (G0)', x: offsetX, y: 450 },
    ],
    gates: [
      { id: 'b2', type: 'XOR', x: offsetX + 150, y: 200, in: ['G3', 'G2'] },
      { id: 'b1', type: 'XOR', x: offsetX + 250, y: 300, in: ['b2', 'G1'] },
      { id: 'b0', type: 'XOR', x: offsetX + 350, y: 400, in: ['b1', 'G0'] },
      { id: 'x0', type: 'NOT', x: offsetX + 600, y: 450, in: ['b0'] },
      { id: 'x1_xor', type: 'XOR', x: offsetX + 500, y: 350, in: ['b1', 'b0'] },
      { id: 'x1', type: 'NOT', x: offsetX + 600, y: 350, in: ['x1_xor'] },
      { id: 'b1_or_b0', type: 'OR', x: offsetX + 500, y: 250, in: ['b1', 'b0'] },
      { id: 'x2', type: 'XOR', x: offsetX + 600, y: 250, in: ['b2', 'b1_or_b0'] },
      { id: 'and1', type: 'AND', x: offsetX + 500, y: 150, in: ['b2', 'b1_or_b0'] },
      { id: 'x3', type: 'XOR', x: offsetX + 600, y: 150, in: ['G3', 'and1'] }
    ],
    outputs: [
      { id: 'X3', label: 'W (X3)', x: offsetX + 700, y: 150, in: 'x3' },
      { id: 'X2', label: 'X (X2)', x: offsetX + 700, y: 250, in: 'x2' },
      { id: 'X1', label: 'Y (X1)', x: offsetX + 700, y: 350, in: 'x1' },
      { id: 'X0', label: 'Z (X0)', x: offsetX + 700, y: 450, in: 'x0' }
    ]
  }
};

function evaluate() {
  const c = circuits[mode];
  const vals = { ...inputValues };
  c.gates.forEach(g => {
    const inVals = g.in.map(id => vals[id]);
    if (g.type === 'AND') vals[g.id] = inVals[0] & inVals[1];
    else if (g.type === 'OR') vals[g.id] = inVals[0] | inVals[1];
    else if (g.type === 'XOR') vals[g.id] = inVals[0] ^ inVals[1];
    else if (g.type === 'NOT') vals[g.id] = inVals[0] ? 0 : 1;
  });
  c.outputs.forEach(o => vals[o.id] = vals[o.in]);
  return vals;
}

function getOutPos(c, id) {
  let node = c.inputs.find(i => i.id === id);
  if (node) return {x: node.x + 14, y: node.y};
  node = c.gates.find(g => g.id === id);
  if (node) return {x: node.x + 15, y: node.y};
  return {x: 0, y: 0};
}

function getGateInputX(g) {
  if (g.type === 'AND' || g.type === 'NOT') return g.x - 15;
  if (g.type === 'OR') return g.x - 20;
  if (g.type === 'XOR') return g.x - 25;
}

function drawWire(ctx, startX, startY, endX, endY, val, offsetIdx) {
  // Multisim uses solid lines, pink for HIGH and black/blue for LOW.
  // In the user's screenshot: pink for HIGH, black/blue for LOW.
  ctx.strokeStyle = val ? '#ff00ff' : '#000000';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(startX, startY);
  const midX = startX + 15 + (offsetIdx % 15) * 4; 
  ctx.lineTo(midX, startY);
  ctx.lineTo(midX, endY);
  ctx.lineTo(endX, endY);
  ctx.stroke();
  
  // Connection dot if starting point is not an input
  if (offsetIdx > -1) {
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(startX, startY, 2, 0, 2*Math.PI);
    ctx.fill();
  }
}

function drawGate(ctx, gate) {
  ctx.strokeStyle = '#000';
  ctx.fillStyle = '#fff';
  ctx.lineWidth = 1.5;
  const {x, y, type} = gate;
  
  if (type === 'AND') {
    ctx.beginPath();
    ctx.moveTo(x - 15, y - 15); ctx.lineTo(x, y - 15);
    ctx.arc(x, y, 15, -Math.PI/2, Math.PI/2);
    ctx.lineTo(x - 15, y + 15); ctx.closePath();
    ctx.fill(); ctx.stroke();
  } else if (type === 'OR') {
    ctx.beginPath();
    ctx.moveTo(x - 20, y - 15); ctx.quadraticCurveTo(x - 10, y, x - 20, y + 15);
    ctx.quadraticCurveTo(x + 5, y + 15, x + 15, y); ctx.quadraticCurveTo(x + 5, y - 15, x - 20, y - 15);
    ctx.fill(); ctx.stroke();
  } else if (type === 'XOR') {
    ctx.beginPath();
    ctx.moveTo(x - 25, y - 15); ctx.quadraticCurveTo(x - 15, y, x - 25, y + 15); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x - 20, y - 15); ctx.quadraticCurveTo(x - 10, y, x - 20, y + 15);
    ctx.quadraticCurveTo(x + 5, y + 15, x + 15, y); ctx.quadraticCurveTo(x + 5, y - 15, x - 20, y - 15);
    ctx.fill(); ctx.stroke();
  } else if (type === 'NOT') {
    ctx.beginPath();
    ctx.moveTo(x - 15, y - 10); ctx.lineTo(x + 5, y); ctx.lineTo(x - 15, y + 10); ctx.closePath();
    ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.arc(x + 10, y, 5, 0, 2*Math.PI); ctx.fill(); ctx.stroke();
  }
}

function draw() {
  const c = circuits[mode];
  const vals = evaluate();
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw table highlight based on current value
  // We'll update the status bar for validation instead of messing with HTML
  let currentDec = 0;
  if (mode === 'xs3_to_gray') {
    const val = (vals.X3<<3) | (vals.X2<<2) | (vals.X1<<1) | vals.X0;
    currentDec = val - 3;
  } else {
    const b3 = vals.G3, b2 = b3 ^ vals.G2, b1 = b2 ^ vals.G1, b0 = b1 ^ vals.G0;
    currentDec = (b3<<3) | (b2<<2) | (b1<<1) | b0;
  }
  
  let validStr = (currentDec >= 0 && currentDec <= 9) ? \Valido. Entrada coincide con tabla.\ : \¡Fuera de rango! (No definido en tabla)\;
  document.getElementById('status-bar').innerText = \Modo: \ | Equivalencia Decimal: \ | \\;
  
  ctx.font = '12px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  let wireIdx = 0;
  // Wires
  c.gates.forEach(g => {
    g.in.forEach((inId, idx) => {
      const outPos = getOutPos(c, inId);
      const targetY = g.in.length > 1 ? (idx === 0 ? g.y - 6 : g.y + 6) : g.y;
      drawWire(ctx, outPos.x, outPos.y, getGateInputX(g), targetY, vals[inId], wireIdx++);
    });
  });
  
  c.outputs.forEach(o => {
    const outPos = getOutPos(c, o.in);
    drawWire(ctx, outPos.x, outPos.y, o.x - 20, o.y, vals[o.in], wireIdx++);
  });

  // Gates
  c.gates.forEach(g => drawGate(ctx, g));
  
  // Inputs (Switch representation)
  c.inputs.forEach(i => {
    const val = vals[i.id];
    // Draw small switch
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.fillRect(i.x - 10, i.y - 10, 20, 20);
    ctx.strokeRect(i.x - 10, i.y - 10, 20, 20);
    // Draw switch toggle
    ctx.fillStyle = val ? '#ff00ff' : '#000';
    ctx.beginPath(); ctx.arc(i.x, val ? i.y - 5 : i.y + 5, 4, 0, 2*Math.PI); ctx.fill();
    
    ctx.fillStyle = '#000';
    ctx.fillText(i.label, i.x - 25, i.y);
  });
  
  // Outputs (LED representation)
  c.outputs.forEach(o => {
    const val = vals[o.id];
    ctx.fillStyle = val ? '#ff0000' : '#888'; 
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(o.x, o.y, 10, 0, 2*Math.PI); ctx.fill(); ctx.stroke();
    
    // Wire connection to ground (simplified)
    ctx.beginPath(); ctx.moveTo(o.x, o.y + 10); ctx.lineTo(o.x, o.y + 20); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(o.x - 5, o.y + 20); ctx.lineTo(o.x + 5, o.y + 20); ctx.stroke();
    
    ctx.fillStyle = '#000';
    ctx.fillText(o.label, o.x + 25, o.y - 15);
  });
}

document.getElementById('btn-toggle-mode').addEventListener('click', (e) => {
  if (mode === 'gray_to_xs3') {
    mode = 'xs3_to_gray';
    e.target.innerText = 'Cambiar a Gray -> XS3';
    document.getElementById('file-title').innerText = 'convertidor de codigo xs3 a gray final.ewb';
    inputValues.X3 = 0; inputValues.X2 = 0; inputValues.X1 = 1; inputValues.X0 = 1; // Dec 0
  } else {
    mode = 'gray_to_xs3';
    e.target.innerText = 'Cambiar a XS3 -> Gray';
    document.getElementById('file-title').innerText = 'convertidor de codigo gray a xs3 final.ewb';
    inputValues.G3 = 0; inputValues.G2 = 0; inputValues.G1 = 0; inputValues.G0 = 0; // Dec 0
  }
  draw();
});

canvas.addEventListener('click', (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  const c = circuits[mode];
  c.inputs.forEach(i => {
    // Click area for the switch box
    if (x > i.x - 15 && x < i.x + 15 && y > i.y - 15 && y < i.y + 15) {
      inputValues[i.id] = inputValues[i.id] ? 0 : 1;
      draw();
    }
  });
});

setTimeout(() => {
  resize();
}, 100);
'''

with open('package.json', 'w', encoding='utf-8') as f:
    f.write(package_json)
with open('main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
with open('renderer.js', 'w', encoding='utf-8') as f:
    f.write(renderer_js)
