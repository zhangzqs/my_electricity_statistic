import requests
from config import config
from dataclasses import dataclass
import json
from file_read_backwards import FileReadBackwards
from typing import Optional
import os.path

@dataclass
class ReadTime:
    month: int
    day: int
    hour: int
    minute: int

    @staticmethod
    def parse(s: str):
        md, ms = s.split(' ')
        month, day = md.split('-')
        hour, minute = ms.split(':')
        return ReadTime(int(month), int(day), int(hour), int(minute))

    def __str__(self):
        return f'{self.month}-{self.day} {self.hour}:{self.minute}'

@dataclass
class DataEntity:
    ts: ReadTime
    balance: float

    @staticmethod
    def parse(dic):
        return DataEntity(
            balance = dic['data']['spareElec'],
            ts = ReadTime.parse(dic['data']['readTime'])
        )
    

def get_local_last() -> Optional[DataEntity]:
    if not os.path.isfile(config.data_file):
        return None
    with FileReadBackwards(path=config.data_file, encoding='utf-8') as f:
        try:
            return DataEntity.parse(json.loads(f.readline()))
        except Exception:
            return None

# 保存到文件末尾
def get_last() -> DataEntity:
    response = requests.get(
        url='https://bzp.iyunmu.com/prepaid/device/meter?sn=YM002272EDA2&userid=', 
        params={'sn': config.sn, 'userid': ''},
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
    )
    record = response.json()
    e = DataEntity.parse(record)
    local_last = get_local_last()
    
    if local_last is None or e.ts != local_last.ts:
        with open(file=config.data_file, encoding='utf-8', mode='a') as f:
            f.write(f"{json.dumps(obj=record, ensure_ascii=False)}\n")
    return e

def get_recently_by_cnt(cnt: int):
    if not os.path.isfile(config.data_file):
        return []
    with FileReadBackwards(config.data_file, encoding="utf-8") as frb:
        i = 0
        for line in frb:
            if i<cnt:
                i += 1
                yield DataEntity.parse(json.loads(line))
            else:
                break

def draw_recently_by_cnt(cnt):
    import matplotlib.pyplot as plt
    from io import BytesIO
    
    logs = list(reversed(list(get_recently_by_cnt(cnt))))
    plt.clf()
    xs = list(map(lambda x: f'{x.ts.hour}', logs))
    ys = list(map(lambda x: x.balance, logs))
    print([xs, ys])
    plt.plot(xs, ys)

    plt.show()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    return buf

draw_recently_by_cnt(24)

__all__ = [
    'get_last',
    'draw_recently_by_cnt',
]