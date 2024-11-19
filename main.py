import base64
import json
import re
import execjs
import requests
from loguru import logger
from urllib.parse import urljoin
import pandas as pd


class AqiScraper(object):

    def __init__(self):
        self.root_url = 'https://www.aqistudy.cn'
        self.session = requests.Session()
        self.output_path = "output.txt"
        self.js_pattern_path = './js/encrypt_e9OKk3qfXQqT.js'
        self.js_pattern = self.read_js_pattern(self.js_pattern_path)

    def read_js_pattern(self, js_pattern_path):
        """
        read template js file
        :param js_pattern_path:
        :return: 
        """
        with open(js_pattern_path, 'r', encoding='utf-8') as f:
            js_pattern = f.read()
        return js_pattern

    def get_js_code(self):
        """
        3.encrypt_e9OKk3qfXQqT.js 动态返回 --> GET https://www.aqistudy.cn/html/city_realtime.php?v=2.3 提取js链接 请求
        :return:
        """
        url = f'{self.root_url}/html/city_detail.php?v=1.10'
        logger.info(url)
   
        headers = {
            'Referer': 'https://www.aqistudy.cn/?mobile=false',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                          'Chrome/100.0.4896.127 Safari/537.36'
        }
        response = self.session.get(url, headers=headers)
        logger.info(response)
        response_str = response.content.decode('utf-8', 'ignore')
        # logger.info(response_str)

        # regex search for encrypted js file
        search_js_path = re.search(r'src=["\']\.\./js/encrypt_\w+\.js\?v=\d+["\']', response_str)
        logger.info(search_js_path)

        # extract file path
        js_code_path = search_js_path.group(0).split('"')[1] if search_js_path else ''
        # join path with root URL, get url for encrypted js file
        js_code_url = urljoin(self.root_url, js_code_path)
        logger.info(f'{js_code_url}')

        # get content from encrypted js file
        js_code_resp = requests.get(js_code_url, headers=headers)
        js_code = js_code_resp.content.decode('utf-8', 'ignore')
        # logger.info(f'{js_code}')

        return js_code

    def decode_js_code(self, js_code):
        """
        4.解密encrypt_e9OKk3qfXQqT.js
        :param js_code:
        :return:
        """
        while True:
            if js_code.startswith('eval(function'):
                js_code = js_code[5:-2]
                js_pattern = self.js_pattern.replace('js_code_pattern', js_code)
                js_pattern_compile = execjs.compile(js_pattern)
                js_code = js_pattern_compile.call('run_js_code')
            elif js_code.startswith('eval(dswejwehxt'):
                count_dswejwehxt = js_code.count('dswejwehxt')
                search_base64_js_code = re.search(r"'(.*?)'", js_code)
                base64_js_code = search_base64_js_code.group(1) if search_base64_js_code else ''
                for _ in range(count_dswejwehxt):
                    base64_js_code = base64.b64decode(base64_js_code).decode('utf-8')
                js_code = base64_js_code
            else:
                break

        # logger.info(f'\n{js_code}')
        return js_code

    def get_all_js_code(self, js_code):
        """
        5.补充执行环境依赖 https://www.aqistudy.cn/js/jquery.min.js?v=1.3 静态返回
        :param js_code:
        :return:
        """
        all_js_code = f'{self.js_pattern}\n{js_code}'
        # logger.info(all_js_code)
        all_js_code_compile = execjs.compile(all_js_code)
        return all_js_code, all_js_code_compile

    def get_names(self, all_js_code):
        """
        6.提取 加密函数名称 data加密参数名称 解密函数名称
        :param all_js_code:
        :return:
        """
        # 加密函数名称
        search_encrypt_func_name = re.search(r'var\s*(\w+?)\s*=\s*\(function\s*\(\)\s*{', all_js_code, re.S)
        encrypt_func_name = search_encrypt_func_name.group(1) if search_encrypt_func_name else ''

        # 加密参数名称
        search_param_name = re.search(r'data:\s*{\s*(\w+):\s*(\w+)\s*},', all_js_code, re.S)
        param_name = search_param_name.group(1) if search_param_name else ''

        # 解密函数名称
        search_decrypt_func_name = re.search(
            r'success:\s*function\s*\(\w+\)\s*{\s*\w+\s*=\s*(\w+)\(\w+\);', all_js_code, re.S)
        decrypt_func_name = search_decrypt_func_name.group(1) if search_decrypt_func_name else ''

        logger.info(f'{encrypt_func_name}, {param_name}, {decrypt_func_name}')
        return encrypt_func_name, param_name, decrypt_func_name

    def get_city_data(self, all_js_code_compile, encrypt_func_name, param_name, method, parameters):
        """
        7.执行加密函数 请求
        :return:
        """
        param_ret = all_js_code_compile.call(encrypt_func_name, method, parameters)
        # logger.info(f'Parameters: {param_name} {param_ret}')

        response_str = self.get_aqistudyapi_request(param_name, param_ret)
        # logger.info(f'Responses: {response_str}')
        return response_str

    def get_aqistudyapi_request(self, param_name, param_ret):
        url = f'{self.root_url}/apinew/aqistudyapi.php'
        data = {
            f'{param_name}': param_ret
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://www.aqistudy.cn/html/city_detail.php?v=1.10',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        response = requests.post(url, headers=headers, data=data)
        response_str = response.content.decode('utf-8')
        return response_str

    def decrypt_resp(self, all_js_code_compile, decrypt_func_name, response_str):
        """
        解密响应
        """
        ret = all_js_code_compile.call(decrypt_func_name, response_str)
        response_dict = json.loads(ret)
        logger.info(response_dict)
        return response_dict
    
    def write_data(self, air_quality_data, weather_data):
        air_quality_df = pd.DataFrame(air_quality_data['result']['data']['rows'])
        weather_df = pd.DataFrame(weather_data['result']['data']['rows'])
        print(weather_df.dtypes)
        
        # 处理时间戳不一致
        weather_df["time"] = pd.to_datetime(weather_df["time"])  # 确保时间列是 datetime 类型
        air_quality_df["time"] = pd.to_datetime(air_quality_df["time"])
        weather_df["time"] = weather_df["time"].dt.round("h")
        print(weather_df.dtypes)

        # 合并数据
        merged_df = pd.merge_asof(
            air_quality_df.sort_values("time"),
            weather_df.sort_values("time"),
            on="time",
            direction="nearest"  # 根据最近的时间戳合并
        )

        '''
        merged_df = pd.merge(
                            air_quality_df, weather_df,
                            on='time', 
                            how='outer'
                        )        
        '''

        logger.info(merged_df)
        merged_df.to_csv(self.output_path, index=False, encoding='utf-8')
        return 
        
    def run(self):
        js_code = self.get_js_code()

        js_code = self.decode_js_code(js_code)

        all_js_code, all_js_code_compile = self.get_all_js_code(js_code)

        encrypt_func_name, param_name, decrypt_func_name = self.get_names(all_js_code)

        parameters = {
            "city": "金华",
            "startTime": "2014-02-01 00:00:00",
            "endTime": "2014-02-28 23:00:00",
            "type": "HOUR"
        }

        method1 = "GETDETAIL"
        method2 = "GETCITYWEATHER"

        air_quality_response = self.get_city_data(all_js_code_compile, encrypt_func_name, param_name, method1, parameters)
        weather_response = self.get_city_data(all_js_code_compile, encrypt_func_name, param_name, method2, parameters)
        air_quality_data = self.decrypt_resp(all_js_code_compile, decrypt_func_name, air_quality_response)
        weather_data = self.decrypt_resp(all_js_code_compile, decrypt_func_name, weather_response)
        self.write_data(air_quality_data, weather_data)

if __name__ == '__main__':
    aqi_scraper = AqiScraper()
    aqi_scraper.run()