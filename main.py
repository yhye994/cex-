import ccxt
import toml
import random
import time
import logging
from decimal import Decimal, ROUND_DOWN
from typing import List, Dict
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WithdrawalManager:
    def __init__(self, config_path: str = 'config.toml'):
        self.config = self._load_config(config_path)
        self.exchanges = self._init_exchanges()
        self.wallets = self._load_wallets()
        self.max_retries = 3  # 最大重试次数
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            return toml.load(config_path)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise

    def _load_wallets(self) -> List[str]:
        """加载钱包地址列表"""
        try:
            with open('地址.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"加载钱包地址失败: {e}")
            raise

    def _get_api_credentials(self, exchange_id: str) -> Dict[str, str]:
        """从环境变量获取API凭证"""
        credentials = {}
        exchange_id = exchange_id.upper()
        
        # 获取API密钥
        api_key = os.getenv(f"{exchange_id}_API_KEY")
        api_secret = os.getenv(f"{exchange_id}_API_SECRET")
        
        if not api_key or not api_secret:
            raise ValueError(f"未找到 {exchange_id} 的API凭证")
            
        credentials['apiKey'] = api_key
        credentials['secret'] = api_secret
        
        # 对于需要passphrase的交易所（如OKX）
        if exchange_id == 'OKX':
            passphrase = os.getenv(f"{exchange_id}_PASSPHRASE")
            if not passphrase:
                raise ValueError(f"未找到 {exchange_id} 的PASSPHRASE")
            credentials['password'] = passphrase
            
        return credentials

    def _init_exchanges(self) -> Dict[str, ccxt.Exchange]:
        """初始化交易所实例"""
        exchanges = {}
        for exchange_id, config in self.config['exchanges'].items():
            if config.get('enable', False):
                try:
                    exchange_class = getattr(ccxt, exchange_id)
                    credentials = self._get_api_credentials(exchange_id)
                    exchange = exchange_class({
                        **credentials,
                        'enableRateLimit': True
                    })
                    exchanges[exchange_id] = exchange
                    logger.info(f"成功初始化交易所: {exchange_id}")
                except Exception as e:
                    logger.error(f"初始化交易所 {exchange_id} 失败: {e}")
        return exchanges

    def _generate_random_amount(self) -> float:
        """生成随机提现金额"""
        min_amount = self.config['withdrawal']['min_amount']
        max_amount = self.config['withdrawal']['max_amount']
        decimal_places = self.config['withdrawal']['decimal_places']
        
        amount = random.uniform(min_amount, max_amount)
        return float(Decimal(str(amount)).quantize(
            Decimal('0.' + '0' * decimal_places),
            rounding=ROUND_DOWN
        ))

    def _get_random_delay(self) -> int:
        """生成随机延迟时间"""
        min_delay = self.config['withdrawal']['min_delay']
        max_delay = self.config['withdrawal']['max_delay']
        return random.randint(min_delay, max_delay)

    def process_withdrawal(self, exchange_id: str, address: str):
        """处理单个提现请求"""
        exchange = self.exchanges[exchange_id]
        amount = self._generate_random_amount()
        
        for retry in range(self.max_retries):
            try:
                # 获取提现费用
                fees = exchange.fetch_deposit_withdraw_fees(
                    self.config['withdrawal']['coin']
                )
                
                # 执行提现
                withdrawal = exchange.withdraw(
                    code=self.config['withdrawal']['coin'],
                    amount=amount,
                    address=address,
                    tag=None,
                    params={
                        'network': self.config['withdrawal']['network']
                    }
                )
                
                logger.info(f"提现成功 - 交易所: {exchange_id}, 地址: {address}, "
                           f"金额: {amount} {self.config['withdrawal']['coin']}")
                
                return withdrawal
            except Exception as e:
                logger.error(f"提现失败 (尝试 {retry + 1}/{self.max_retries}) - "
                           f"交易所: {exchange_id}, 地址: {address}, 错误: {str(e)}")
                if retry < self.max_retries - 1:
                    time.sleep(5)  # 失败后等待5秒再重试
                else:
                    logger.error(f"达到最大重试次数，跳过此提现")
                    return None

    def start_withdrawals(self):
        """开始批量提现流程"""
        try:
            for address in self.wallets:
                for exchange_id in self.exchanges:
                    self.process_withdrawal(exchange_id, address)
                    delay = self._get_random_delay()
                    logger.info(f"等待 {delay} 秒后继续...")
                    time.sleep(delay)
        except KeyboardInterrupt:
            logger.info("程序被用户中断")
            return

def main():
    try:
        manager = WithdrawalManager()
        manager.start_withdrawals()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")

if __name__ == "__main__":
    main() 