import requests
import json

# 模拟POST请求数据
data = {
    'theme': 'Python基础',
    'duration': '45',
    'ai_only': 'true'
}

try:
    # 发送POST请求
    print("Sending POST request to /lessonplan/generate...")
    response = requests.post('http://localhost:8000/lessonplan/generate', data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Response Text: {response.text[:200]}...")  # 显示前200个字符
    
    try:
        json_data = response.json()
        print("Response JSON:")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except ValueError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response:")
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    print("Please make sure the Django server is running on port 8000")