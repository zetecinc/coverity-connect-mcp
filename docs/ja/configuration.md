# 設定リファレンス - Coverity Connect MCP Server

## 🎯 概要

このガイドでは、Coverity Connect MCP Serverの包括的な設定オプションを、環境変数、設定ファイル、高度な設定を含めて説明します。

## 📋 設定方法

サーバーは複数の設定方法をサポートしており、優先順位は以下の通りです：

1. **コマンドライン引数** (最高優先度)
2. **環境変数**
3. **設定ファイル**
4. **デフォルト値** (最低優先度)

## 🔧 環境変数

### Coverity コア設定

#### COVERITY_HOST
- **説明**: Coverity Connect サーバーのホスト名またはIPアドレス
- **タイプ**: 文字列
- **必須**: はい
- **デフォルト**: なし
- **例**: 
  - `coverity.company.com`
  - `192.168.1.100`
  - `localhost` (開発用)

```bash
export COVERITY_HOST="coverity.company.com"
```

#### COVERITY_PORT
- **説明**: Coverity Connect サーバーのポート
- **タイプ**: 整数
- **必須**: いいえ
- **デフォルト**: `8080`
- **一般的な値**: `8080`, `443`, `8443`

```bash
export COVERITY_PORT="8080"
```

#### COVERITY_SSL
- **説明**: SSL/TLS接続の有効化
- **タイプ**: 真偽値 (True/False)
- **必須**: いいえ
- **デフォルト**: `True`
- **注意**: 開発/テスト時のみ`False`に設定

```bash
export COVERITY_SSL="True"      # 本番環境
export COVERITY_SSL="False"     # 開発環境
```

### 認証設定

#### COVAUTHUSER
- **説明**: Coverity Connect ユーザー名
- **タイプ**: 文字列
- **必須**: はい
- **セキュリティ**: 安全に保存し、コードに含めない

```bash
export COVAUTHUSER="your-username"
```

#### COVAUTHKEY
- **説明**: Coverity Connect 認証キーまたはパスワード
- **タイプ**: 文字列
- **必須**: はい
- **セキュリティ**: 高度に機密 - セキュアボルトに保存

```bash
export COVAUTHKEY="your-auth-key-here"
```

### MCP サーバー設定

#### MCP_DEBUG
- **説明**: MCPデバッグモードの有効化
- **タイプ**: 真偽値 (True/False)
- **必須**: いいえ
- **デフォルト**: `False`

```bash
export MCP_DEBUG="True"         # 開発環境
export MCP_DEBUG="False"        # 本番環境
```

#### LOG_LEVEL
- **説明**: ログの詳細レベル
- **タイプ**: 文字列
- **必須**: いいえ
- **デフォルト**: `INFO`
- **値**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```bash
export LOG_LEVEL="DEBUG"        # 開発環境
export LOG_LEVEL="INFO"         # 本番環境
export LOG_LEVEL="WARNING"      # 最小ログ
```

## 📄 設定ファイル

### .env ファイル形式

プロジェクトルートに`.env`ファイルを作成：

```bash
# Coverity Connect 設定
COVERITY_HOST=coverity.company.com
COVERITY_PORT=8080
COVERITY_SSL=True
COVAUTHUSER=your-username
COVAUTHKEY=your-auth-key

# MCP 設定
MCP_DEBUG=False
LOG_LEVEL=INFO

# パフォーマンス
TIMEOUT_SECONDS=30
MAX_CONNECTIONS=10
```

### 環境固有ファイル

#### 開発環境 (.env.development)
```bash
# 開発環境
COVERITY_HOST=localhost
COVERITY_PORT=5000
COVERITY_SSL=False
COVAUTHUSER=dummy_user
COVAUTHKEY=dummy_key
MCP_DEBUG=True
LOG_LEVEL=DEBUG
```

#### 本番環境 (.env.production)
```bash
# 本番環境
COVERITY_HOST=coverity.company.com
COVERITY_PORT=8080
COVERITY_SSL=True
COVAUTHUSER=${VAULT_USER}
COVAUTHKEY=${VAULT_KEY}
MCP_DEBUG=False
LOG_LEVEL=INFO
SSL_VERIFY=True
TIMEOUT_SECONDS=60
```

