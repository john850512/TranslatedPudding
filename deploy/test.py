from langconv import Converter
recognize_text = '可以不要用简体字吗'
recognize_text = Converter('zh-hant').convert(recognize_text)
recognize_text = recognize_text
print(recognize_text)