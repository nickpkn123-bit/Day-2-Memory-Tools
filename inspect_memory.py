"""
Memory Inspector - View what your CrewAI agent has stored
==========================================================

This script helps you see what your agent remembers.
"""

import os
import json
from pathlib import Path

def inspect_memory():
    """Display contents of CrewAI memory storage."""
    
    # Get actual CrewAI storage location
    try:
        from crewai.utilities.paths import db_storage_path
        memory_dir = Path(db_storage_path())
    except:
        # Fallback to local db if import fails
        memory_dir = Path("db")
    
    if not memory_dir.exists():
        print("\nNo memory storage found yet.")
        print("Run main.py and have a conversation first!\n")
        return
    
    print("\n" + "="*70)
    print("CrewAI Memory Storage Inspector")
    print("="*70 + "\n")
    
    print(f"Storage Location: {memory_dir}\n")
    
    # Check for long-term memory database
    ltm_db = memory_dir / "long_term_memory_storage.db"
    if ltm_db.exists():
        size_kb = ltm_db.stat().st_size / 1024
        print(f"Long-Term Memory Database:")
        print(f"  File: {ltm_db.name}")
        print(f"  Size: {size_kb:.2f} KB")
        
        try:
            import sqlite3
            conn = sqlite3.connect(str(ltm_db))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"  Tables: {len(tables)}")
            conn.close()
        except:
            pass
    
    # Check task outputs database
    task_db = memory_dir / "latest_kickoff_task_outputs.db"
    if task_db.exists():
        size_kb = task_db.stat().st_size / 1024
        print(f"\nTask Outputs Database:")
        print(f"  File: {task_db.name}")
        print(f"  Size: {size_kb:.2f} KB")
    
    # Check memory directories
    memory_types = {
        "short_term": "Short-Term Memory (ChromaDB)",
        "entities": "Entity Memory (ChromaDB)", 
        "long_term_memory": "Long-Term Memory (ChromaDB)"
    }
    
    print("\nMemory Directories:")
    for dir_name, description in memory_types.items():
        dir_path = memory_dir / dir_name
        if dir_path.exists():
            files = list(dir_path.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            print(f"  {description}:")
            print(f"    Location: {dir_name}/")
            print(f"    Files: {file_count}")
        else:
            print(f"  {description}: Not created yet")
    
    print("\n" + "="*70)
    print("\nMemory System Status:")
    print("  - Short-Term Memory: Stores recent conversation context (RAG)")
    print("  - Long-Term Memory: Preserves insights across sessions")
    print("  - Entity Memory: Tracks people, places, concepts (RAG)")
    print("  - Contextual Memory: Combines all memory types")
    print("\nNote: Memory is stored as vector embeddings and SQLite databases")
    print("="*70 + "\n")

def clear_memory():
    """Clear all stored memory (use with caution!)."""
    
    # Get actual CrewAI storage location
    try:
        from crewai.utilities.paths import db_storage_path
        memory_dir = Path(db_storage_path())
    except:
        memory_dir = Path("db")
    
    if not memory_dir.exists():
        print("\nNo memory to clear.\n")
        return
    
    response = input("\nAre you sure you want to clear all memory? (yes/no): ")
    
    if response.lower() == 'yes':
        import shutil
        shutil.rmtree(memory_dir)
        print("\nMemory cleared! Agent will start fresh next time.\n")
    else:
        print("\nCancelled.\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_memory()
    else:
        inspect_memory()
        print("\nTip: Run 'python inspect_memory.py clear' to reset all memory\n")

