#!/usr/bin/env python3
"""
OmniDesk AI PyQt6 版本 - Windows EXE 打包脚本
一键生成完整的 Windows 安装程序
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
from datetime import datetime

class PyQt6Builder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / 'dist_pyqt6'
        self.build_dir = self.project_root / 'build_pyqt6'
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def print_header(self, text):
        """打印标题"""
        print()
        print("=" * 70)
        print(f"  {text}")
        print("=" * 70)
        print()
    
    def print_step(self, text):
        """打印步骤"""
        print(f"▶ {text}")
    
    def check_dependencies(self):
        """检查依赖"""
        self.print_header("检查依赖")
        
        dependencies = {
            'pyinstaller': 'PyInstaller',
            'PyQt6': 'PyQt6',
        }
        
        for package, name in dependencies.items():
            try:
                __import__(package)
                print(f"  ✓ {name} 已安装")
            except ImportError:
                print(f"  ✗ {name} 未安装")
                print(f"    运行: pip install {package}")
                return False
        
        return True
    
    def clean_previous_builds(self):
        """清理之前的构建"""
        self.print_step("清理之前的构建文件...")
        
        for directory in [self.dist_dir, self.build_dir]:
            if directory.exists():
                shutil.rmtree(directory)
                print(f"  已删除: {directory}")
    
    def build_with_pyinstaller(self):
        """使用 PyInstaller 构建"""
        self.print_header("使用 PyInstaller 构建应用")
        
        spec_file = self.project_root / 'omnidesk_pyqt6.spec'
        
        if not spec_file.exists():
            print(f"  ✗ 错误: 找不到 {spec_file}")
            return False
        
        self.print_step("运行 PyInstaller...")
        
        try:
            cmd = [
                sys.executable,
                '-m', 'PyInstaller',
                str(spec_file),
                '--distpath', str(self.dist_dir),
                '--buildpath', str(self.build_dir),
                '--specpath', str(self.project_root),
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"  ✗ 构建失败:")
                print(result.stderr)
                return False
            
            print(f"  ✓ 构建成功")
            return True
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")
            return False
    
    def create_installer(self):
        """创建 Windows 安装程序"""
        self.print_header("创建 Windows 安装程序")
        
        exe_dir = self.dist_dir / 'OmniDesk-AI'
        
        if not exe_dir.exists():
            print(f"  ✗ 错误: 找不到 {exe_dir}")
            return False
        
        # 创建安装程序目录
        installer_dir = self.dist_dir / 'installer'
        installer_dir.mkdir(exist_ok=True)
        
        # 复制 EXE 和依赖
        self.print_step("复制应用文件...")
        
        app_dir = installer_dir / 'app'
        if app_dir.exists():
            shutil.rmtree(app_dir)
        
        shutil.copytree(exe_dir, app_dir)
        print(f"  ✓ 文件已复制到 {app_dir}")
        
        return True
    
    def generate_release_notes(self):
        """生成发布说明"""
        self.print_header("生成发布说明")
        
        release_notes = f"""# OmniDesk AI v1.1.0 - PyQt6 版本

## 发布信息
- **版本**: 1.1.0
- **发布日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **构建时间**: {self.timestamp}
- **平台**: Windows 10/11 64-bit

## 新增功能
- ✓ PyQt6 原生 Windows 桌面应用
- ✓ 完整的虚拟机集成
- ✓ AI 代理和任务执行
- ✓ 三层感知引擎
- ✓ 安全审计系统
- ✓ 插件系统
- ✓ 实时协作
- ✓ 性能优化
- ✓ AI 模型动态热重载
- ✓ 开箱即用

## 系统要求
- Windows 10/11 64-bit
- 至少 8 GB RAM
- 至少 20 GB 磁盘空间

## 安装说明
1. 下载 OmniDesk-AI-Setup-1.1.0.exe
2. 双击运行安装程序
3. 按照提示完成安装
4. 启动应用

## 使用说明
请参考 QUICKSTART_PYQT6.md 文件

## 已知问题
无

## 反馈
如有问题，请联系: support@omnidesk.ai

---

