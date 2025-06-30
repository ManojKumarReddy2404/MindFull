import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_command(command, cwd=None, shell=True, wait=False):
    """Run a command in the specified directory"""
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if wait:
            stdout, stderr = process.communicate()
            return process.returncode, stdout, stderr
        return process
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def start_backend():
    print("🚀 Starting Backend Server...")
    backend_dir = os.path.join(os.path.dirname(__file__), "zen_ai")
    
    # Create and activate virtual environment
    if not os.path.exists(os.path.join(backend_dir, "venv")):
        print("Creating virtual environment...")
        run_command("python -m venv venv", cwd=backend_dir, wait=True)
    
    # Install requirements
    print("Installing Python dependencies...")
    pip_cmd = os.path.join(backend_dir, "venv", "Scripts", "pip")
    run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir, wait=True)
    
    # Start FastAPI server
    uvicorn_cmd = os.path.join(backend_dir, "venv", "Scripts", "uvicorn")
    return run_command(f"{uvicorn_cmd} zen_ai.backend.app:app --reload", cwd=backend_dir)

def start_frontend():
    print("\n🌐 Starting Frontend...")
    frontend_dir = os.path.join(os.path.dirname(__file__), "zen-frontend")
    
    # Install Node dependencies if needed
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("Installing Node dependencies...")
        run_command("npm install", cwd=frontend_dir, wait=True)
    
    # Start Expo development server
    return run_command("npm start", cwd=frontend_dir)

def main():
    print("🚀 Zen Focus Application Launcher")
    print("===================================")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server")
        return
    
    # Give backend a moment to start
    print("\n⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend")
        backend_process.terminate()
        return
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(10)  # Give frontend time to start
        webbrowser.open("http://localhost:19006")
    
    Thread(target=open_browser, daemon=True).start()
    
    print("\n✅ Application is running!")
    print("-----------------------------------")
    print("Backend:  http://localhost:8000")
    print("Frontend: http://localhost:19006")
    print("-----------------------------------")
    print("Press Ctrl+C to stop the application")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping application...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Application stopped")

if __name__ == "__main__":
    main()
