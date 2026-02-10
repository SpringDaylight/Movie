"""
Database migration script
Creates and applies Alembic migrations
"""
import sys
import subprocess
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))


def create_migration(message: str):
    """Create a new migration"""
    print(f"Creating migration: {message}")
    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Migration created successfully!")
        print(result.stdout)
    else:
        print("✗ Migration creation failed!")
        print(result.stderr)
        sys.exit(1)


def apply_migrations():
    """Apply all pending migrations"""
    print("Applying migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Migrations applied successfully!")
        print(result.stdout)
    else:
        print("✗ Migration failed!")
        print(result.stderr)
        sys.exit(1)


def show_current():
    """Show current migration version"""
    print("Current migration version:")
    result = subprocess.run(
        ["alembic", "current"],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def show_history():
    """Show migration history"""
    print("Migration history:")
    result = subprocess.run(
        ["alembic", "history"],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )
    print(result.stdout)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration tool")
    parser.add_argument("action", choices=["create", "apply", "current", "history"],
                       help="Action to perform")
    parser.add_argument("-m", "--message", help="Migration message (for create)")
    
    args = parser.parse_args()
    
    if args.action == "create":
        if not args.message:
            print("Error: --message is required for create action")
            sys.exit(1)
        create_migration(args.message)
    elif args.action == "apply":
        apply_migrations()
    elif args.action == "current":
        show_current()
    elif args.action == "history":
        show_history()
