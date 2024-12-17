import requests
import json
import getTime
import zipfile
import os

userid='' #Changeit
demoPath = './demo'  # 替换为实际demo解压路径

# 请求的URL
url_getuuid = 'https://gate.5eplay.com/userinterface/http/v1/userinterface/idTransfer'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_uuid(url, payload):
    try:
        # 发送POST请求
        response = requests.post(url, json=payload)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()
            
            # 假设uuid在响应的某个字段中，这里需要根据实际响应结构来定位uuid
            # 例如，如果uuid在响应的'data'字段中
            uuid = response_data.get('data', {}).get('uuid')
            return uuid
        else:
            return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        # 处理请求异常
        return f"An error occurred: {e}"


# 调用函数并打印结果
uuid = get_uuid(url_getuuid, {
    "trans": {
        "domain": userid
    }
})
print(f"The UUID is: {uuid}")

# 构造目标URL
url_getmatchid = f'https://gate.5eplay.com/crane/http/api/data/player_match?uuid={uuid}'


def get_matchids(url_getmatchid):
    response_getmatchid = requests.get(url_getmatchid, headers=headers)
# 检查请求是否成功
    if response_getmatchid.status_code == 200:
    # 解析JSON数据
        data = response_getmatchid.json()
    # 提取match_data列表
        match_data = data.get('data', {}).get('match_data', [])
    
    # 遍历match_data列表，提取每个match_id
        match_ids = [match['match_id'] for match in match_data]
        return match_ids

    else:
        print("Failed to retrieve data, status code:", response_getmatchid.status_code)

match_ids=get_matchids(url_getmatchid)
    

def get_demo_url(match_id):
    # 构造URL
    url = f'https://gate.5eplay.com/crane/http/api/data/match/{match_id}'
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()
            
            # 提取demo_url
            demo_url = response_data.get('data', {}).get('main', {}).get('demo_url')
            return demo_url
        else:
            return f"Failed to retrieve data for match {match_id}, status code: {response.status_code}"
    except requests.RequestException as e:
        # 处理请求异常
        return f"An error occurred while requesting match {match_id}: {e}"


# 循环遍历match_ids数组，并获取每个matchid的demo下载链接
demo_urls = {}
for match_id in match_ids:
    demo_url = get_demo_url(match_id)
    demo_urls[match_id] = demo_url

# 打印所有demo的下载链接
for match_id, demo_url in demo_urls.items():
    print(f"Demo URL for match {match_id}: {demo_url}")

# today_end_of_day_timestamp = getTime.get_end_of_day_timestamp()
# print("Today's end of day timestamp:", today_end_of_day_timestamp)

def download_file(url, local_filename):
    # 发起GET请求，设置stream=True以流式下载文件
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # 确保请求成功
        total_size = int(r.headers.get('content-length', 0))
        chunk_size = 8192  # 每次下载的块大小
        downloaded_size = 0  # 已下载的大小

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # 过滤掉保持连接的chunk
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    done = int(50 * downloaded_size / total_size)
                    print(f"\r[{'=' * done}{' ' * (50-done)}] {done * 2}%", end='')

    print("\nDownload completed!")
    return local_filename

def unzip_file(zip_path, demoPath):
    # 使用zipfile解压文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(demoPath)

def download_and_extract(url, demoPath):
    if not url:
        print("URL is empty, skipping download and extraction.")
        return
    # 从URL中提取文件名
    filename = url.split('/')[-1]
    # 下载文件
    local_filename = download_file(url, filename)
    # 解压文件
    unzip_file(local_filename, demoPath)
    # 删除ZIP文件
    os.remove(local_filename)
    print(f"File downloaded and extracted to {demoPath}")

# 使用函数
for _ , demo_url in demo_urls.items():
    download_and_extract(demo_url, demoPath)











