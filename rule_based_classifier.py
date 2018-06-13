import xml.etree.ElementTree as ET
from datetime import date, timedelta
import re
from typing import Dict, Pattern, Set

MAGIC_NUM_ALL_CATE = 6666


class Article:
    text: str
    channel_id: int
    push_time: date
    author: str

    def __init__(self, text, channel_id, push_time, author):
        self.text = text
        self.channel_id = channel_id
        self.push_time = push_time
        self.author = author


# 一般处理类
class CGeneralProc:
    media_accounts: Set[str]
    channel_ids: Set[int]
    channel_2_pattern: Dict[int, Pattern[str]]

    def __init__(self, conf: str):
        tree = ET.parse(conf)
        root = tree.getroot()

        file_name = root.find('general_proc').text
        last_id = None
        channel_2_pattern = {}
        patterns = []
        for line in open(file_name, encoding='utf-8'):
            line = line.strip()
            if line:
                if ':' in line and len(line.split(':')) == 3:
                    _, channel_id, _ = line.split(':')
                    last_id = int(channel_id)
                else:
                    patterns.append(line)
            else:
                channel_2_pattern[last_id] = re.compile('|'.join(patterns))
                patterns = []
        if patterns:
            channel_2_pattern[last_id] = re.compile('|'.join(patterns))
        self.channel_2_pattern = channel_2_pattern

        self.channel_ids = set(int(x) for x in root.find('allow_in_cid').text.split(','))

        media_account = set()
        file_name = root.find('account_list').text
        for line in open(file_name, encoding='utf-8'):
            line = line.strip()
            if line:
                media_account.add(line)
        self.media_accounts = media_account

    def is_account_timely(self, article: Article):
        if article.channel_id not in self.channel_ids:
            return False
        return article.author in self.media_accounts

    def is_content_timely(self, article: Article):
        bIsTimely = False
        bUncerPhrase = False  # 包含不定时间的短语
        bHasIndicateTime = False  # 有确定的时间短语
        specExpireTime = None  # 文本包含具体时间
        if article.channel_id not in self.channel_ids:
            return False
        yesterday = article.push_time - timedelta(1)
        pattern = self.channel_2_pattern[MAGIC_NUM_ALL_CATE]
        for word in pattern.finditer(article.text):
            word = word.group()
            if re.match("((\\d+年)?\\d+月)?\\d{1,2}([^0-9月]\\d{1,2})?日", word):
                bHasIndicateTime = True
                year = article.push_time.year
                month = article.push_time.month
                try:
                    # 处理如：4月25-26日，4月25、26日这种情况,去掉后面这个数字(-26)
                    word = self.discard_range_date(word)
                    if '年' in word:
                        year, month, day = [int(x) for x in re.match(r'(\d+)年(\d+)月(\d+)日', word).groups()]
                    elif '月' in word:
                        month, day = [int(x) for x in re.match(r'(\d+)月(\d+)日', word).groups()]
                    else:
                        day, = [int(x) for x in re.match(r'(\d+)日', word).groups()]
                    text_time = date(year, month, day)
                    bIsTimely = True
                    if specExpireTime == None or text_time > specExpireTime:
                        specExpireTime = text_time
                except Exception:
                    continue
            elif '今' in word:
                # 今天就来...这样的短语不一定是描写当前的一个事件
                if (word[-1] in ['就', '想', '要', '来', '跟', '为', '给', '和', '说', '讲']
                        or word.startswith('在')
                        or word.startswith('的')
                        or word.startswith('今时')
                        or word.startswith('到')):
                    continue
                else:
                    bIsTimely = True
            elif '昨' in word:
                bIsTimely = True
            else:
                bUncerPhrase = True
        # 先判断具体时间是否已经过期，如果过期，则认为文章不具有时效性
        if bHasIndicateTime and specExpireTime is not None and specExpireTime < yesterday:
            bIsTimely = False
        # 因为没有确定时间短语造成的判断
        if not bIsTimely and not bHasIndicateTime and bUncerPhrase:
            bIsTimely = True
        # 走分类识别
        if not bIsTimely:
            bIsTimely = self.is_timely_in_category(article)
        return bIsTimely

    def is_timely_in_category(self, article: Article):
        if article.channel_id not in self.channel_2_pattern:
            return False
        pattern = self.channel_2_pattern[article.channel_id]
        if pattern.search(article.text):
            return True

    @staticmethod
    def discard_range_date(word: str):
        if re.search("[^0-9月]\\d{1,2}日", word):
            if '月' in word:
                day_offset = word.find('月') + 1
            elif word[0].isdigit():
                day_offset = 0
            else:
                return word
            for div_offset in range(day_offset, len(word)):
                if not word[div_offset].isdigit():
                    break
            word = word[:day_offset] + word[div_offset+1:]
        return word

    def is_timely(self, article: Article):
        return self.is_content_timely(article) or self.is_account_timely(article)


if __name__ == '__main__':
    general_proc = CGeneralProc('kd_content_mining.xml')
    print(general_proc.channel_2_pattern)
    print(general_proc.channel_ids)
    print(general_proc.media_accounts)
