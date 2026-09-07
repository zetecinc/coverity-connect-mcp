# インストールガイド - Coverity Connect MCP Server

## 🎯 概要

このガイドでは、Coverity Connect MCP Serverの包括的なインストール手順を、様々な環境とプラットフォームに対応して説明します。

## 📋 前提条件

### システム要件
- **Python**: 3.8 以上
- **オペレーティングシステム**: Windows 10/11、macOS 10.14+、Linux (Ubuntu 18.04+、CentOS 7+)
- **メモリ**: 最小 512MB RAM、推奨 1GB+
- **ディスク容量**: インストール用 100MB、ログとデータ用 500MB
- **ネットワーク**: Coverity Connect サーバーへのアクセス (通常ポート 8080/443)

### 必要なソフトウェア
- **Python パッケージマネージャー**: pip 21.0+
- **Git**: ソースインストール用 (オプション)
- **Claude Desktop**: MCP統合用の最新版

### アクセス要件
- **Coverity Connect**: 適切な権限を持つ有効なユーザーアカウント
- **認証**: 認証キーまたはユーザー名/パスワード資格情報
- **ネットワークアクセス**: Coverity Connect サーバーへの接続性

## 🚀 インストール方法

### 方法1: パッケージインストール (推奨)

#### pipを使用
```bash
# ソースからインストール (現在の方法)
git clone https://github.com/keides2/coverity-connect-mcp.git
cd coverity-connect-mcp
pip install -e .
```

#### インストール確認
```bash
# インポートテスト
python -c "import coverity_mcp_server; print('インストール成功')"

# バージョン確認
python -m coverity_mcp_server --help
```

### 方法2: ソースインストール

#### リポジトリのクローン
```bash
git clone https://github.com/keides2/coverity-connect-mcp.git
cd coverity-connect-mcp
```

#### 仮想環境の作成
```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 依存関係のインストール
```bash
# 開発用インストール
pip install -e .

# 開発用依存関係 (オプション)
pip install -e ".[dev]"
```

## 🔧 Claude Desktop 統合

### 設定ファイルの場所
Claude Desktop設定ファイルを見つけます：

**Windows:**
- `%APPDATA%\Claude\claude_desktop_config.json`
- `%LOCALAPPDATA%\Claude\claude_desktop_config.json`

**macOS:**
- `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:**
- `~/.config/claude/claude_desktop_config.json`

### 設定セットアップ
Claude Desktop設定に以下を追加します：

```json
{
  "mcpServers": {
    "coverity-connect": {
      "command": "python",
      "args": ["-m", "coverity_mcp_server"],
      "cwd": "/path/to/coverity-connect-mcp",
      "env": {
        "COVERITY_HOST": "your-coverity-server.com",
        "COVERITY_PORT": "8080",
        "COVERITY_SSL": "True",
        "COVAUTHUSER": "your-username",
        "COVAUTHKEY": "your-auth-key"
      }
    }
  }
}
```

## 🧪 インストール確認

### 基本テスト
```bash
# インポートテスト
python -c "import coverity_mcp_server; print('✅ インポート成功')"

# サーバー起動テスト
python -m coverity_mcp_server --help

# 設定テスト
python -c "from coverity_mcp_server.config import get_config; print('✅ 設定読み込み完了')"
```

### 開発環境テスト
```bash
# モックサーバー起動 (別ターミナルで)
python examples/development/mock_server.py

# モックデータでMCPサーバーテスト
export COVERITY_HOST=localhost
export COVERITY_PORT=5000
export COVERITY_SSL=False
export COVAUTHUSER=dummy_user
export COVAUTHKEY=dummy_key

python -m coverity_mcp_server
```

## 🚨 トラブルシューティング

### 一般的なインストール問題

#### Pythonバージョン互換性
```bash
# Pythonバージョン確認
python --version

# 互換バージョンのインストール
pyenv install 3.10.0
pyenv local 3.10.0
```

#### ネットワーク接続問題
```bash
# 接続テスト
telnet your-coverity-server 8080

```

### ヘルプの取得

#### サポートチャネル
- **GitHub Issues**: https://github.com/keides2/coverity-connect-mcp/issues
- **ドキュメント**: SETUP_GUIDE.md で詳細手順確認
- **ディスカッション**: https://github.com/keides2/coverity-connect-mcp/discussions

---

**最終更新**: 2025年7月19日  
**バージョン**: 1.0.0