OmniDesk AI - 完整的 Windows AI 代理系统
"""
        
        release_notes_file = self.dist_dir / 'RELEASE_NOTES_PyQt6.md'
        with open(release_notes_file, 'w', encoding='utf-8') as f:
            f.write(release_notes)
        
        print(f"  ✓ 发布说明已生成: {release_notes_file}")
    
    def generate_checksums(self):
        """生成校验和"""
        self.print_header("生成校验和")
        
        import hashlib
        
        checksums = {}
        
        # 计算 EXE 文件的校验和
        exe_file = self.dist_dir / 'OmniDesk-AI' / 'OmniDesk-AI.exe'
        if exe_file.exists():
            sha256_hash = hashlib.sha256()
            with open(exe_file, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(byte_block)
            
            checksums['OmniDesk-AI.exe'] = sha256_hash.hexdigest()
            print(f"  ✓ OmniDesk-AI.exe: {checksums['OmniDesk-AI.exe']}")
        
        # 保存校验和
        checksums_file = self.dist_dir / 'CHECKSUMS_PyQt6.json'
        with open(checksums_file, 'w', encoding='utf-8') as f:
            json.dump(checksums, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ 校验和已保存: {checksums_file}")
    
    def generate_project_info(self):
        """生成项目信息"""
        self.print_header("生成项目信息")
        
        project_info = {
            "name": "OmniDesk AI",
            "version": "1.1.0",
            "variant": "PyQt6",
            "description": "完整的 Windows AI 代理系统",
            "build_timestamp": self.timestamp,
            "build_date": datetime.now().isoformat(),
            "platform": "Windows",
            "architecture": "x86_64",
            "features": [
                "虚拟机集成",
                "AI 代理",
                "三层感知引擎",
                "安全审计系统",
                "插件系统",
                "实时协作",
                "性能优化",
                "AI 模型动态热重载",
                "开箱即用"
            ]
        }
        
        info_file = self.dist_dir / 'PROJECT_INFO_PyQt6.json'
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(project_info, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ 项目信息已生成: {info_file}")
    
    def create_final_zip(self):
        """创建最终 ZIP 包"""
        self.print_header("创建最终 ZIP 包")
        
        import zipfile
        
        zip_file = self.dist_dir / 'OmniDesk-AI-v1.1.0-PyQt6.zip'
        
        self.print_step("压缩文件...")
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 添加 EXE 和依赖
            app_dir = self.dist_dir / 'OmniDesk-AI'
            if app_dir.exists():
                for root, dirs, files in os.walk(app_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(self.dist_dir)
                        zf.write(file_path, arcname)
            
            # 添加文档
            for doc_file in ['RELEASE_NOTES_PyQt6.md', 'CHECKSUMS_PyQt6.json', 'PROJECT_INFO_PyQt6.json']:
                doc_path = self.dist_dir / doc_file
                if doc_path.exists():
                    zf.write(doc_path, doc_file)
        
        zip_size = zip_file.stat().st_size / (1024 * 1024)
        print(f"  ✓ ZIP 包已创建: {zip_file} ({zip_size:.2f} MB)")
        
        return zip_file
    
    def print_summary(self, zip_file):
        """打印总结"""
        self.print_header("构建完成!")
        
        print("✓ 所有步骤已完成")
        print()
        print("生成的文件:")
        print(f"  • {zip_file.name}")
        print()
        print("下一步:")
        print("  1. 下载 ZIP 文件")
        print("  2. 在 Windows 上解压")
        print("  3. 运行 OmniDesk-AI.exe")
        print()
        print("或者:")
        print("  1. 解压 ZIP 文件")
        print("  2. 运行 start_pyqt6.bat 启动应用")
        print()
    
    def build(self):
        """执行构建"""
        self.print_header("OmniDesk AI PyQt6 版本 - Windows EXE 构建")
        
        # 检查依赖
        if not self.check_dependencies():
            print("✗ 依赖检查失败")
            return False
        
        # 清理之前的构建
        self.clean_previous_builds()
        
        # 使用 PyInstaller 构建
        if not self.build_with_pyinstaller():
            print("✗ PyInstaller 构建失败")
            return False
        
        # 创建安装程序
        if not self.create_installer():
            print("✗ 安装程序创建失败")
            return False
        
        # 生成发布说明
        self.generate_release_notes()
        
        # 生成校验和
        self.generate_checksums()
        
        # 生成项目信息
        self.generate_project_info()
        
        # 创建最终 ZIP 包
        zip_file = self.create_final_zip()
        
        # 打印总结
        self.print_summary(zip_file)
        
        return True


def main():
    builder = PyQt6Builder()
    
    try:
        if builder.build():
            print("✓ 构建成功!")
            return 0
        else:
            print("✗ 构建失败!")
            return 1
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
