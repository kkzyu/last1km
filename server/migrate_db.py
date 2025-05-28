import sqlite3
import os
import shutil
from datetime import datetime

def backup_database():
    """备份数据库"""
    db_path = os.path.join('instance', 'zjulast1km.db')
    if os.path.exists(db_path):
        backup_path = f"instance/zjulast1km_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db_path, backup_path)
        print(f"数据库已备份到: {backup_path}")
        return True
    return False

def get_table_columns(cursor, table_name):
    """获取表的列信息"""
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [col[1] for col in cursor.fetchall()]

def add_missing_columns():
    """添加缺失的列到users表"""
    db_path = os.path.join('instance', 'zjulast1km.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取当前表的列
        current_columns = get_table_columns(cursor, 'users')
        print(f"当前users表的列: {current_columns}")
        
        # 需要添加的列及其定义
        columns_to_add = {
            'email': 'VARCHAR(120)',
            'last_login': 'DATETIME'
        }
        
        # 检查并添加缺失的列
        for column_name, column_definition in columns_to_add.items():
            if column_name not in current_columns:
                print(f"添加列: {column_name}")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_definition};")
                
                # 为email创建唯一索引
                if column_name == 'email':
                    try:
                        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);")
                        print("创建email唯一索引")
                    except Exception as e:
                        print(f"创建email索引失败: {e}")
            else:
                print(f"列 {column_name} 已存在，跳过")
        
        conn.commit()
        
        # 验证更新后的表结构
        updated_columns = get_table_columns(cursor, 'users')
        print(f"更新后users表的列: {updated_columns}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"添加列失败: {e}")
        return False

def migrate_database():
    """执行数据库迁移"""
    print("开始数据库迁移...")
    
    # 备份数据库
    backup_database()
    
    # 添加缺失的列
    if add_missing_columns():
        print("数据库迁移完成！")
    else:
        print("数据库迁移失败！")

if __name__ == "__main__":
    migrate_database()