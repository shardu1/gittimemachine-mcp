# GitTimeMachine MCP Server  
🚀 AI-powered Git history analysis & time-travel debugging for AI assistants  

---

## 📖 Overview  
**GitTimeMachine** is a **Model Context Protocol (MCP) server** that gives AI assistants like **Claude Code** deep access to your Git history. It enables intelligent analysis of code changes, commit blame information, and **time-travel debugging** of files across commits.  

This makes your AI assistant not just a code helper, but a **true collaborator** in understanding the evolution of your codebase.  

---

## ✨ Features  
- 📜 **Git History Analysis**: Get detailed commit history for files and specific lines  
- 🔍 **Blame Information**: See who changed what and when  
- ⏮️ **Time-Travel Debugging**: View previous versions of files at specific commits  
- 📂 **Repository Browser**: List and explore files in any Git repository  
- 🔄 **Dynamic Switching**: Switch between different Git repositories on-the-fly  
- 🤖 **MCP Compatible**: Works with Claude Code currently (Cursor and other MCP clients will be available soon)  

---

## 🛠️ System Requirements  
- Python **3.8+**  
- Git installed & available in `PATH`  
- Claude Desktop (Download manually https://claude.ai/download)

---

## 🚀 Quick Start  

### One-Click Installation (Recommended)  
```bash
# Clone the repository
git clone https://github.com/yourusername/gittimemachine-mcp.git
cd gittimemachine-mcp

# Run the automated installer (Windows/Mac/Linux)
python install.py
```

## 🎯 Usage Guide  

Once installed and configured, **GitTimeMachine** integrates seamlessly with your **Claude Desktop** or **Clauda Code**.  

### Example Commands Supported  
- `Open Clauda Code/Desktop`
- `Use /path/to/your/git/repository for ananlysis`
- `Show me the commit history of app.py`  
- `Who last modified line 42 in main.py?`  
- `Restore the version of server.js from commit abc123`  
- `Switch to repository my-other-project`  

