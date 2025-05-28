import sqlite3
import os

def migrate_database():
    """添加地址字段到用户表"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'zjulast1km_backup_20250527_220615.db')
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查列是否已经存在
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # 添加 default_pickup_address 列
        if 'default_pickup_address' not in columns:
            cursor.execute('''
                ALTER TABLE users 
                ADD COLUMN default_pickup_address TEXT DEFAULT ''
            ''')
            print("✓ 添加了 default_pickup_address 列")
        else:
            print("✓ default_pickup_address 列已存在")
        
        # 添加 default_delivery_address 列
        if 'default_delivery_address' not in columns:
            cursor.execute('''
                ALTER TABLE users 
                ADD COLUMN default_delivery_address TEXT DEFAULT ''
            ''')
            print("✓ 添加了 default_delivery_address 列")
        else:
            print("✓ default_delivery_address 列已存在")
        
        conn.commit()
        conn.close()
        print("🎉 数据库迁移完成!")
        return True
        
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

if __name__ == '__main__':
    migrate_database()