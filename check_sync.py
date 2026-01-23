import os
import re

# 获取绝对路径，避免 ./ 带来的混淆
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BASE_DIR, 'source', '_posts')
IMAGES_DIR = os.path.join(BASE_DIR, 'source', 'images')

def get_time_from_str(s):
    nums = "".join(re.findall(r'\d+', s))
    return nums[:14] if len(nums) >= 12 else None

def run_sync(dry_run=True):
    if not os.path.exists(IMAGES_DIR):
        print(f"错误：找不到文件夹 {IMAGES_DIR}")
        return

    real_images = [f for f in os.listdir(IMAGES_DIR) if '屏幕截图' in f]
    referenced_names = set()
    
    for root, _, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = re.findall(r'/images/(image-\d+\.png)', content)
                    referenced_names.update(links)

    print(f"找到 MD 引用: {len(referenced_names)} 个")
    print(f"找到物理图片: {len(real_images)} 张\n")

    matches = []
    for ref in referenced_names:
        ref_time = get_time_from_str(ref)
        if not ref_time: continue
        
        best_match, min_diff = None, float('inf')
        for real in real_images:
            real_time = get_time_from_str(real)
            if not real_time: continue
            try:
                diff = abs(int(ref_time) - int(real_time))
                if diff < min_diff:
                    min_diff, best_match = diff, real
            except: continue
        
        if best_match and min_diff < 10000:
            matches.append((best_match, ref))

    if matches:
        print(f"准备重命名 {len(matches)} 个文件...")
        if not dry_run:
            confirm = input("确定执行？(y/n): ")
            if confirm.lower() == 'y':
                for old_name, new_name in matches:
                    old_path = os.path.join(IMAGES_DIR, old_name)
                    new_path = os.path.join(IMAGES_DIR, new_name)
                    try:
                        if os.path.exists(old_path):
                            os.rename(old_path, new_path)
                            print(f"成功: {old_name} -> {new_name}")
                    except Exception as e:
                        print(f"失败: {old_name} 被占用或找不到 - {e}")
                print("\n操作完成！")
    else:
        print("没有找到匹配的图片。")

if __name__ == "__main__":
    run_sync(dry_run=False)