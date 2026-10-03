const canvas = document.getElementById('circuitCanvas');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  draw();
}
window.addEventListener('resize', resize);

let mode = 'gray_to_xs3';
let powerOn = false; // Starts off like real workbench
const inputValues = {
  D: 0, C: 0, B: 0, A: 0
};

const offsetX = 400;

const circuits = {
  xs3_to_gray: {
    inputs: [
      { id: 'D', label: 'D', x: offsetX, y: 150 },
      { id: 'C', label: 'C', x: offsetX, y: 250 },
      { id: 'B', label: 'B', x: offsetX, y: 350 },
      { id: 'A', label: 'A', x: offsetX, y: 450 },
    ],
    gates: [
      { id: 'g1', type: 'AND', x: offsetX + 150, y: 400, in: ['B', 'A'] },
      { id: 'g2', type: 'OR', x: offsetX + 300, y: 300, in: ['C', 'g1'] },
      { id: 'g3', type: 'XOR', x: offsetX + 300, y: 200, in: ['C', 'g1'] },
      { id: 'g4', type: 'NOT', x: offsetX + 400, y: 200, in: ['g3'] },
      { id: 'g5', type: 'XOR', x: offsetX + 400, y: 150, in: ['D', 'g2'] },
      { id: 'g6', type: 'NOT', x: offsetX + 500, y: 150, in: ['g5'] },
      { id: 'g7', type: 'XOR', x: offsetX + 150, y: 500, in: ['B', 'A'] },
      { id: 'g8', type: 'XOR', x: offsetX + 600, y: 250, in: ['g6', 'g4'] },
      { id: 'g9', type: 'XOR', x: offsetX + 600, y: 350, in: ['g4', 'g7'] },
      { id: 'g10', type: 'NOT', x: offsetX + 600, y: 450, in: ['B'] }
    ],
    outputs: [
      { id: 'W', label: 'W', x: offsetX + 700, y: 150, in: 'g6' },
      { id: 'X', label: 'X', x: offsetX + 700, y: 250, in: 'g8' },
      { id: 'Y', label: 'Y', x: offsetX + 700, y: 350, in: 'g9' },
      { id: 'Z', label: 'Z', x: offsetX + 700, y: 450, in: 'g10' }
    ]
  },
  gray_to_xs3: {
    inputs: [
      { id: 'D', label: 'D', x: offsetX, y: 150 },
      { id: 'C', label: 'C', x: offsetX, y: 250 },
      { id: 'B', label: 'B', x: offsetX, y: 350 },
      { id: 'A', label: 'A', x: offsetX, y: 450 },
    ],
    gates: [
      { id: 'b2', type: 'XOR', x: offsetX + 150, y: 200, in: ['D', 'C'] },
      { id: 'b1', type: 'XOR', x: offsetX + 250, y: 300, in: ['b2', 'B'] },
      { id: 'b0', type: 'XOR', x: offsetX + 350, y: 400, in: ['b1', 'A'] },
      { id: 'x0', type: 'NOT', x: offsetX + 600, y: 450, in: ['b0'] },
      { id: 'x1_xor', type: 'XOR', x: offsetX + 500, y: 350, in: ['b1', 'b0'] },
      { id: 'x1', type: 'NOT', x: offsetX + 600, y: 350, in: ['x1_xor'] },
      { id: 'b1_or_b0', type: 'OR', x: offsetX + 500, y: 250, in: ['b1', 'b0'] },
      { id: 'x2', type: 'XOR', x: offsetX + 600, y: 250, in: ['b2', 'b1_or_b0'] },
      { id: 'and1', type: 'AND', x: offsetX + 500, y: 150, in: ['b2', 'b1_or_b0'] },
      { id: 'x3', type: 'XOR', x: offsetX + 600, y: 150, in: ['D', 'and1'] }
    ],
    outputs: [
      { id: 'W', label: 'W', x: offsetX + 700, y: 150, in: 'x3' },
      { id: 'X', label: 'X', x: offsetX + 700, y: 250, in: 'x2' },
      { id: 'Y', label: 'Y', x: offsetX + 700, y: 350, in: 'x1' },
      { id: 'Z', label: 'Z', x: offsetX + 700, y: 450, in: 'x0' }
    ]
  }
};

