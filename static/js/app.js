new Vue({
    el: '#app',
    data: {
        step: 1,  // 当前步骤
        selectedPlatform: '',  // 用户选择的平台
        credentials: null,  // 导入的凭证数据
    },
    methods: {
        // 下一步
        nextStep() {
            if (this.selectedPlatform) {
                this.step = 2;
            } else {
                alert("请选择一个平台！");
            }
        },
        // 用户认证
        authenticate() {
            // 调用后端API进行认证，获取用户凭证
            fetch('/login')
                .then(response => response.json())
                .then(data => {
                    // 模拟从后端获取到的凭证
                    this.credentials = data.credentials;
                    this.step = 3;
                })
                .catch(error => console.error('Error:', error));
        },
        // 确认导入凭证
        confirmImport() {
            // 调用后端API确认导入凭证
            fetch('/import-credentials', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ credentials: this.credentials }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.step = 4;  // 导入成功
                } else {
                    alert('导入失败');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }
});
