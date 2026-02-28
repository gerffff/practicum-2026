import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import User

def change_user_role(user_email: str, role: str):
    if role.lower() not in ['admin', 'client']:
        print("Ошибка: Роль должна быть 'admin' или 'client'")
        return False
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            print(f"Ошибка: Пользователь с email '{user_email}' не найден")
            return False
        
        user.is_admin = (role.lower() == 'admin')
        db.commit()
        
        role_text = "администратор" if user.is_admin else "клиент"
        print(f"✅ Роль пользователя {user_email} изменена на: {role_text}")
        return True
        
    except Exception as e:
        print(f"Ошибка при изменении роли: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("\n📋 Список пользователей:")
        print("-" * 50)
        for user in users:
            role = "Admin" if user.is_admin else "Client"
            print(f"📧 {user.email:<30} | 🔑 {role}")
        print("-" * 50)
    except Exception as e:
        print(f"Ошибка при получении списка пользователей: {e}")
    finally:
        db.close()

def main():
    if len(sys.argv) == 1:
        print("🔧 Управление ролями пользователей")
        print("\nИспользование:")
        print("  python manage_user_role.py <email> <role>")
        print("  python manage_user_role.py list")
        print("\nПримеры:")
        print("  python manage_user_role.py admin@example.com admin")
        print("  python manage_user_role.py user@example.com client")
        print("  python manage_user_role.py list")
        list_users()
        return
    
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'list':
        list_users()
        return
    
    if len(sys.argv) != 3:
        print("❌ Неверное количество аргументов")
        print("Используйте: python manage_user_role.py <email> <role>")
        return
    
    email = sys.argv[1]
    role = sys.argv[2]
    
    change_user_role(email, role)

if __name__ == "__main__":
    main()
