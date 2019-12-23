// QR Code Reader setup

var App = {
    init: function() {
        var self = this;
        Quagga.init(this.state, (err) => {
            if (err) {
                return self.handleError(err);
            }
            Quagga.start();
        });
    },
    handleError: (err) => {
        console.log(err);
    },
    state: {
        inputStream: {
            type: 'LiveStream',
            constraints: {
                width: {min: 800},
                height: {min: 600},
                facingMode: "environment",
                aspectRatio: {min: 1, max: 2},
            },
            target: "#interactive",
        },
        locator: {
            patchSize: 'small',
            halfSample: false,
        },
        numOfWorkers: 4,
        frequency: 30,
        decoder: {
            readers: [{
                format: "ean_reader",
                config: {},
            }],
        },
        locate: true,
    },
    lastResult: null,
};

App.init();

Quagga.onProcessed(function(result) {
    var drawingCtx = Quagga.canvas.ctx.overlay,
        drawingCanvas = Quagga.canvas.dom.overlay;

    if (result) {
        if (result.boxes) {
            drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
            result.boxes.filter(function (box) {
                return box !== result.box;
            }).forEach(function (box) {
                Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx, {color: "green", lineWidth: 2});
            });
        }

        if (result.box) {
            Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx, {color: "#00F", lineWidth: 2});
        }

        if (result.codeResult && result.codeResult.code) {
            Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx, {color: 'red', lineWidth: 3});
        }
    }
});

Quagga.onDetected(function(result) {
    Quagga.stop();
    var code = result.codeResult.code;
    console.log("Code: " + code);
    document.querySelector('#id_ean').value = code;
    document.querySelector("form").submit();

    if (App.lastResult !== code) {
        App.lastResult = code;
        var $node = null, canvas = Quagga.canvas.dom.image;

        $node = $('<li><div class="thumbnail"><div class="imgWrapper"><img /></div><div class="caption"><h4 class="code"></h4></div></div></li>');
        $node.find("img").attr("src", canvas.toDataURL());
        $node.find("h4.code").html(code);
        $("#result_strip ul.thumbnails").prepend($node);
    }
});