## ⚙️ Claude Desktop 設定

### 基本設定
```json
{
  "mcpServers": {
    "coverity-connect": {
      "command": "python",
      "args": ["-m", "coverity_mcp_server"],
      "cwd": "/path/to/coverity-connect-mcp",
      "env": {
        "COVERITY_HOST": "coverity.company.com",
        "COVERITY_PORT": "8080",
        "COVERITY_SSL": "True",
        "COVAUTHUSER": "your-username",
        "COVAUTHKEY": "your-auth-key"
      }
    }
  }
}
```

## 🔐 セキュリティ設定

### セキュアな認証情報保存

#### 環境変数使用 (基本)
```bash
# セキュアな場所に保存
echo 'export COVAUTHKEY="your-key"' >> ~/.bashrc_secrets
chmod 600 ~/.bashrc_secrets
source ~/.bashrc_secrets
```

#### Vault使用 (推奨)
```bash
# HashiCorp Vault に保存
vault kv put secret/coverity-mcp \
  username=your-user \
  authkey=your-key

# アプリケーションで取得
export COVAUTHUSER=$(vault kv get -field=username secret/coverity-mcp)
export COVAUTHKEY=$(vault kv get -field=authkey secret/coverity-mcp)
```

## ⚠️ 設定検証

### 必須設定チェック
```bash
# 検証スクリプト
python -c "
import os
required = ['COVERITY_HOST', 'COVAUTHUSER', 'COVAUTHKEY']
missing = [var for var in required if not os.getenv(var)]
if missing:
    print(f'❌ 不足している必須変数: {missing}')
    exit(1)
else:
    print('✅ すべての必須変数が設定されています')
"
```

### 設定テスト
```bash
# 設定テスト
python -c "
from coverity_mcp_server.config import get_config
try:
    config = get_config()
    print('✅ 設定が正常に読み込まれました')
    print(f'ホスト: {config.host}')
    print(f'ポート: {config.port}')
    print(f'SSL: {config.use_ssl}')
except Exception as e:
    print(f'❌ 設定エラー: {e}')
"
```

## 🔧 設定のトラブルシューティング

### 一般的な問題

#### 認証失敗
```bash
# 認証情報確認
echo "ユーザー: $COVAUTHUSER"
echo "キー長: ${#COVAUTHKEY}"

# 認証テスト
curl -u "$COVAUTHUSER:$COVAUTHKEY" \
  "https://$COVERITY_HOST:$COVERITY_PORT/ws/v9/configurationservice?wsdl"
```

#### SSL証明書問題
```bash
# 証明書確認
openssl s_client -connect $COVERITY_HOST:$COVERITY_PORT -showcerts

# SSL無効化 (一時的、非セキュア)
export SSL_VERIFY=False
```

#### ネットワーク接続
```bash
# ネットワーク接続テスト
telnet $COVERITY_HOST $COVERITY_PORT

```

## 📋 設定チェックリスト

### 開発環境
- [ ] `COVERITY_HOST=localhost`
- [ ] `COVERITY_PORT=5000`
- [ ] `COVERITY_SSL=False`
- [ ] `COVAUTHUSER=dummy_user`
- [ ] `COVAUTHKEY=dummy_key`
- [ ] `MCP_DEBUG=True`
- [ ] `LOG_LEVEL=DEBUG`

### 本番環境
- [ ] `COVERITY_HOST=production-server`
- [ ] `COVERITY_SSL=True`
- [ ] セキュアな認証情報保存
- [ ] `MCP_DEBUG=False`
- [ ] `LOG_LEVEL=WARNING`
- [ ] SSL検証有効
- [ ] パフォーマンス調整適用
- [ ] 監視設定
- [ ] ヘルスチェック有効

## 📚 追加リソース

### 設定例
- **開発**: `examples/development/.env.development`
- **本番**: `examples/production/.env.production`

### 関連ドキュメント
- **インストールガイド**: `docs/ja/installation.md`
- **セットアップガイド**: `SETUP_GUIDE.md`
- **API リファレンス**: `docs/ja/api.md`

---

**最終更新**: 2025年7月19日  
**バージョン**: 1.0.0  
**設定スキーマバージョン**: 1.0