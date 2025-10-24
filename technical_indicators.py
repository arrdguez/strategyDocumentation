"""
Technical Indicators Module
Calculates EMA(10,55,200), ADX, SMI, ATR
Uses exact same implementations as SMI.py
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import structlog


class TechnicalIndicators:
    """Unified technical indicators calculator using SMI.py implementations"""
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
    
    def calculate_all_indicators(self, df, 
                               ema_periods=None,
                               adx_period=14,
                               atr_period=14,
                               smi_period=18,
                               bb_length=18,
                               bb_mult=2.0,
                               kc_length=18,
                               kc_mult=1.5,
                               use_true_range=True):
        """
        Calculate all technical indicators for trading analysis
        Uses exact same implementations as SMI.py
        """
        
        if ema_periods is None:
            ema_periods = [10, 55, 200]
            
        self.logger.info(f"Calculating technical indicators: EMA{ema_periods}, ADX{adx_period}, ATR{atr_period}, SMI{smi_period}")
        
        # Make a copy to avoid modifying original
        result_df = df.copy()
        
        # Calculate EMAs
        for period in ema_periods:
            result_df[f'ema{period}'] = self.calculate_ema(result_df, period)
        
        # Calculate ADX (using SMI.py implementation)
        result_df['adx'] = self.calculate_adx_smi_style(result_df, adx_period)
        
        # Calculate ATR (using SMI.py implementation)
        result_df['atr'] = self.calculate_atr_smi_style(result_df)
        
        # Calculate SMI (using SMI.py implementation)
        result_df['smi'] = self.calculate_smi_smi_style(result_df, smi_period)
        
        # Calculate complete Squeeze Momentum Indicator (using Pine Script parameters)
        squeeze_momentum, squeeze_state = self.calculate_squeeze_momentum(
            result_df, bb_length=18, bb_mult=2.0, kc_length=20, kc_mult=1.5, use_true_range=True
        )
        result_df['squeeze_momentum'] = squeeze_momentum
        result_df['squeeze_state'] = squeeze_state
        
        # Add squeeze state as numeric values for visualization
        result_df['squeeze_state_numeric'] = self._convert_squeeze_state_to_numeric(squeeze_state)
        
        self.logger.info(f"Technical indicators calculation completed")
        
        return result_df
    
    def calculate_ema(self, df, period):
        """Calculate Exponential Moving Average"""
        return df['close'].ewm(span=period, adjust=False).mean()
    
    def calculate_adx_smi_style(self, df, period=14):
        """Calculate ADX using exact same implementation as SMI.py"""
        df_tmp = pd.DataFrame()
        df_tmp['open'] = df['open']
        df_tmp['high'] = df['high']
        df_tmp['low'] = df['low']
        df_tmp['close'] = df['close']
        df_tmp['up'] = df['high'].diff()
        df_tmp['down'] = -df['low'].diff()
        df_tmp['up'] = df_tmp['up'].fillna(0)
        df_tmp['down'] = df_tmp['down'].fillna(0)
        
        # Calculate True Range (manual implementation)
        df_tmp['TR'] = self._calculate_true_range(df)
        df_tmp['truerange'] = self._calculate_smma(df_tmp, period=14, column="TR", adjust=True)
        
        df_tmp = df_tmp.fillna(0)

        for i in range(0, len(df_tmp['close'])):
            if (df_tmp.loc[i,"up"] > df_tmp.loc[i,"down"]) & (df_tmp.loc[i,"up"] > 0):
                df_tmp.loc[i, 'plus'] = df_tmp.loc[i, 'up']
            else:
                df_tmp.loc[i, 'plus'] = 0
            if (df_tmp.loc[i,"down"] > df_tmp.loc[i,"up"]) & (df_tmp.loc[i,"down"] > 0):
                df_tmp.loc[i, 'minus'] = df_tmp.loc[i, 'down']
            else:
                df_tmp.loc[i, 'minus'] = 0

        df_tmp['plus'] = df_tmp['plus'].fillna(0)
        df_tmp['minus'] = df_tmp['minus'].fillna(0)

        df_tmp['plus'] = self._calculate_smma(df_tmp, period=14, column='plus', adjust=True)
        df_tmp['minus'] = self._calculate_smma(df_tmp, period=14, column='minus', adjust=True)

        df_tmp['plus'] = 100 * df_tmp['plus'] / df_tmp['truerange']
        df_tmp['minus'] = 100 * df_tmp['minus'] / df_tmp['truerange']

        df_tmp['sum'] = df_tmp['minus'] + df_tmp['plus']

        for i in range(0, len(df_tmp['sum'])):
          if float(df_tmp.loc[i,'sum']) == 0:
              df_tmp.loc[i,'tmp'] = abs(df_tmp.loc[i,'plus'] - df_tmp.loc[i,'minus']) / 1
          else:
              df_tmp.loc[i,'tmp'] = abs(df_tmp.loc[i,'plus'] - df_tmp.loc[i,'minus']) / df_tmp.loc[i,'sum']

        df_tmp['ADX'] = 100 * self._calculate_smma(df_tmp, period=period, column='tmp', adjust=True)

        return df_tmp['ADX']
    
    def calculate_atr_smi_style(self, df):
        """Calculate ATR using exact same implementation as SMI.py"""
        # Manual ATR calculation matching SMI.py style
        high = df['high']
        low = df['low']
        close = df['close']
        
        # True Range calculation
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # ATR as 14-period SMA of True Range
        atr = tr.rolling(window=14).mean()
        
        # Convert to pandas Series and fill NaN
        atr_series = pd.Series(atr, index=df.index)
        atr_series = atr_series.fillna(0)
        
        return atr_series
    
    def calculate_smi_smi_style(self, df, kclength=18):
        """Calculate SMI using exact same implementation as SMI.py"""
        df_tem = pd.DataFrame()
        df_tem['close'] = df['close']
        df_tem['sma'] =  df['close'].rolling(window = kclength).mean()
        df_tem['highest'] = df["high"].rolling(center=False, window = kclength).max()
        df_tem['lowest'] = df["low"].rolling(center=False, window = kclength).min()
        df_tem['aveHL'] = (df_tem['lowest'] + df_tem['highest'])/2
        df_tem['aveHLS'] = (df_tem['aveHL'] + df_tem['sma'])/2
        df_tem['source'] = df['close'] - df_tem['aveHLS']
        df_tem = df_tem.fillna(0)

        y_all = df_tem['source'].values.tolist()
        x = np.array(list(range(1, kclength+1))).reshape((-1, 1))

        smh = []
        for i in range(len(df_tem['close'])-1, kclength*2, -1):
            y = np.array(y_all[i-kclength+1:i+1])
            reg = LinearRegression(fit_intercept = True).fit(x, y)
            smh.append(reg.predict(x)[-1])

        tmp = [0 for _ in range(len(y_all)-len(smh))]
        smh = smh + tmp
        smh.reverse()

        return pd.Series(smh, name="{0} period SMI".format(kclength))
    
    def calculate_squeeze_momentum(self, df, bb_length=18, bb_mult=2.0, kc_length=20, kc_mult=1.5, use_true_range=True):
        """
        Calculate complete Squeeze Momentum Indicator with Bollinger Bands and Keltner Channel
        Based on LazyBear's implementation - Updated to match Pine Script exactly
        """
        # Calculate Bollinger Bands
        source = df['close']
        basis = source.rolling(window=bb_length).mean()
        dev = bb_mult * source.rolling(window=bb_length).std()
        upper_bb = basis + dev
        lower_bb = basis - dev
        
        # Calculate Keltner Channel
        ma = source.rolling(window=kc_length).mean()
        
        if use_true_range:
            # Calculate True Range
            tr1 = df['high'] - df['low']
            tr2 = (df['high'] - df['close'].shift()).abs()
            tr3 = (df['low'] - df['close'].shift()).abs()
            t_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        else:
            t_range = df['high'] - df['low']
            
        range_ma = t_range.rolling(window=kc_length).mean()
        upper_kc = ma + range_ma * kc_mult
        lower_kc = ma - range_ma * kc_mult
        
        # Calculate squeeze states (EXACTLY as in Pine Script)
        sqz_on = (lower_bb > lower_kc) & (upper_bb < upper_kc)
        sqz_off = (lower_bb < lower_kc) & (upper_bb > upper_kc)
        no_sqz = (~sqz_on) & (~sqz_off)
        
        # Calculate squeeze momentum value (EXACTLY as in Pine Script)
        highest_high = df['high'].rolling(window=kc_length).max()
        lowest_low = df['low'].rolling(window=kc_length).min()
        avg_hl = (highest_high + lowest_low) / 2
        sma_close = df['close'].rolling(window=kc_length).mean()
        avg_hl_sma = (avg_hl + sma_close) / 2
        
        # This matches the Pine Script calculation: source - math.avg(math.avg(highest, lowest), sma(close))
        source_val = df['close'] - avg_hl_sma
        
        # Linear regression for momentum (matching ta.linreg)
        squeeze_momentum = []
        for i in range(len(source_val)):
            if i >= kc_length - 1:
                y = source_val.iloc[i-kc_length+1:i+1].values
                x = np.array(range(1, kc_length+1)).reshape(-1, 1)  # Start from 1 like Pine Script
                if len(y) == kc_length and not np.any(np.isnan(y)):
                    reg = LinearRegression(fit_intercept=True).fit(x, y)
                    # Predict the last value (kc_length) like Pine Script's ta.linreg
                    squeeze_momentum.append(reg.predict([[kc_length]])[0])
                else:
                    squeeze_momentum.append(0)
            else:
                squeeze_momentum.append(0)
        
        squeeze_momentum = pd.Series(squeeze_momentum, index=df.index)
        
        # Create squeeze state column using Pine Script naming
        squeeze_state = pd.Series('no_squeeze', index=df.index)
        squeeze_state[sqz_on] = 'squeeze_on'
        squeeze_state[sqz_off] = 'squeeze_off'
        
        return squeeze_momentum, squeeze_state
    
    def _calculate_true_range(self, df):
        """Calculate True Range manually"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        
        return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    def _calculate_smma(self, df, period=14, column="TR", adjust=True):
        """Calculate Smoothed Moving Average (SMMA)"""
        # SMMA is equivalent to EMA with adjust=False
        return df[column].ewm(span=period, adjust=adjust).mean()
    
    def _convert_squeeze_state_to_numeric(self, squeeze_state):
        """Convert squeeze state to numeric values for visualization"""
        state_mapping = {
            'squeeze_on': 1,
            'squeeze_off': -1,
            'no_squeeze': 0
        }
        return squeeze_state.map(state_mapping)


# Singleton instance for easy access
indicators = TechnicalIndicators()