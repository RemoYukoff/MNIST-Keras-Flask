const html = document.getElementsByTagName("html")[0];
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const result = document.getElementById("result");
const predict = document.getElementById("predict");
const clear = document.getElementById("clear");

var isDrawing = false;
var lastX = 0;
var lastY = 0;

ctx.lineWidth = 20;
ctx.lineJoin = "round";

function Clean() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

/*Lleno el canvas de blanco*/
Clean();

canvas.addEventListener("mousedown", function (e) {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
});

canvas.addEventListener("mouseup", () => isDrawing = false);

canvas.addEventListener("mouseout", () => isDrawing = false);

canvas.addEventListener("mousemove", (e) => {
    if (isDrawing) {
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.closePath();
        ctx.stroke();
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }
});

clear.addEventListener("click", Clean);

predict.addEventListener("click", function (e) {
    result.innerHTML = "Predicting...";
    var img = canvas.toDataURL();

    $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + "/predict",
        data: img,
        success: function (data) {
            result.innerHTML = "Prediction: " + data
        }
    });
});