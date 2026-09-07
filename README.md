# Coverity Connect MCP Server

<img src="top.png" alt="Coverity Connect MCP Server" width="700">

<!-- [![PyPI version](https://badge.fury.io/py/coverity-connect-mcp.svg)](https://badge.fury.io/py/coverity-connect-mcp) -->
<!-- [![Python Support](https://img.shields.io/pypi/pyversions/coverity-connect-mcp.svg)](https://pypi.org/project/coverity-connect-mcp/) -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Check](https://github.com/keides2/coverity-connect-mcp/workflows/Security%20Check%20Only/badge.svg)](https://github.com/keides2/coverity-connect-mcp/actions)
[![Coverage](https://codecov.io/gh/keides2/coverity-connect-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/keides2/coverity-connect-mcp)

**English** | [日本語](README_ja.md)

A **Model Context Protocol (MCP) server** that provides seamless integration between AI assistants (like Claude Desktop) and **Black Duck Coverity Connect** static analysis platform.

Transform your Coverity workflow with natural language commands and automated analysis through AI-powered interactions.

## 🚀 Features

### 🔍 **Comprehensive Coverity Integration**
- **Project Management**: List and explore Coverity projects and streams
- **Defect Analysis**: Advanced defect search with intelligent filtering and detailed analysis
- **User Management**: Complete user administration, role management, and access control
- **Security Focus**: Specialized security vulnerability detection and analysis
- **CI/CD Automation**: Automated pipeline integration for continuous quality monitoring
- **Quality Reports**: Executive-level quality dashboards and trend analysis

### 🤖 **AI-Powered Analysis**
- **Natural Language Queries**: "Show me critical security issues in project X" or "List users with administrator privileges"
- **Intelligent Filtering**: Automatic prioritization of high-impact defects and user access management
- **Contextual Recommendations**: AI-driven remediation suggestions and security audit insights
- **Trend Analysis**: Historical data analysis, quality metrics, and user activity patterns

### 🛠️ **Enterprise Ready**
- **SOAP API Integration**: Full Coverity Connect Web Services support
- **Authentication**: Secure auth-key based authentication
- **Direct Connections**: Coverity requests never use a proxy
- **Multi-Platform**: Windows, macOS, and Linux support
- **Docker Ready**: Containerized deployment for enterprise environments

## 📦 Installation

### 🎯 **Claude Desktop Integration (Recommended)**

For Claude Desktop users, download the DXT package from the latest release:

1. **Download DXT Package**:
   - Go to [Releases](https://github.com/keides2/coverity-connect-mcp/releases)
   - Download `coverity-connect-mcp-1.0.0.dxt` from the latest release

2. **Install in Claude Desktop**:
   - Drag and drop the `.dxt` file into Claude Desktop
   - Configure environment variables (see Configuration section)

### 🐍 **Python Package Installation**

#### Direct Installation from GitHub
```bash
# Install directly from GitHub (recommended)
pip install git+https://github.com/keides2/coverity-connect-mcp.git
```
### Source Installation

```bash
# Clone and install from source
git clone https://github.com/keides2/coverity-connect-mcp.git
cd coverity-connect-mcp
pip install -e .
```

### 🔧 Development Installation

For development purposes:

```bash
git clone https://github.com/keides2/coverity-connect-mcp.git
cd coverity-connect-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

### 🚀 Future Installation Methods
These installation methods are planned for future releases:

#### PyPI Installation (Planned)

```bash
pip install coverity-connect-mcp
```

#### Docker Installation (Planned)

```bash
docker pull keides2/coverity-connect-mcp:latest
```
## ⚙️ Configuration

### 1. Environment Variables
Create a `.env` file or set environment variables:

```bash
# Required - Coverity Connect Authentication
export COVAUTHUSER="your_coverity_username"
export COVAUTHKEY="your_coverity_auth_key"

# Required - Coverity Server
export COVERITY_HOST="your-coverity-server.com"
export COVERITY_PORT="443"
export COVERITY_SSL="True"

# Optional - Local Workspace
export COVERITY_BASE_DIR="/path/to/coverity/workspace"

```

### 2. Claude Desktop Integration
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "coverity-connect": {
      "command": "coverity-mcp-server",
      "env": {
        "COVAUTHUSER": "${COVAUTHUSER}",
        "COVAUTHKEY": "${COVAUTHKEY}",
        "COVERITY_HOST": "your-coverity-server.com"
      }
    }
  }
}
```

### 3. Docker Configuration

> **Note**: Since the Docker image is not yet published, you can build it locally:

```yaml
# docker-compose.yml
version: '3.8'
services:
  coverity-mcp:
    build: .  # Build from local source
    # Future: image: keides2/coverity-connect-mcp:latest
    environment:
      - COVAUTHUSER=${COVAUTHUSER}
      - COVAUTHKEY=${COVAUTHKEY}
      - COVERITY_HOST=${COVERITY_HOST}
    ports:
      - "8000:8000"
```

## 🎯 Usage Examples

### Basic Project Analysis
```
Show me all Coverity projects and their current status
```

### Security-Focused Analysis
```
Analyze the latest snapshot of project "MyWebApp" and focus on high-severity security vulnerabilities. Provide specific remediation recommendations.
```

### Quality Reporting
```
Generate a comprehensive quality report for project "MyProject" including trends over the last 30 days
```

### CI/CD Integration
```
Run automated Coverity analysis for group "web-team", project "frontend", branch "main" with commit message "Security fixes"
```

### Advanced Filtering
```
Show me all CERT-C violations in project "EmbeddedSystem" with impact level "High" and provide code examples for fixes
```

### User Management & Security Audit
```
List all users with administrator privileges and show their last login times
```

### Role-Based Access Control
```
Show me the permissions and role assignments for user "developer1" and identify any security concerns
```

## 🛠️ Available Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `search_defects` | Advanced defect search with filtering | Find high-severity security vulnerabilities |
| `get_defect_details` | Get detailed information about a specific defect | Analyze defect events and remediation steps |
| `mark_defect_intentional` | Classify an issue as Intentional in one stream | Mark CID 12345 as intentional in main |
| `list_projects` | List all accessible Coverity projects | Project inventory and access verification |
| `list_streams` | Get streams for a specific project | Stream-based analysis planning |
| `get_project_summary` | Get comprehensive project analysis | Executive project health reports |
| `list_users` | 🆕 List all users in Coverity Connect | User inventory and access management |
| `get_user_details` | 🆕 Get detailed information about a user | User profile and account status verification |
| `get_user_roles` | 🆕 Get user role and permission information | Security audit and access control review |

## 📚 Documentation

### 🚀 Quick Start
- **[Getting Started Guide](docs/GETTING_STARTED.md)** - 📋 Complete setup guide for production environments
- **[Setup Guide](SETUP_GUIDE.md)** - Complete development to production setup

### English
- **[Installation Guide](docs/installation.md)** - Detailed setup instructions for all platforms
- **[Configuration Reference](docs/configuration.md)** - Complete configuration options and security settings
- **[API Reference](docs/api.md)** - Comprehensive API documentation with examples
- **[Usage Examples](examples/)** - Environment-specific configurations and examples

### 日本語 (Japanese)
- **[本番環境セットアップガイド](docs/GETTING_STARTED.md)** - 📋 本番環境での完全な立ち上げ手順
- **[インストールガイド](docs/ja/installation.md)** - 詳細なセットアップ手順（全プラットフォーム対応）
- **[設定リファレンス](docs/ja/configuration.md)** - 完全な設定オプションとセキュリティ設定
- **[API リファレンス](docs/ja/api.md)** - 包括的なAPI仕様書と使用例
- **[使用例](examples/)** - 環境別設定とサンプル

> 🌐 **多言語サポート**: 英語と日本語の完全ドキュメントを提供しています。すべてのガイドにはステップバイステップの手順、トラブルシューティングのヒント、実用的な例が含まれています。

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/ -m integration

# Run with coverage
pytest --cov=coverity_mcp_server tests/

# Test with Docker
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/keides2/coverity-connect-mcp.git
cd coverity-connect-mcp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Black Duck Coverity** for providing the static analysis platform
- **Anthropic** for the Model Context Protocol and Claude AI
- **Open Source Community** for the foundational libraries and tools

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/keides2/coverity-connect-mcp/issues)
- **Discussions**: [Community support and questions](https://github.com/keides2/coverity-connect-mcp/discussions)
- **Security Issues**: Please see our [Security Policy](SECURITY.md)

## 🗺️ Roadmap

- [x] **v1.0**: Complete MCP implementation with user management ✨
- [ ] **v1.1**: Advanced filtering, custom views, and analytics dashboards
- [ ] **v1.2**: Multi-tenant support and enhanced user administration
- [ ] **v1.3**: GraphQL API and real-time notifications
- [ ] **v1.4**: Machine learning-powered defect prioritization and risk assessment
- [ ] **v2.0**: Plugin architecture and third-party integrations

---

**Made with ❤️ for the software security community**

*Transform your static analysis workflow with the power of AI*
