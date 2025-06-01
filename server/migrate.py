from app import create_app
from models import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # 使用新的SQLAlchemy语法
        with db.engine.connect() as conn:
            # 检查字段是否已存在，避免重复添加
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN origin_lat FLOAT'))
                print('添加字段 origin_lat')
            except Exception as e:
                if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                    print('字段 origin_lat 已存在，跳过')
                else:
                    print(f'添加 origin_lat 失败: {e}')
            
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN origin_lng FLOAT'))
                print('添加字段 origin_lng')
            except Exception as e:
                if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                    print('字段 origin_lng 已存在，跳过')
                else:
                    print(f'添加 origin_lng 失败: {e}')
            
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN dest_lat FLOAT'))
                print('添加字段 dest_lat')
            except Exception as e:
                if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                    print('字段 dest_lat 已存在，跳过')
                else:
                    print(f'添加 dest_lat 失败: {e}')
            
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN dest_lng FLOAT'))
                print('添加字段 dest_lng')
            except Exception as e:
                if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                    print('字段 dest_lng 已存在，跳过')
                else:
                    print(f'添加 dest_lng 失败: {e}')
            
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN estimated_duration INTEGER'))
                print('添加字段 estimated_duration')
            except Exception as e:
                if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                    print('字段 estimated_duration 已存在，跳过')
                else:
                    print(f'添加 estimated_duration 失败: {e}')
            
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN estimated_distance FLOAT'))
                print('添加字段 estimated_distance')
            except Exception as e:
                if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                    print('字段 estimated_distance 已存在，跳过')
                else:
                    print(f'添加 estimated_distance 失败: {e}')
            
            conn.commit()
        
        print('数据库迁移完成')
        
    except Exception as e:
        print(f'数据库迁移失败: {e}')
        print('可能是因为字段已存在或其他原因')