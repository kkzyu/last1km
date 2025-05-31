import os
import re
import json
import requests
from flask import current_app

class AIService:
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """延迟初始化百度AI客户端"""
        try:
            from aip import AipOcr
            
            # 从环境变量获取凭证
            app_id = os.getenv('BAIDU_AI_APP_ID')
            api_key = os.getenv('BAIDU_AI_API_KEY') 
            secret_key = os.getenv('BAIDU_AI_SECRET_KEY')
            
            if not all([app_id, api_key, secret_key]):
                print("警告：百度AI凭证未配置，AI识别功能将不可用")
                return
            
            # 初始化百度OCR客户端
            self.client = AipOcr(app_id, api_key, secret_key)
            print("百度AI OCR客户端初始化成功")
            
        except ImportError as e:
            print(f"警告：无法导入百度AI SDK: {e}")
        except Exception as e:
            print(f"警告：初始化百度AI客户端失败: {e}")
    
    def recognize_text(self, image_path):
        """OCR文字识别"""
        if not self.client:
            raise Exception("AI服务未正确初始化，请检查配置")
        
        try:
            # 读取图片文件
            with open(image_path, 'rb') as fp:
                image = fp.read()
            
            # 调用百度OCR API
            result = self.client.basicGeneral(image)
            
            if 'error_code' in result:
                raise Exception(f"OCR API错误: {result.get('error_msg', '未知错误')}")
            
            if 'words_result' in result:
                # 提取所有识别到的文字
                text_lines = [item['words'] for item in result['words_result']]
                return '\n'.join(text_lines)
            else:
                current_app.logger.warning(f"OCR识别结果异常: {result}")
                return ''
                
        except Exception as e:
            current_app.logger.error(f"OCR识别失败: {str(e)}")
            raise Exception(f"图片识别失败: {str(e)}")
    
    def parse_order_info(self, text):
        """使用AI智能解析订单信息"""
        result = {
            'description': '',
            'orderInfo': ''
        }
        
        if not text.strip():
            return result
        
        try:
            # 使用AI理解文本内容
            ai_result = self._ai_understand_text(text)
            
            if ai_result and isinstance(ai_result, dict):
                result['description'] = ai_result.get('description', '')
                result['orderInfo'] = ai_result.get('orderInfo', '')
            
            # 如果AI解析失败，回退到规则解析
            if not result['description'] and not result['orderInfo']:
                result['description'] = self._fallback_extract_description(text)
                result['orderInfo'] = self._fallback_extract_order_info(text)
            
        except Exception as e:
            current_app.logger.error(f"AI解析失败，使用备用方案: {str(e)}")
            # 回退到规则解析
            result['description'] = self._fallback_extract_description(text)
            result['orderInfo'] = self._fallback_extract_order_info(text)
        
        return result
    
    def _ai_understand_text(self, text):
        """使用AI模型理解文本内容"""
        try:
            # 构建提示词
            prompt = f"""请分析以下外卖订单截图的文字内容，提取关键信息。

文字内容：
{text}

请从中提取：
1. 商家名称和主要商品（格式：商家名 - 商品名）
2. 取件信息（包括地址、联系人、电话等）

要求：
- 忽略广告语、优惠信息、状态提示等无关内容
- 商品名称要选择主要的、实质性的商品，不要选配菜或赠品
- 联系电话只显示后4位，格式：****XXXX
- 如果信息不完整或无法确定，返回空字符串

请以JSON格式返回，不要包含其他文字：
{{"description": "商家名 - 主要商品", "orderInfo": "完整的取件信息"}}"""
            
            # 调用文心一言API
            ai_response = self._call_wenxin_api(prompt)
            
            if ai_response:
                # 尝试解析JSON
                try:
                    return json.loads(ai_response)
                except json.JSONDecodeError:
                    # 如果不是标准JSON，尝试提取JSON部分
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
            
        except Exception as e:
            current_app.logger.error(f"AI理解失败: {str(e)}")
            return None
    
    def _call_wenxin_api(self, prompt):
        """调用百度文心一言API"""
        try:
            # 获取access_token
            access_token = self._get_wenxin_access_token()
            
            if not access_token:
                raise Exception("无法获取文心一言API访问令牌")
            
            # 文心一言API地址
            url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={access_token}"
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "top_p": 0.8,
                "penalty_score": 1.0,
                "enable_system_memory": False,
                "system": "你是一个专门分析外卖订单信息的AI助手，能够准确识别和提取商家名称、商品信息和取件信息。请严格按照JSON格式返回结果。"
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            current_app.logger.info(f"文心一言API响应状态: {response.status_code}")
            current_app.logger.info(f"文心一言API响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    return result['result']
                else:
                    current_app.logger.error(f"文心一言API响应格式异常: {result}")
                    return None
            else:
                raise Exception(f"文心一言API调用失败: {response.status_code}, {response.text}")
            
        except Exception as e:
            current_app.logger.error(f"文心一言API调用错误: {str(e)}")
            return None
    
    def _get_wenxin_access_token(self):
        """获取文心一言API的access_token"""
        try:
            # 从环境变量获取文心一言的API密钥
            api_key = os.getenv('BAIDU_WENXIN_API_KEY') or os.getenv('BAIDU_AI_API_KEY')
            secret_key = os.getenv('BAIDU_WENXIN_SECRET_KEY') or os.getenv('BAIDU_AI_SECRET_KEY')
            
            if not api_key or not secret_key:
                current_app.logger.error("文心一言API密钥未配置")
                return None
            
            url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={api_key}&client_secret={secret_key}&grant_type=client_credentials"
            
            response = requests.post(url, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'access_token' in result:
                    current_app.logger.info("文心一言access_token获取成功")
                    return result['access_token']
                else:
                    current_app.logger.error(f"获取access_token失败: {result}")
            else:
                current_app.logger.error(f"获取access_token HTTP错误: {response.status_code}")
            
        except Exception as e:
            current_app.logger.error(f"获取文心一言access_token失败: {str(e)}")
        
        return None
    
    def _fallback_extract_description(self, text):
        """备用规则提取商品描述"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        restaurant_name = ""
        main_dish = ""
        
        store_indicators = ['店', '餐厅', '堂', '坊', '轩', '居', '斋', '阁', '苑', '庄', '楼', '厅', '房', '屋', '铺', '家', '记', '园', '庭', '坞', '湾', '城']
        
        for line in lines:
            # 跳过无关信息
            if any(skip in line for skip in ['订单已送达', '恭喜', '成长值', '优惠', '服务', '联系', '打赏', '开发票', '加入', '立即', '查看详情', '其他服务', '号码保护', '商家赠送', '温馨提示', '实付', '配送费']):
                continue
            
            # 查找商家名
            if not restaurant_name and any(indicator in line for indicator in store_indicators):
                if 3 <= len(line) <= 40 and '￥' not in line and not re.search(r'\d{11}', line):
                    restaurant_name = line
                    continue
            
            # 查找主要商品
            if restaurant_name and not main_dish:
                if (3 <= len(line) <= 50 and 
                    '￥' not in line and 
                    not re.search(r'\d{11}', line) and
                    '送至' not in line and
                    not re.match(r'^[\d\s\-:\.￥元×x]+$', line)):
                    main_dish = line
                    break
        
        if restaurant_name and main_dish:
            return f"{restaurant_name} - {main_dish}"
        elif restaurant_name:
            return restaurant_name
        elif main_dish:
            return main_dish
        
        return ""
    
    def _fallback_extract_order_info(self, text):
        """备用规则提取取件信息"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            if '送至' in line:
                match = re.search(r'送至(.+)', line)
                if match:
                    full_info = match.group(1).strip()
                    
                    # 提取手机号并隐藏
                    phone_match = re.search(r'(\d{11})', full_info)
                    if phone_match:
                        full_phone = phone_match.group(1)
                        phone_hidden = f"****{full_phone[-4:]}"
                        info_without_phone = full_info.replace(full_phone, phone_hidden)
                        return info_without_phone
                    else:
                        return full_info
        
        return ""

# 创建全局实例
ai_service = AIService()