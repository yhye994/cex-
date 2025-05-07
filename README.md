# 交易所自动批量提现工具

这是一个用于从多个交易所批量提现加密货币的工具。

## 功能特点

- 支持多个主流交易所（Binance、OKX、Bybit等）
- 可配置随机提现金额范围
- 可配置随机提现时间间隔
- 支持指定提现币种和网络
- 自动处理提现费用
- 详细的日志记录
- 安全的API密钥管理

## 安装要求

- Python 3.8+
- Microsoft C++ 生成工具（https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/）
- 安装依赖包：`pip install -r requirements.txt`

## 配置说明

1. 创建 `.env` 文件并配置API密钥：
   ```
   # Binance API配置
   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here

   # OKX API配置
   OKX_API_KEY=your_api_key_here
   OKX_API_SECRET=your_api_secret_here
   OKX_PASSPHRASE=your_passphrase_here

   # Bybit API配置
   BYBIT_API_KEY=your_api_key_here
   BYBIT_API_SECRET=your_api_secret_here
   ```

2. 在 `config.toml` 中配置提现参数：
   - 设置提现币种和网络
   - 设置最小和最大提现金额
   - 设置最小和最大延迟时间
   - 设置金额小数位数
   - 启用需要使用的交易所（设置 `enable = true`）

3. 在 `地址.txt` 中添加提现目标钱包地址列表

## 使用方法

1. 确保已完成所有配置
2. 运行程序：
   ```bash
   python main.py
   ```

## 安全建议

- 永远不要将 `.env` 文件提交到版本控制系统
- 将 `.env` 添加到 `.gitignore` 文件中
- 定期更换API密钥
- 使用最小权限原则设置API密钥权限
- 妥善保管API密钥信息

## 注意事项

- 请确保API密钥具有提现权限
- 建议先使用小额测试
- 建议在提现前检查网络费用

## 免责声明

本工具仅供学习和研究使用，使用本工具产生的任何风险由使用者自行承担。 