function evaluate() {
  const c = circuits[mode];
  const vals = { ...inputValues }; // Keep switch state visual for inputs
  
  if (!powerOn) {
    // If power is off, all gates and outputs are dead (0)
    c.gates.forEach(g => vals[g.id] = 0);
    c.outputs.forEach(o => vals[o.id] = 0);
    return vals;
  }
  
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
  ctx.strokeStyle = val && powerOn ? '#ff00ff' : '#000000';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(startX, startY);
  const midX = startX + 15 + (offsetIdx % 15) * 6; 
  ctx.lineTo(midX, startY);
  ctx.lineTo(midX, endY);
  ctx.lineTo(endX, endY);
  ctx.stroke();
  
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
  
  let currentDec = 0;
  if (mode === 'xs3_to_gray') {
    const val = (vals.D<<3) | (vals.C<<2) | (vals.B<<1) | vals.A;
    currentDec = val - 3;
  } else {
    const b3 = vals.D, b2 = b3 ^ vals.C, b1 = b2 ^ vals.B, b0 = b1 ^ vals.A;
    currentDec = (b3<<3) | (b2<<2) | (b1<<1) | b0;
  }
  
  let validStr = (currentDec >= 0 && currentDec <= 9) ? "Valido. Entrada coincide con tabla." : "Fuera de rango! (No definido en tabla)";
  let modeStr = mode === 'xs3_to_gray' ? 'XS3 a Gray' : 'Gray a XS3';
  let powerStr = powerOn ? "(SIMULADOR ENCENDIDO)" : "(SIMULADOR APAGADO - Enciende el switch arriba a la derecha)";
  document.getElementById('status-bar').innerText = "Modo: " + modeStr + " | Equivalencia Decimal: " + currentDec + " | " + validStr + " | " + powerStr;
  
  ctx.font = '12px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  let wireIdx = 0;
  c.gates.forEach(g => {
    g.in.forEach((inId, idx) => {
      const outPos = getOutPos(c, inId);
      const targetY = g.in.length > 1 ? (idx === 0 ? g.y - 6 : g.y + 6) : g.y;
      // Note: for wires starting from inputs, we pass inputValues so they turn pink if on, but wait, the simulation is off so wires should be black!
      // In evaluate(), inputs retain their value so the user sees the switch, but we handled powerOn in drawWire.
      drawWire(ctx, outPos.x, outPos.y, getGateInputX(g), targetY, vals[inId], wireIdx++);
    });
  });
  
  c.outputs.forEach(o => {
    const outPos = getOutPos(c, o.in);
    drawWire(ctx, outPos.x, outPos.y, o.x - 20, o.y, vals[o.in], wireIdx++);
  });

  c.gates.forEach(g => {
    drawGate(ctx, g);
    ctx.font = '10px Arial';
    ctx.fillStyle = '#000';
    ctx.fillText(g.type + ' GATE', g.x, g.y + 25);
  });
  
  c.inputs.forEach(i => {
    // The visual state of the switch is always preserved
    const val = inputValues[i.id];
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.fillRect(i.x - 10, i.y - 10, 20, 20);
    ctx.strokeRect(i.x - 10, i.y - 10, 20, 20);
    ctx.fillStyle = val ? '#ff00ff' : '#000';
    ctx.beginPath(); ctx.arc(i.x, val ? i.y - 5 : i.y + 5, 4, 0, 2*Math.PI); ctx.fill();
    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';
    ctx.fillText(i.label, i.x - 25, i.y);
    ctx.fillStyle = '#888';
    ctx.fillText('[' + i.id + ']', i.x - 45, i.y);
    ctx.font = '10px Arial';
    ctx.fillStyle = '#000';
    ctx.fillText('INPUT', i.x, i.y + 20);
  });
  
  c.outputs.forEach(o => {
    const val = vals[o.id];
    ctx.fillStyle = val && powerOn ? '#ff0000' : '#fff'; 
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(o.x, o.y, 10, 0, 2*Math.PI); ctx.fill(); ctx.stroke();
    
    ctx.beginPath(); ctx.moveTo(o.x, o.y + 10); ctx.lineTo(o.x, o.y + 20); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(o.x - 5, o.y + 20); ctx.lineTo(o.x + 5, o.y + 20); ctx.stroke();
    
    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';
    
    let colorName = val && powerOn ? 'RED' : 'WHITE';
    let ledName = val && powerOn ? 'LED' : 'PROBE';
    ctx.textAlign = 'left';
    ctx.fillText(`${colorName} ${ledName} ${o.label}`, o.x + 20, o.y);
    ctx.textAlign = 'center';
  });

  drawLegendGrid(ctx);
}

