"""
Development resources for local development
"""

from workspace.settings import ws_settings
import uvicorn

def serve_api(
    app_file: str = "api.main:app",
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True
):
    """Serve the FastAPI application"""
    print(f"🚀 Starting FastAPI server on http://{host}:{port}")
    print(f"📚 API docs available at http://{host}:{port}/docs")
    
    uvicorn.run(
        app_file,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

def serve_ui(
    app_file: str = "ui/agent_chat.py",
    host: str = "0.0.0.0", 
    port: int = 8501
):
    """Serve the Streamlit application"""
    import subprocess
    import sys
    
    print(f"🎨 Starting Streamlit UI on http://{host}:{port}")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        app_file,
        "--server.address", host,
        "--server.port", str(port),
        "--server.headless", "true"
    ]
    
    subprocess.run(cmd)

def serve_both():
    """Serve both API and UI (for development)"""
    import subprocess
    import sys
    import time
    
    print("🚀 Starting both API and UI services...")
    print("💡 Note: Use 'make run-api' and 'make run-ui' in separate terminals for development with reload")
    
    # Start API in background process (no reload to avoid thread issues)
    api_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "api.main:app",
        "--host", ws_settings.api_host,
        "--port", str(ws_settings.api_port),
        "--log-level", "info"
    ])
    
    print(f"🌐 API started on http://{ws_settings.api_host}:{ws_settings.api_port}")
    
    # Give API time to start
    time.sleep(3)
    
    try:
        # Start Streamlit (this will block)
        serve_ui(
            host=ws_settings.streamlit_host,
            port=ws_settings.streamlit_port
        )
    finally:
        # Clean up API process
        print("🛑 Stopping API...")
        api_process.terminate()
        api_process.wait()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "api":
            serve_api()
        elif sys.argv[1] == "ui":
            serve_ui()
        elif sys.argv[1] == "both":
            serve_both()
        else:
            print("Usage: python dev_resources.py [api|ui|both]")
    else:
        serve_both() 