import subprocess
import json

def test_system():
    print("🔍 Testing Project Management CLI...")
    
    # Check if JSON files exist and have data
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
            print(f"✅ Users file exists with {len(users)} users")
    except:
        print("❌ Users file not found or empty")
    
    try:
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
            print(f"✅ Projects file exists with {len(projects)} projects")
    except:
        print("❌ Projects file not found or empty")
    
    try:
        with open('data/tasks.json', 'r') as f:
            tasks = json.load(f)
            print(f"✅ Tasks file exists with {len(tasks)} tasks")
    except:
        print("❌ Tasks file not found or empty")
    
    print("\n📊 Summary:")
    print(f"Total Users: {len(users) if 'users' in locals() else 0}")
    print(f"Total Projects: {len(projects) if 'projects' in locals() else 0}")
    print(f"Total Tasks: {len(tasks) if 'tasks' in locals() else 0}")

if __name__ == "__main__":
    test_system()
