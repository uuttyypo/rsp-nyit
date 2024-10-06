# from flask import Flask, render_template, request, jsonify
# import pymysql
#
# app = Flask(__name__)
#
# # 数据库连接配置
# def get_db_connection():
#     return pymysql.connect(
#         host='localhost',
#         user='root',
#         password='qweasdzxc',
#         database='Relationship_Service_Provider',
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#
# @app.route('/')
# def index():
#     return render_template('index.html')  # 渲染登录页面
#
# # 登录 API
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json  # 获取从前端发送的数据
#     username = data.get('username')
#     password = data.get('password')
#
#     # 连接数据库并查询用户信息
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             # 查询数据库中的用户，获取 handle 和 password 列
#             sql = "SELECT handle, password FROM Users WHERE handle = %s"
#             cursor.execute(sql, (username,))
#             user = cursor.fetchone()
#
#             if not user:
#                 return jsonify({"message": "用户名不存在"}), 404
#
#             # 校验密码（明文比较）
#             if user['password'] == password:
#                 return jsonify({"message": "登录成功!"}), 200
#             else:
#                 return jsonify({"message": "密码错误"}), 401
#     finally:
#         connection.close()
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql
import hashlib
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 数据库连接配置
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='qweasdzxc',
        database='Relationship_Service_Provider',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 帮助函数：密码哈希
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 帮助函数：生成唯一句柄
def generate_handle(name):
    return name.lower().replace(' ', '_') + str(uuid.uuid4())[:8]

@app.route('/')
def index():
    return render_template('index.html')  # 渲染登录页面


# ================================================
# 1. 用户注册
# ================================================
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        handle = request.form['handle']
        password = hash_password(request.form['password'])
        biometrics = request.form.get('biometrics', '')
        public_key = request.form.get('publicKey', '')
        private_key = request.form.get('privateKey', '')

        public_private_key_pair = {
            'public_key': public_key,
            'private_key': private_key
        }

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查邮箱或句柄是否已存在
                cursor.execute("SELECT * FROM Users WHERE email = %s OR handle = %s", (email, handle))
                existing_user = cursor.fetchone()

                if existing_user:
                    return jsonify({"status": "error", "message": "Email or handle already exists!"}), 400

                # 插入新用户
                sql = """
                INSERT INTO Users (name, email, handle, password, biometrics, public_private_key_pair)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (name, email, handle, password, biometrics, str(public_private_key_pair)))
                connection.commit()

            return jsonify({"status": "success", "message": "User registered successfully"}), 201
        finally:
            connection.close()
    return render_template('register.html')

# ================================================
# 2. 用户登录
# ================================================
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    # print(request.form)  # 打印整个表单数据
    # if 'email' not in request.form:
    #     return "Email field is missing", 400

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查用户是否存在并验证密码
                cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()

                if user:
                    # 登录成功，保存会话信息
                    session['user_id'] = user['id']
                    session['email'] = user['email']
                    return redirect(url_for('update_user'))  # 重定向到更新页面
                else:
                    return jsonify({"status": "error", "message": "Invalid email or password"}), 401
        finally:
            connection.close()
    return render_template('login.html')

# ================================================
# 3. 更新用户信息
# ================================================
@app.route('/update', methods=['GET', 'POST'])
def update_user():
    if 'user_id' not in session:
        return redirect(url_for('login_user'))  # 如果未登录，跳转到登录页面

    user_id = session['user_id']

    connection = get_db_connection()
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            handle = request.form['handle']

            # 更新用户信息
            with connection.cursor() as cursor:
                sql = "UPDATE Users SET name = %s, email = %s, handle = %s WHERE id = %s"
                cursor.execute(sql, (name, email, handle, user_id))
                connection.commit()

            return jsonify({"status": "success", "message": "User information updated successfully"}), 200

        # 获取当前用户信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

        return render_template('update.html', user=user)
    finally:
        connection.close()

# ================================================
# 4. 退出登录
# ================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_user'))

if __name__ == '__main__':
    app.run(debug=True)
