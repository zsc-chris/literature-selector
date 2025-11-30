from bs4 import BeautifulSoup, Comment
import re
import os
from multiprocessing import Process
from ollama import Client
import time
import ctypes
import winsound
import pyautogui
import pyperclip

client = Client()

# 配置
LINKS_FILE = "article_links.txt"
RESULTS_FILE = "classification_results.txt"
DOMAIN_FILE = "domain_definition.txt"
OLLAMA_MODEL = "deepseek-r1:32b"  # 替换为您使用的模型

def tag_visible(element):
	"""判断元素是否可见"""
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def text_from_html(body):
	"""从HTML提取可见文本"""
	soup = BeautifulSoup(body, 'html.parser')
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_visible, texts)  
	return " ".join(t.strip() for t in visible_texts)

def extract_abstract_and_context(text):
	"""提取abstract及其后100个单词"""
	# 因为忽略大小写，实际只需一种abstract匹配模式
	pattern = r'\bAbstract\b[^a-zA-Z]*([^.]{50,500})'

	match = re.search(pattern, text, re.IGNORECASE)
	if match:
		abstract_text = match.group(1).strip()
		# 获取abstract后的100个单词
		words = re.findall(r'\b\w+\b', text[match.end():])
		context = ' '.join(words[:100])
		return f"{abstract_text} {context}"
	
	# 如果没有找到abstract，返回前200个单词作为备选
	words = re.findall(r'\b\w+\b', text)
	return ' '.join(words[:200])

def load_domain_definition():
	"""加载领域定义"""
	try:
		with open(DOMAIN_FILE, 'r', encoding='utf-8') as f:
			return f.read().strip()
	except FileNotFoundError:
		print(f"错误: 找不到领域定义文件 {DOMAIN_FILE}")
		return "生物信息学"  # 默认领域

def query_ollama(title, abstract, domain_definition):
	"""使用Ollama判断摘要是否属于指定领域"""
	prompt = f"""
请判断以下学术文献是否能为领域"{domain_definition}"的研究提供有价值的信息。研究者是博士生，希望能一定程度拓宽视野但不被相关程度低的文献干扰。你的标准应设定得较严格一些。

文章标题:
{title}

摘要内容（可能有无关信息或不完整）:
{abstract}

你只需要回答是或否。
"""
	
	try:
		# 使用Ollama API
		messages = [
		  {
		    'role': 'user',
		    'content': prompt,
		  },
		]

		result=client.chat(model=OLLAMA_MODEL, messages=messages, keep_alive=1, options=dict(seed=0,temperature=0))['message']['content']
		return "是" in result or "yes" in result.lower()
	except Exception as e:
		print(f"Ollama查询错误: {e}")
		return False

def load_existing_results():
	"""加载已存在的结果"""
	results = {}
	if os.path.exists(RESULTS_FILE):
		with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
			for line in f:
				parts = line.strip().split('\t')
				if len(parts) >= 4:
					title = parts[0]
					domain = parts[1]
					model = parts[2]
					results[(title,domain,model)] = parts[3]
	return results

# 播放提示音。提示音需要在E5和C5之间循环，一个1秒
def play_sound():
	frequency1 = 659  # E5
	frequency2 = 523  # C5
	duration = 1000  # milliseconds
	while True:
		winsound.Beep(frequency1, duration)
		winsound.Beep(frequency2, duration)

