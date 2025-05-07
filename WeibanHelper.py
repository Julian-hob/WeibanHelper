"""
安全微课自动完成脚本
Author: Julian
Created: 2025/5/07
Description : 
"""

import requests
import time
import tqdm
import json
from typing import Dict, List


class SafetyCourseAutomation:
    def __init__(self, user_config: Dict):
        """初始化配置"""
        self.user_config = user_config
        self.headers = {
            'Cookie': user_config['cookie'],
            'User-Agent': user_config['User-Agent'],
            'X-Token': user_config['x_token']
        }
        self.base_data = {
            'tenantCode': user_config['tenant_code'],
            'userId': user_config['user_id'],
            'userProjectId': user_config['user_project_id'],
            'chooseType': 3
        }
        self.base_url = 'https://weiban.mycourse.cn/pharos'

    def get_timestamp(self) -> str:
        """获取时间戳"""
        return str(int(time.time() * 1000) / 1000)

    def sleep_with_progress(self, seconds: int):
        """带进度条的延时"""
        for _ in tqdm.tqdm(range(seconds)):
            time.sleep(1)

    def get_category_codes(self) -> List[str]:
        """获取所有课程分类代码"""
        url = f'{self.base_url}/usercourse/listCategory.do?timestamp={self.get_timestamp()}'
        response = requests.post(url, headers=self.headers, data=self.base_data)
        return [category["categoryCode"] for category in response.json()["data"]]

    def get_course_list(self, category_code: str) -> List[Dict]:
        """获取指定分类下的所有课程"""
        url = f'{self.base_url}/usercourse/listCourse.do?timestamp={self.get_timestamp()}'
        data = {**self.base_data, 'categoryCode': category_code}
        response = requests.post(url, headers=self.headers, data=data)
        return response.json()['data']

    def study_course(self, course_info: Dict):
        """学习单个课程"""
        resource_id = course_info['resourceId']
        user_course_id = course_info['userCourseId']
        resource_name = course_info['resourceName']

        # 开始学习
        study_data = {**self.base_data, 'courseId': resource_id}
        study_url = f'{self.base_url}/usercourse/study.do?timestamp={self.get_timestamp()}'
        requests.post(study_url, headers=self.headers, data=study_data)

        # 获取课程URL
        url_data = {**study_data}
        course_url = f'{self.base_url}/usercourse/getCourseUrl.do?timestamp={self.get_timestamp()}'
        course_response = requests.post(course_url, headers=self.headers, data=url_data)

        # 访问课程
        course_link = course_response.json()['data']
        params = {
            'userProjectId': self.user_config['user_project_id'],
            'userId': self.user_config['user_id'],
            'courseId': resource_id,
            'projectType': 'lab',
            'projectId': 'undefined',
            'protocol': 'true',
            'link': 39656,
            'weiban': 'weiban',
            'userName': self.user_config['user_name']
        }
        requests.get(course_link, headers=self.headers, params=params)

        # 等待学习时间
        self.sleep_with_progress(15)

        # 验证码处理
        self.handle_captcha(user_course_id)

        print(f'完成课程: {resource_name}')

    def handle_captcha(self, user_course_id: str):
        """处理验证码"""
        # 获取验证码
        captcha_url = f'{self.base_url}/usercourse/getCaptcha.do'
        captcha_params = {
            'userCourseId': user_course_id,
            'userProjectId': self.user_config['user_project_id'],
            'userId': self.user_config['user_id'],
            'tenantCode': self.user_config['tenant_code']
        }
        captcha_response = requests.post(captcha_url, params=captcha_params, headers=self.headers)
        question_id = captcha_response.json()['captcha']['questionId']

        # 提交验证码
        check_url = f'{self.base_url}/usercourse/checkCaptcha.do'
        check_params = {**captcha_params, 'questionId': question_id}
        check_data = {
            'coordinateXYs': '[{"x": 64, "y": 416}, {"x": 141, "y": 416}, {"x": 218, "y": 410}]'
        }
        requests.post(check_url, params=check_params, data=check_data, headers=self.headers)

        # 完成验证
        finish_url = f'{self.base_url}/usercourse/v2/{user_course_id}.do'
        finish_data = {
            'callback': f'jQuery34107900224573703418_{int(time.time())}',
            'userCourseId': user_course_id,
            'tenantCode': self.user_config['tenant_code'],
            '_': str(int(time.time()))
        }
        requests.post(finish_url, data=finish_data, headers=self.headers)

    def run(self):
        """运行主程序"""
        category_codes = self.get_category_codes()

        for category_code in category_codes:
            course_list = self.get_course_list(category_code)
            print(f'分类 {category_code} 共有 {len(course_list)} 个课程')

            for index, course in enumerate(course_list, 1):
                print(f'正在学习第 {index}/{len(course_list)} 个课程')
                self.study_course(course)

                # 课程间隔
                if index != len(course_list):
                    self.sleep_with_progress(1)
                else:
                    self.sleep_with_progress(3)


def main():
    """主函数"""
    user_config = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'user_id': '3ab448e9-8e58-4427-bfee-7c455dd4b920',
        'user_project_id': 'f476c86b-f76a-47b2-9844-d09752c0b3e6',
        'cookie': 'Hm_lvt_05399cc451ee10764eab39735c54698f=1746585178; HMACCOUNT=09AE6B5F8CFCEBEB; __root_domain_v=.mycourse.cn; _qddaz=QD.977446585178797; _qdda=3-1.1; _qddab=3-h4v27z.madbpx3v; Hm_lpvt_05399ccffcee10764eab39735c54698f=1746586149; SERVERID=9ee29c682be9356b7648e0eed9416111|1746586158|1746585176',
        'user_name': '123456789416199e94fa8a88fe163',
        'x_token': '9128223f-0138-4aa7-80e6-88094a0f4165',
        'tenant_code': 45000080
    }

    automation = SafetyCourseAutomation(user_config)
    automation.run()


if __name__ == '__main__':
    main()
