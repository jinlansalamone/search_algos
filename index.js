window.onload = async () => {
  const size = 40;
  drawGrid($("#gridHolder"), size);
  addTarget();
  addDebris(0.3 * size * size);
  addStart();

  // await startBfsSearch();
  $("button").onclick = startSearch;

  window.visitCount = 0;
};

async function startSearch() {
  const searchType = $('input[name="searchType"]:checked').value;
  $("button").disabled = true;
  $("button").innerText = "searching...";
  if (searchType === "bfs") {
    await startBfsSearch();
  } else if (searchType === "astar") {
    await startAStarSearch();
  }
  $("button").disabled = false;
  $("button").innerText = "reset";
  $("button").onclick = reset;
}

function reset() {
  window.visitCount = 0;
  const size = window.grid.length;
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      window.grid[i][j].classList.remove("seen");
      window.grid[i][j].classList.remove("found");
    }
  }
  $("button").innerText = "start";
  $("button").onclick = startSearch;
}

function drawGrid(element, size) {
  window.grid = [];
  for (let i = 0; i < size; i++) {
    let row = document.createElement("div");
    row.classList.add("row");
    let rowArr = [];
    for (let j = 0; j < size; j++) {
      let square = document.createElement("div");
      square.classList.add("square");
      row.appendChild(square);
      rowArr.push(square);
    }
    element.appendChild(row);
    window.grid.push(rowArr);
  }
}

function addDebris(count) {
  const size = window.grid.length;
  let placed = 0;

  while (placed < Math.floor(count)) {
    const y = Math.floor(Math.random() * size);
    const x = Math.floor(Math.random() * size);
    const sq = window.grid[y][x];

    if (
      !sq.classList.contains("start") &&
      !sq.classList.contains("target") &&
      !sq.classList.contains("debris")
    ) {
      sq.classList.add("debris");
      placed++;
    }
  }
}

function addStart() {
  window.grid[0][0].classList.add("start");
}

function addTarget() {
  const size = window.grid.length;

  let x = 0;
  let y = 0;

  while (x === 0 && y === 0) {
    x = Math.floor(Math.random() * size);
    y = Math.floor(Math.random() * size);
  }

  window.grid[y][x].classList.add("target");
}

function makeKey(y, x) {
  return `${y},${x}`;
}

function getAdjacent(y, x, size) {
  let coords = [];
  if (y > 0) coords.push([y - 1, x]);
  if (x > 0) coords.push([y, x - 1]);
  if (y + 1 < size) coords.push([y + 1, x]);
  if (x + 1 < size) coords.push([y, x + 1]);
  return coords.filter(
    ([ny, nx]) => !window.grid[ny][nx].classList.contains("debris"),
  );
}

function getTargetCoord() {
  const size = window.grid.length;
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if (window.grid[y][x].classList.contains("target")) return [y, x];
    }
  }
  return null;
}

async function markSeenSquare(y, x) {
  const square = window.grid[y][x];
  const size = window.grid.length;
  await sleep(10);
  if (
    !square.classList.contains("start") &&
    !square.classList.contains("seen")
  ) {
    square.classList.add("seen");
    window.visitCount++;
  }

  const count = window.visitCount;
  const pct = ((100 * count) / size / size).toFixed(1) + "%";
  $("#visitCount").innerText = `visit count: ${count} (${pct})`;
}

function isTargetSquare(y, x) {
  return window.grid[y][x].classList.contains("target");
}

function markFoundSquare(y, x) {
  const square = window.grid[y][x];
  // square.classList.remove("target");
  square.classList.add("found");
}

function reconstructPath(cameFrom, ty, tx) {
  let cur = makeKey(ty, tx);
  let path = [];
  while (cameFrom.has(cur)) {
    const [y, x] = cur.split(",").map(Number);
    path.push([y, x]);
    cur = cameFrom.get(cur);
  }
  path.reverse();
  return path;
}

async function startBfsSearch() {
  const size = window.grid.length;

  const seen = new Set();
  const queue = [[0, 0]];
  seen.add(makeKey(0, 0));

  while (queue.length) {
    const [y, x] = queue.shift();

    await markSeenSquare(y, x);

    if (isTargetSquare(y, x)) {
      markFoundSquare(y, x);
      break;
    }

    const adj = getAdjacent(y, x, size).filter(
      ([ny, nx]) => !seen.has(makeKey(ny, nx)),
    );
    for (const [ny, nx] of adj) {
      seen.add(makeKey(ny, nx));
      queue.push([ny, nx]);
    }
  }
}

async function startAStarSearch() {
  function manhattan(y1, x1, y2, x2) {
    return Math.abs(y1 - y2) + Math.abs(x1 - x2);
  }
  function popBest(open) {
    let bestIdx = 0;
    for (let i = 1; i < open.length; i++) {
      if (open[i].f < open[bestIdx].f) bestIdx = i;
    }
    return open.splice(bestIdx, 1)[0];
  }
  async function drawPath(path) {
    for (const [y, x] of path) {
      await sleep(10);
      const sq = window.grid[y][x];
      if (!sq.classList.contains("start") && !sq.classList.contains("found")) {
        sq.classList.add("found");
      }
    }
  }
  const size = window.grid.length;
  const target = getTargetCoord();
  if (!target) return;
  const [ty, tx] = target;

  const gScore = new Map();
  const cameFrom = new Map();
  const closed = new Set();

  const startKey = makeKey(0, 0);
  gScore.set(startKey, 0);

  let open = [{ y: 0, x: 0, f: manhattan(0, 0, ty, tx) }];

  while (open.length) {
    const cur = popBest(open);
    const y = cur.y;
    const x = cur.x;
    const key = makeKey(y, x);

    if (closed.has(key)) continue;
    closed.add(key);

    await markSeenSquare(y, x);

    if (isTargetSquare(y, x)) {
      markFoundSquare(y, x);
      const path = reconstructPath(cameFrom, y, x);
      await drawPath(path);
      break;
    }

    const baseG = gScore.get(key) ?? Infinity;

    for (const [ny, nx] of getAdjacent(y, x, size)) {
      const nkey = makeKey(ny, nx);
      if (closed.has(nkey)) continue;

      const tentativeG = baseG + 1;
      const prevG = gScore.get(nkey) ?? Infinity;

      if (tentativeG < prevG) {
        cameFrom.set(nkey, key);
        gScore.set(nkey, tentativeG);
        open.push({ y: ny, x: nx, f: tentativeG + manhattan(ny, nx, ty, tx) });
      }
    }
  }
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function $(s) {
  return document.querySelector(s);
}