def process_articles():
	"""处理所有文章"""
	# 使用屏幕选择复制（自动打开页面并提示用户手动处理Cloudflare）
	pyautogui.FAILSAFE = False

	# 提示用户打开浏览器
	msg = "请打开浏览器，然后点击确定继续。"
	ctypes.windll.user32.MessageBoxW(0, msg, "准备浏览器", 1)
	pyautogui.hotkey('ctrl', 't')  # 新标签页。避免打开过多标签页，只执行一次

	domain_definition = load_domain_definition()
	results = load_existing_results()

	# 读取链接文件
	with open(LINKS_FILE, 'r', encoding='utf-8') as f:
		lines = f.readlines()

	for i, line in enumerate(lines):
		if not line.strip():
			continue

		parts = line.strip().split('\t')
		if len(parts) < 2:
			continue

		title, url = parts[0], parts[1]

		# 检查是否已处理
		if (title, domain_definition, OLLAMA_MODEL) in results:
			print(f"跳过已处理: {title}")
			continue

		print(f"处理 ({i+1}/{len(lines)}): {title}")

		# 自动复制链接到浏览器并敲回车打开
		pyperclip.copy(url)

		# 快捷键打开浏览器地址栏
		pyautogui.hotkey('ctrl', 'l')  # 快捷键选中地址栏
		time.sleep(0.1)
		pyautogui.hotkey('ctrl', 'v')  # 粘贴URL
		time.sleep(0.1)
		pyautogui.press('enter')  # 打开链接

		# 反复尝试复制并检查长度，以检测 Cloudflare 验证
		copied_text = ""
		attempt = 0
		while attempt < 3:
			attempt += 1
			time.sleep(5) # 等待页面加载
			try:
				# 选中页面内容。因为页面内容可能较多，等待相对较长时间确保选中
				pyautogui.hotkey('ctrl', 'a')
				time.sleep(0.5)
				# 复制到剪贴板
				pyautogui.hotkey('ctrl', 'c')
				time.sleep(0.5)
				copied_text = pyperclip.paste()
			except Exception as e:
				print(f"  复制尝试出错: {e}")
				copied_text = ""

			# 如果复制内容足够长，认为成功
			if copied_text and len(copied_text) > 120:
				break

			# 复制结果很短，可能存在 Cloudflare 验证或页面未准备好
			# 播放提示音并提示用户手动通过后重试或取消
			sound_process = Process(target=play_sound)
			sound_process.start()
			res = ctypes.windll.user32.MessageBoxW(0, "复制到剪贴板的文本太短，可能存在 Cloudflare 验证或页面未准备好。\n\n请手动完成验证后点击确定重试，或点击取消跳过此文章。", "需要手动验证", 1 | 0x20)
			sound_process.terminate()
			# MessageBoxW 返回 1 为确定，2 为取消（IDCANCEL）
			if res == 2:
				# 用户选择取消，跳过此文章
				print(f"  用户选择跳过: {title}")
				copied_text = ""
				break

		# 如果最终复制文本仍然很短，则记录为不可用并继续
		if not copied_text or len(copied_text) < 120:
			print(f"  警告: 复制文本过短，可能存在验证，跳过自动判断")
			is_in_domain = False
			abstract_context = ""
		else:
			# 使用复制的屏幕文本作为输入，提取摘要/上下文
			abstract_context = extract_abstract_and_context(copied_text)
			print(abstract_context)
			# 使用Ollama判断
			is_in_domain = query_ollama(title, abstract_context, domain_definition)

		# 保存结果
		result_line = f"{title}\t{domain_definition}\t{is_in_domain}"
		results[(title, domain_definition, OLLAMA_MODEL)] = is_in_domain
		print(f"  结果: 属于{domain_definition} = {is_in_domain}")

		# 每处理10个文章保存一次进度
		if (i + 1) % 10 == 0:
			save_results(results)

	# 最终保存
	save_results(results)
	print(f"处理完成！结果保存在: {RESULTS_FILE}")
	ctypes.windll.user32.MessageBoxW(0, "处理完成！", "处理完成！", 1) # 添加提示框通知用户处理完成，因为用户此时活动窗口为浏览器

def save_results(results):
	"""保存结果到文件"""
	with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
		for (title, domain, model), result in results.items():
			f.write(f"{title}\t{domain}\t{model}\t{result}\n")

if __name__ == "__main__":
	process_articles()