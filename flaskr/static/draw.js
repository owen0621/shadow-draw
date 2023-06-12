// 取得畫布元素和按鈕元素
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const clearBtn = document.getElementById('clearBtn');
const saveBtn = document.getElementById('saveBtn');

let isDrawing = false; // 是否正在繪製
let lines = []; // 儲存繪製的曲線
var bgimg = null;

// 設定滑鼠事件監聽器
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);


function setBackground() {
    context.globalCompositeOperation = 'destination-over';
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);

    canvas.toBlob(function (blob) {
        const formData = new FormData();
        formData.append('canvasImage', blob, 'canvas.jpg');

        fetch('/get_background', {
            method: 'POST',
            body: formData
        })
            .then(response => response.blob())
            .then(backgroundBlob => {
                const imageURL = URL.createObjectURL(backgroundBlob);
                canvas.style.backgroundImage = `url(${imageURL})`;
                bgimg = `url(${imageURL})`;
            })
            .catch(error => console.error(error));
    }, 'image/jpeg', 1.0);
}

// 開始繪製
function startDrawing(e) {
    isDrawing = true;
    lines.push([]); // 新增一條曲線
    const currentLine = lines[lines.length - 1];
    const x = e.offsetX;
    const y = e.offsetY;
    currentLine.push({ x, y });
}

// 停止繪製
function stopDrawing() {
    isDrawing = false;
    setBackground();
    if (bgimg !== null) {
        document.body.style.backgroundImage = bgimg;
    }
}

// 繪製
function draw(e) {
    if (!isDrawing) return;

    const currentLine = lines[lines.length - 1];
    const x = e.offsetX;
    const y = e.offsetY;
    currentLine.push({ x, y });

    context.clearRect(0, 0, canvas.width, canvas.height); // 清除畫布
    drawLines(); // 繪製所有曲線
}

// 繪製所有曲線
function drawLines() {
    for (let i = 0; i < lines.length; i++) {
        const currentLine = lines[i];

        if (currentLine.length < 2) continue;

        context.beginPath();
        context.moveTo(currentLine[0].x, currentLine[0].y);

        for (let j = 1; j < currentLine.length; j++) {
            const xc = (currentLine[j].x + currentLine[j - 1].x) / 2;
            const yc = (currentLine[j].y + currentLine[j - 1].y) / 2;
            context.quadraticCurveTo(currentLine[j - 1].x, currentLine[j - 1].y, xc, yc);
        }

        context.stroke();
    }
    if (bgimg !== null) {
        canvas.style.backgroundImage = bgimg;
    }
}

// 清空所有筆跡
clearBtn.addEventListener('click', function () {
    lines = [];
    context.clearRect(0, 0, canvas.width, canvas.height);
});

// 儲存為 JPG
saveBtn.addEventListener('click', function () {
    context.globalCompositeOperation = 'destination-over';
    // Now draw!
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);

    const image = canvas.toDataURL("image/jpeg", 1);
    const link = document.createElement('a');
    link.href = image;
    link.download = 'canvas.jpg';
    link.click();
});

// Call get_background API every second
// setInterval(setBackground, 10000);