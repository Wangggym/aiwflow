import os
import string


def get_env_variable(var_name: str, required: bool = True) -> str:
    """获取环境变量值
    
    Args:
        var_name: 环境变量名
        required: 是否必需，如果为True且变量不存在则抛出异常，否则返回None
    """
    value = os.environ.get(var_name)
    if value is None and required:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value


def contains_only_english_with_special_chars(text):
    # Define allowed special characters, including all ASCII punctuation characters
    allowed_special_chars = set(string.punctuation)

    # Check if the string contains only English characters and allowed special characters
    for char in text:
        if (ord(char) < 0x20 or ord(char) > 0x7E) and char not in allowed_special_chars:
            return False
    return True


def is_long_desc(text: str) -> bool:
    length_threshold = 100
    return len(text) > length_threshold
