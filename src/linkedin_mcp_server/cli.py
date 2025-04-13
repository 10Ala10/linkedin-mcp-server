# src/linkedin_mcp_server/cli.py
"""
CLI utilities for LinkedIn MCP server.

This module handles the command-line interface and configuration management.
"""

from typing import Dict, Any, List
import os
import json
import subprocess
import logging
import pyperclip

logger = logging.getLogger(__name__)


def print_claude_config() -> None:
    """
    Print Claude configuration and copy to clipboard.

    This function generates the configuration needed for Claude Desktop
    and copies it to the clipboard for easy pasting.
    """
    current_dir = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )

    # Find the full path to uv executable
    try:
        uv_path = subprocess.check_output(["which", "uv"], text=True).strip()
        print(f"🔍 Found uv at: {uv_path}")
    except subprocess.CalledProcessError:
        # Fallback if which uv fails
        uv_path = "uv"
        print(
            "⚠️ Could not find full path to uv, using 'uv' directly. "
            "This may not work in Claude Desktop."
        )

    # Include useful command-line arguments in the default args
    args: List[str] = ["--directory", current_dir, "run", "main.py"]

    config_json: Dict[str, Any] = {
        "mcpServers": {
            "linkedin_scraper": {
                "command": uv_path,
                "args": args,
                "disabled": False,
                "requiredTools": [
                    "get_person_profile",
                    "get_company_profile",
                    "get_job_details",
                    "search_jobs",
                ],
            }
        }
    }

    # Convert to string for clipboard
    config_str = json.dumps(config_json, indent=2)

    # Print the final configuration
    print("\n📋 Your Claude configuration should look like:")
    print(config_str)
    print(
        "\n🔧 Add this to your Claude Desktop configuration in Settings > Developer > Edit Config"
    )

    # Copy to clipboard
    try:
        pyperclip.copy(config_str)  # Only copy the JSON, not the comments
        print("\n✅ Claude configuration copied to clipboard!")
    except ImportError:
        print(
            "\n⚠️ pyperclip not installed. To copy configuration automatically, run: uv add pyperclip"
        )
    except Exception as e:
        print(f"\n❌ Could not copy to clipboard: {e}")
