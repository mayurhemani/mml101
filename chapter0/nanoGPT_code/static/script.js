const canvas = document.getElementById('canvas');
const ctx    = canvas.getContext('2d');
const acceptBtn = document.getElementById('acceptBtn');

let drawing = false;
let currentStroke = [];
let userStrokes = [];
let suggestion = [];

let predictTimeout = null;

// Resize handling
function resize() {
  canvas.width  = 1000; //window.innerWidth;
  canvas.height = 1000; // window.innerHeight;
  redraw();
}
window.addEventListener('resize', resize);
resize();

// Start a new stroke
canvas.addEventListener('mousedown', e => {
  drawing = true;
  currentStroke = [[e.offsetX, e.offsetY]];
  suggestion = [];
  acceptBtn.style.display = 'none';
});

// Continue stroke & debounce prediction
canvas.addEventListener('mousemove', e => {
  if (!drawing) return;
  const pt =  currentStroke[currentStroke.length-1];
  const npt = [e.offsetX, e.offsetY];
  if ((pt[0] != npt[0]) || (pt[1] != npt[1])) {
	currentStroke.push(npt);
  	redraw();
  }
  clearTimeout(predictTimeout);
  predictTimeout = setTimeout(runPredict, 200);
});

// End stroke
canvas.addEventListener('mouseup', e => {
  drawing = false;
  userStrokes.push(currentStroke);
  clearTimeout(predictTimeout);
  runPredict();
});

// Send current stroke to server
async function runPredict() {
  if (!currentStroke.length) return;
  try {
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stroke: currentStroke })
    });
    const data = await resp.json();
    suggestion = data.prediction || [];
    acceptBtn.style.display = suggestion.length ? 'block' : 'none';
    redraw();
  } catch(err) {
    console.error('Predict error', err);
  }
}

// Accept the suggestion as part of your drawing
acceptBtn.addEventListener('click', () => {
  if (suggestion.length) {
    userStrokes.push(suggestion);
    suggestion = [];
    acceptBtn.style.display = 'none';
    redraw();
  }
});

// Redraw everything
function redraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw all finished strokes
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#000';
  for (let stroke of userStrokes) {
    ctx.beginPath();
    stroke.forEach((p, i) => {
      i===0 ? ctx.moveTo(...p) : ctx.lineTo(...p);
    });
    ctx.stroke();
  }

  // Draw current stroke
  if (drawing) {
    ctx.beginPath();
    ctx.strokeStyle = '#000';
    currentStroke.forEach((p, i) => {
      i===0 ? ctx.moveTo(...p) : ctx.lineTo(...p);
    });
    ctx.stroke();
  }

  // Draw suggestion in light colour
  if (suggestion.length) {
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(0, 0, 255, 0.3)';
	const pt = currentStroke[currentStroke.length-1];
	ctx.moveTo(...pt);
	for (let i = 0, ie = suggestion.length - 1; i < ie; i+=2) {
		ctx.quadraticCurveTo(suggestion[i][0], suggestion[i][1], suggestion[i+1][0], suggestion[i+1][1]);
		ctx.moveTo(suggestion[i+1][0], suggestion[i+1][1]);
	}
    ctx.stroke();
  }
}