function drawLegendGrid(ctx) {
  const startX = 650;
  const startY = 480; // Bottom right area
  const cellH = 20;
  
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(startX, startY, 400, cellH * 5);
  ctx.strokeStyle = '#000';
  ctx.lineWidth = 1;
  ctx.strokeRect(startX, startY, 400, cellH * 5);
  
  ctx.fillStyle = '#000';
  ctx.font = 'bold 11px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('LEYENDA DE COMPONENTES', startX + 200, startY + 14);
  
  ctx.beginPath(); ctx.moveTo(startX, startY + cellH); ctx.lineTo(startX + 400, startY + cellH); ctx.stroke();
  
  // Columns X offsets
  const col1 = startX;
  const col2 = startX + 40;
  const col3 = startX + 80;
  const col4 = startX + 220;
  const col5 = startX + 260;
  const col6 = startX + 310;
  
  const drawRow = (rowIdx, icon1, name1, desc1, icon2, name2, desc2) => {
    const y = startY + cellH * (rowIdx + 1);
    ctx.beginPath(); ctx.moveTo(startX, y); ctx.lineTo(startX + 400, y); ctx.stroke();
    
    // Vertical dividers
    ctx.beginPath();
    ctx.moveTo(col2, startY + cellH); ctx.lineTo(col2, startY + cellH * 5);
    ctx.moveTo(col3, startY + cellH); ctx.lineTo(col3, startY + cellH * 5);
    ctx.moveTo(col4, startY + cellH); ctx.lineTo(col4, startY + cellH * 5);
    ctx.moveTo(col5, startY + cellH); ctx.lineTo(col5, startY + cellH * 5);
    ctx.moveTo(col6, startY + cellH); ctx.lineTo(col6, startY + cellH * 4); // Only to row 3 for the second column
    ctx.stroke();

    ctx.textAlign = 'left';
    ctx.font = '11px Arial';
    ctx.fillStyle = '#000';
    
    // Draw Col 1
    if (name1) {
      if (icon1 === 'XOR' || icon1 === 'AND' || icon1 === 'OR' || icon1 === 'NOT') {
        drawGate(ctx, { x: col1 + 25, y: y + 10, type: icon1 });
      }
      ctx.fillText(name1, col2 + 5, y + 14);
      ctx.fillText(desc1, col3 + 5, y + 14);
    }
    
    // Draw Col 2
    if (name2) {
      if (icon2 === 'PROBE') {
        ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(col4 + 20, y + 10, 6, 0, 2*Math.PI); ctx.fill(); ctx.stroke();
      } else if (icon2 === 'INPUT') {
        ctx.strokeRect(col4 + 10, y + 2, 16, 16);
        ctx.beginPath(); ctx.arc(col4 + 18, y + 10, 2, 0, 2*Math.PI); ctx.fill();
      } else if (icon2 === 'GROUND') {
        ctx.beginPath(); ctx.moveTo(col4+20, y+4); ctx.lineTo(col4+20, y+10);
        ctx.moveTo(col4+10, y+10); ctx.lineTo(col4+30, y+10);
        ctx.moveTo(col4+14, y+13); ctx.lineTo(col4+26, y+13);
        ctx.moveTo(col4+18, y+16); ctx.lineTo(col4+22, y+16);
        ctx.stroke();
      }
      ctx.fillStyle = '#000';
      ctx.fillText(name2, col5 + 5, y + 14);
      ctx.fillText(desc2, col6 + 5, y + 14);
    }
  };

  drawRow(0, 'XOR', 'XOR', 'Logic Exclusive-OR Gate', 'PROBE', 'Probe', 'Logic Monitor');
  drawRow(1, 'AND', 'AND', 'Logic AND Gate', 'INPUT', 'Input', 'Logical Input');
  drawRow(2, 'OR',  'OR',  'Logic OR Gate', 'GROUND', 'Ground', 'Earth Connection');
  drawRow(3, 'NOT', 'NOT', 'Logic Inverter Gate', null, '', '');
}

function toggleInput(id) {
  inputValues[id] = inputValues[id] ? 0 : 1;
  draw();
}

document.getElementById('btn-toggle-mode').addEventListener('click', (e) => {
  if (mode === 'gray_to_xs3') {
    mode = 'xs3_to_gray';
    e.target.innerText = 'Cambiar a Gray -> XS3';
    document.getElementById('file-title').innerText = 'convertidor de codigo xs3 a gray final.ewb';
    inputValues.D = 0; inputValues.C = 0; inputValues.B = 1; inputValues.A = 1; // Dec 0
  } else {
    mode = 'gray_to_xs3';
    e.target.innerText = 'Cambiar a XS3 -> Gray';
    document.getElementById('file-title').innerText = 'convertidor de codigo gray a xs3 final.ewb';
    inputValues.D = 0; inputValues.C = 0; inputValues.B = 0; inputValues.A = 0; // Dec 0
  }
  draw();
});

document.getElementById('power-switch').addEventListener('click', () => {
  powerOn = !powerOn;
  const toggle = document.getElementById('switch-toggle');
  if (powerOn) {
    toggle.classList.remove('off');
    toggle.classList.add('on');
  } else {
    toggle.classList.remove('on');
    toggle.classList.add('off');
  }
  draw();
});

canvas.addEventListener('click', (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  const c = circuits[mode];
  c.inputs.forEach(i => {
    if (x > i.x - 15 && x < i.x + 15 && y > i.y - 15 && y < i.y + 15) {
      toggleInput(i.id);
    }
  });
});

window.addEventListener('keydown', (e) => {
  const key = e.key.toUpperCase();
  if (['A', 'B', 'C', 'D'].includes(key)) {
    toggleInput(key);
  }
});

setTimeout(() => {
  resize();
}, 100);
