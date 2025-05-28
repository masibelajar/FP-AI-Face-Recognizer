// Webcam logic
const video = document.getElementById("webcam");
const canvas = document.getElementById("canvas");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    }).catch(err => {
        alert("Webcam tidak tersedia");
    });

function capture() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        const file = new File([blob], "webcam_capture.jpg", { type: "image/jpeg" });
        const fileInput = document.querySelector("input[name='img1']");
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        alert("✅ Gambar webcam dimasukkan ke Gambar 1. Sekarang pilih Gambar 2 dan bandingkan.");
    }, "image/jpeg");
}
