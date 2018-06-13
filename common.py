from enum import Enum


class L1_CHANNEL_ID(Enum):
    L1_CHANNEL_OTHER = 0
    L1_CHANNEL_SPORTS = 1
    L1_CHANNEL_TECH = 2
    L1_CHANNEL_ENT = 3
    L1_CHANNEL_AUTO = 4
    L1_CHANNEL_FASHION = 5
    L1_CHANNEL_ASTRO = 6
    L1_CHANNEL_HOUSE = 7
    L1_CHANNEL_DIGITAL = 8
    L1_CHANNEL_FINANCE = 9
    L1_CHANNEL_GAME = 10
    L1_CHANNEL_MIL = 11
    L1_CHANNEL_SOCIAL = 12
    L1_CHANNEL_CUL = 13
    L1_CHANNEL_POLITICS = 14
    L1_CHANNEL_ANIMATION = 33


channel_id_to_name = {
    0: 'other',         # 其它
    1: 'sports',        # 体育
    2: 'tech',          # 科技
    3: 'ent',           # 娱乐
    4: 'auto',          # 汽车
    5: 'women',         # 时尚
    6: 'astro',         # 占卜
    7: 'house',         # 房产
    8: 'digital',       # 数码
    9: 'finance',       # 财经
    10: 'game',         # 游戏
    11: 'mil',          # 军事
    12: 'social',       # 社会
    13: 'cul',          # 文化
    14: 'politics',     # 时政
    15: 'baby',         # 亲子
    16: 'edu',          # 教育
    17: 'food',         # 美食
    18: 'funny',        # 搞笑
    19: 'religion',     # 宗教
    20: 'health',       # 健康
    21: 'travel',       # 旅游
    23: 'pet',          # 宠物
    24: 'inspiration',  # 心灵鸡汤
    28: 'weather',      # 天气
    29: 'history',      # 历史
    30: 'emotion',      # 情感
    32: 'beauty',       # 美女
    33: 'comic',        # 动漫
    35: 'abroad',       # 出国
    36: 'agriculture',  # 农林牧副渔
    37: 'creativity',   # 创意设计
    38: 'houseliving',  # 家居
    39: 'law',          # 法规
    40: 'lifestyle',    # 生活方式
    41: 'lottery',      # 彩票
    42: 'science',      # 科学
    43: 'photography',  # 摄影
    44: 'career',       # 职场
    45: 'life',         # 生活百科
    51: 'novel',        # 小说 (看点)
    52: 'live',         # 直播 (看点)
}

channel_name_to_id = {v: k for k, v in channel_id_to_name.items()}
