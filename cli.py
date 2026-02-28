import typer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User

cli = typer.Typer()

@cli.command()
def change_role(email: str, is_admin: bool = typer.Option(False, "--admin", help="Make user admin")):
    """Change user role (admin/client)"""
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            typer.echo(f"User with email {email} not found")
            raise typer.Exit(1)
        
        user.is_admin = is_admin
        db.commit()
        
        role = "admin" if is_admin else "client"
        typer.echo(f"User {email} role changed to {role}")
    finally:
        db.close()

if __name__ == "__main__":
    cli()