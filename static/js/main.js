document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // 防止表单刷新页面

    // 获取表单数据
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 将数据发送到后端API
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        // 在页面上显示登录消息
        const messageDiv = document.getElementById('message');
        if (data.message === "登录成功!") {
            messageDiv.innerHTML = '<p class="text-success">' + data.message + '</p>';
        } else {
            messageDiv.innerHTML = '<p class="text-danger">' + data.message + '</p>';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
