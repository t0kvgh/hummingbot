import asyncio
from unittest import TestCase

import hummingbot.strategy.dev_4_twap.dev_4_twap_config_map as twap_config_map_module


class TwapConfigMapTests(TestCase):

    def test_trading_pair_prompt(self):
        twap_config_map_module.dev_4_twap_config_map.get("exchange").value = "binance"
        self.assertEqual(twap_config_map_module.trading_pair_prompt(),
                         "Enter the token trading pair you would like to trade on binance (e.g. ZRX-ETH) >>> ")

        twap_config_map_module.dev_4_twap_config_map.get("exchange").value = "undefined-exchange"
        self.assertEqual(twap_config_map_module.trading_pair_prompt(),
                         "Enter the token trading pair you would like to trade on undefined-exchange >>> ")

    def test_target_asset_amount_prompt(self):
        twap_config_map_module.dev_4_twap_config_map.get("trading_pair").value = "BTC-USDT"
        twap_config_map_module.dev_4_twap_config_map.get("trade_side").value = "buy"
        self.assertEqual(twap_config_map_module.target_asset_amount_prompt(),
                         "What is the total amount of USDT to be traded? >>> ")

        twap_config_map_module.dev_4_twap_config_map.get("trade_side").value = "sell"
        self.assertEqual(twap_config_map_module.target_asset_amount_prompt(),
                         "What is the total amount of BTC to be traded? >>> ")

    def test_trade_side_config(self):
        config_var = twap_config_map_module.dev_4_twap_config_map.get("trade_side")

        self.assertTrue(config_var.required)

        prompt_text = asyncio.get_event_loop().run_until_complete(config_var.get_prompt())
        self.assertEqual(prompt_text, "What operation will be executed? (buy/sell) >>> ")

    def test_trade_side_only_accepts_buy_or_sell(self):
        config_var = twap_config_map_module.dev_4_twap_config_map.get("trade_side")

        validate_result = asyncio.get_event_loop().run_until_complete(config_var.validate("invalid value"))
        self.assertEqual(validate_result, "Invalid operation type.")

        validate_result = asyncio.get_event_loop().run_until_complete(config_var.validate("buy"))
        self.assertIsNone(validate_result)

        validate_result = asyncio.get_event_loop().run_until_complete(config_var.validate("sell"))
        self.assertIsNone(validate_result)
