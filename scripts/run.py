#!/usr/bin/env python3
"""
Run script for the Multi-Agent System
Starts the API, UI, or both services
"""

import sys
import argparse
import logging
from workspace.dev_resources import serve_api, serve_ui, serve_both

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main run function"""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="Multi-Agent System Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scripts.run api          # Start only the API server
  python -m scripts.run ui           # Start only the Streamlit UI
  python -m scripts.run both         # Start both services
  python -m scripts.run --help       # Show this help message
        """
    )
    
    parser.add_argument(
        "service",
        choices=["api", "ui", "both"],
        default="both",
        nargs="?",
        help="Service to run (default: both)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--api-port",
        type=int,
        default=8000,
        help="API port (default: 8000)"
    )
    
    parser.add_argument(
        "--ui-port", 
        type=int,
        default=8501,
        help="UI port (default: 8501)"
    )
    
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload for API (production mode)"
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Starting Multi-Agent System - {args.service.upper()}")
    
    try:
        if args.service == "api":
            serve_api(
                host=args.host,
                port=args.api_port,
                reload=not args.no_reload
            )
        elif args.service == "ui":
            serve_ui(
                host=args.host,
                port=args.ui_port
            )
        elif args.service == "both":
            serve_both()
            
    except KeyboardInterrupt:
        print("\n👋 Service stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 