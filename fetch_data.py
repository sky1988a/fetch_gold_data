import requests
import sqlite3
import time

# 数据库文件路径
DB_FILE = 'gold_prices.db'

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS gold_prices
                 (date TEXT PRIMARY KEY, price REAL)''')
    conn.commit()
    conn.close()

# 获取数据并插入数据库
def get_and_insert_data():
    url = 'https://api.jdjygold.com/gw/generic/hj/h5/m/todayLatestPrices'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        datas = data.get('resultData', {}).get('datas', [])
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        for item in datas:
            date = item.get('name')
            price = float(item.get('value', [])[1])
            try:
                c.execute("INSERT INTO gold_prices (date, price) VALUES (?,?)", (date, price))
            except sqlite3.IntegrityError:
                # 如果日期已存在，忽略
                pass
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# 主程序
if __name__ == "__main__":
    init_db()
    while True:
        get_and_insert_data()
        time.sleep(5)
