import pymysql

# 数据库连接参数
connection = pymysql.connect(
    host='localhost',  # 数据库服务器地址
    user='root',  # MariaDB 用户名
    password='qweasdzxc',  # MariaDB 密码
    charset='utf8mb4',  # 字符编码
    cursorclass=pymysql.cursors.DictCursor  # 光标类型
)

try:
    with connection.cursor() as cursor:
        # 1. 创建数据库（如果还没有创建）
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS Relationship_Service_Provider CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

        # 2. 使用数据库
        cursor.execute("USE Relationship_Service_Provider;")

        # 3. 创建 Users 表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            handle VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            biometrics VARCHAR(512),
            public_private_key_pair VARCHAR(1024)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
        cursor.execute(create_table_sql)
        print("Table 'Users' created successfully.")

    # 提交更改
    connection.commit()

finally:
    # 关闭数据库连接
    connection.close()
