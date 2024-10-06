import pymysql

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

# 插入测试用户数据
def insert_test_user():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 插入用户数据，密码为明文存储
            sql = """
            INSERT INTO Users (name, email, handle, password, biometrics, public_private_key_pair)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                'AAAA',               # 用户名
                'fgds@example.com',        # 邮箱
                'safdsafas',                 # 用户句柄
                'password',             # 明文密码
                'encrypted_biometrics',    # 生物识别数据
                'encrypted_key_pair'       # 公私钥对
            ))
            connection.commit()  # 提交数据
            print("测试用户插入成功！")
    finally:
        connection.close()

# 调用该函数插入测试用户
insert_test_user()
