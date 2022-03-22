# -*- coding: utf-8 -*-
from .default import DevelopmentConfig
from .default import ProductConfig

# 区分不同环境字符串映射
map_config = {
    'develop': DevelopmentConfig,
    'product': ProductConfig
}
