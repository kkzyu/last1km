import sqlite3
import os

# 数据库文件路径
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'zjulast1km.db')

def check_database():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("数据库中的表:", tables)
        
        # 检查users表结构
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        print("\nusers表结构:")
        for col in columns:
            print(f"  {col[1]} {col[2]} {'NOT NULL' if col[3] else 'NULL'}")
        
        # 检查用户数据
        cursor.execute("SELECT id, username, nickname, phone, email, created_at FROM users;")
        users = cursor.fetchall()
        print(f"\n用户数据 (共{len(users)}条):")
        for user in users:
            print(f"  ID: {user[0]}, 用户名: {user[1]}, 昵称: {user[2]}, 手机: {user[3]}, 邮箱: {user[4]}, 创建时间: {user[5]}")
        
        conn.close()
        
    except Exception as e:
        print(f"检查数据库时出错: {e}")

if __name__ == "__main__":
    check_database()