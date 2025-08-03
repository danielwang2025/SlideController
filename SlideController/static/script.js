document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("startButton");

    startButton.addEventListener("click", function () {
        // 发送 POST 请求以启动 Python 脚本
        fetch('/start', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    console.log("Python script started successfully.");
                } else {
                    console.error("Failed to start the Python script.");
                }
            })
            .catch(error => console.error("Error:", error));
    });
});