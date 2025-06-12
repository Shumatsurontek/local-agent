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
    import threading
    import time
    
    # Start API in a separate thread
    api_thread = threading.Thread(
        target=serve_api,
        kwargs={
            "host": ws_settings.api_host,
            "port": ws_settings.api_port,
            "reload": True
        }
    )
    api_thread.daemon = True
    api_thread.start()
    
    # Give API time to start
    time.sleep(2)
    
    # Start Streamlit
    serve_ui(
        host=ws_settings.streamlit_host,
        port=ws_settings.streamlit_port
    )

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