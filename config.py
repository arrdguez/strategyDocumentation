"""
Configuration module for Trading Data Labeling System
"""

import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TradingConfig:
    """Configuration for trading data parameters"""
    
    # Trading parameters
    symbol: str = "BTCUSDT"
    interval: str = "4h"
    limit: int = 1000
    
    # Technical indicators
    ema_periods: list = None  # type: ignore
    adx_period: int = 14
    atr_period: int = 14
    smi_period: int = 18
    
    # Output settings
    output_dir: str = "data/processed"
    raw_dir: str = "data/raw"
    exports_dir: str = "data/exports"
    label_studio_config: str = "label_studio_config.xml"
    
    def get_output_filename(self) -> str:
        """Generate automatic filename: SYMBOL_INTERVAL_timestamp.csv"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.symbol}_{self.interval}_{timestamp}.csv"
    
    def __post_init__(self):
        if self.ema_periods is None:
            self.ema_periods = [10, 55, 200]


class ConfigLoader:
    """Load configuration from file or environment"""
    
    @staticmethod
    def from_dict(config_dict: Dict[str, Any]) -> TradingConfig:
        """Create config from dictionary"""
        return TradingConfig(**config_dict)
    
    @staticmethod
    def from_env() -> TradingConfig:
        """Create config from environment variables"""
        return TradingConfig(
            symbol=os.getenv('TRADING_SYMBOL', 'BTCUSDT'),
            interval=os.getenv('TRADING_INTERVAL', '4h'),
            limit=int(os.getenv('TRADING_LIMIT', '1000'))
        )
    
    @staticmethod
    def default() -> TradingConfig:
        """Return default configuration"""
        return TradingConfig()


# Global configuration instance
config = ConfigLoader.default()