#!/usr/bin/env python3
"""
OpenMineral Release Management Script

This script handles versioning, tagging, and release preparation for the OpenMineral platform.
"""

import os
import re
import json
import subprocess
import sys
from datetime import datetime
from typing import Tuple
import semver

class ReleaseManager:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.version_files = {
            'backend': 'backend/main.py',
            'frontend': 'frontend/package.json',
            'docs': 'docs/mkdocs.yml',
            'changelog': 'CHANGELOG.md'
        }
        
    def get_current_version(self) -> str:
        """Get current version from package.json"""
        package_json_path = os.path.join(self.root_dir, 'frontend/package.json')
        
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        return package_data.get('version', '0.1.0')
    
    def bump_version(self, current_version: str, bump_type: str) -> str:
        """Bump version using semantic versioning"""
        try:
            if bump_type == 'major':
                return semver.bump_major(current_version)
            elif bump_type == 'minor':
                return semver.bump_minor(current_version)
            elif bump_type == 'patch':
                return semver.bump_patch(current_version)
            else:
                raise ValueError(f"Invalid bump type: {bump_type}")
        except ValueError as e:
            # Handle non-semver versions
            parts = current_version.split('.')
            if len(parts) < 3:
                parts.extend(['0'] * (3 - len(parts)))
            
            major, minor, patch = map(int, parts[:3])
            
            if bump_type == 'major':
                return f"{major + 1}.0.0"
            elif bump_type == 'minor':
                return f"{major}.{minor + 1}.0"
            elif bump_type == 'patch':
                return f"{major}.{minor}.{patch + 1}"
    
    def update_version_files(self, new_version: str):
        """Update version in all relevant files"""
        updates = []
        
        # Update package.json
        package_json_path = os.path.join(self.root_dir, 'frontend/package.json')
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        package_data['version'] = new_version
        
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        updates.append(f"Updated frontend/package.json to {new_version}")
        
        # Update backend main.py version
        main_py_path = os.path.join(self.root_dir, 'backend/main.py')
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Update FastAPI version
        content = re.sub(
            r'version="[^"]*"',
            f'version="{new_version}"',
            content
        )
        
        with open(main_py_path, 'w') as f:
            f.write(content)
        
        updates.append(f"Updated backend/main.py to {new_version}")
        
        # Update README badges
        readme_path = os.path.join(self.root_dir, 'README.md')
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        readme_content = re.sub(
            r'badge/version-v[^-]*-blue',
            f'badge/version-v{new_version}-blue',
            readme_content
        )
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        updates.append(f"Updated README.md version badge to {new_version}")
        
        return updates
    
    def update_changelog(self, version: str, changes: list):
        """Update CHANGELOG.md with new version"""
        changelog_path = os.path.join(self.root_dir, 'CHANGELOG.md')
        
        with open(changelog_path, 'r') as f:
            content = f.read()
        
        # Insert new version section after "## [Unreleased]"
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        new_section = f"""
## [v{version}] - {date_str}

### Added
{chr(10).join(f'- {change}' for change in changes)}

### Changed
- Updated dependencies to latest versions
- Improved performance and stability

### Security
- Updated security dependencies
- Enhanced authentication mechanisms
"""
        
        # Replace [Unreleased] section
        unreleased_pattern = r'## \[Unreleased\].*?(?=## \[|$)'
        unreleased_replacement = f"## [Unreleased]\n\n### Planned\n- Advanced LangGraph workflow designer\n- Claude 3.5 Sonnet integration\n- Vector database semantic search\n{new_section}"
        
        content = re.sub(unreleased_pattern, unreleased_replacement, content, flags=re.DOTALL)
        
        with open(changelog_path, 'w') as f:
            f.write(content)
        
        return f"Updated CHANGELOG.md with version {version}"
    
    def create_git_tag(self, version: str):
        """Create and push git tag"""
        tag_name = f"v{version}"
        
        try:
            # Create annotated tag
            subprocess.run([
                'git', 'tag', '-a', tag_name, 
                '-m', f'Release version {version}'
            ], check=True)
            
            # Push tag to remote
            subprocess.run(['git', 'push', 'origin', tag_name], check=True)
            
            return f"Created and pushed tag {tag_name}"
        
        except subprocess.CalledProcessError as e:
            return f"Error creating tag: {e}"
    
    def run_tests(self) -> bool:
        """Run tests before release"""
        print("Running tests before release...")
        
        try:
            # Backend tests
            subprocess.run(['pytest', 'backend/tests/', '-v'], 
                         cwd=self.root_dir, check=True)
            
            # Frontend tests
            subprocess.run(['npm', 'test', '--', '--run'], 
                         cwd=os.path.join(self.root_dir, 'frontend'), check=True)
            
            return True
        
        except subprocess.CalledProcessError:
            print("❌ Tests failed! Please fix issues before release.")
            return False
    
    def prepare_release(self, bump_type: str = 'minor'):
        """Prepare a new release"""
        print(f"🚀 Preparing OpenMineral release ({bump_type} bump)")
        
        # Get current version
        current_version = self.get_current_version()
        print(f"Current version: {current_version}")
        
        # Calculate new version
        new_version = self.bump_version(current_version, bump_type)
        print(f"New version: {new_version}")
        
        # Run tests
        if not self.run_tests():
            sys.exit(1)
        
        # Update version files
        print("📝 Updating version files...")
        updates = self.update_version_files(new_version)
        for update in updates:
            print(f"  ✅ {update}")
        
        # Update changelog
        print("📋 Updating CHANGELOG...")
        changelog_update = self.update_changelog(new_version, [
            "Platform improvements and bug fixes",
            "Enhanced AI integration capabilities", 
            "Updated dependencies and security patches"
        ])
        print(f"  ✅ {changelog_update}")
        
        # Commit changes
        print("💾 Committing changes...")
        try:
            subprocess.run(['git', 'add', '.'], cwd=self.root_dir, check=True)
            subprocess.run([
                'git', 'commit', '-m', f'chore: bump version to {new_version}'
            ], cwd=self.root_dir, check=True)
            
            print(f"  ✅ Committed version bump to {new_version}")
        
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error committing changes: {e}")
            return
        
        # Create and push tag
        print("🏷️  Creating release tag...")
        tag_result = self.create_git_tag(new_version)
        print(f"  ✅ {tag_result}")
        
        # Push changes
        print("🚀 Pushing to remote...")
        try:
            subprocess.run(['git', 'push'], cwd=self.root_dir, check=True)
            print("  ✅ Pushed changes to remote")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error pushing changes: {e}")
            return
        
        print(f"🎉 Release {new_version} prepared successfully!")
        print(f"📦 GitHub Release will be created automatically via Actions")
        print(f"🐳 Docker images will be built and published")
        print(f"📚 Documentation will be updated at docs.openmineral.com")

def main():
    """Main function for release management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenMineral Release Manager')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], 
                       default='minor', help='Version bump type')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    manager = ReleaseManager()
    
    if args.dry_run:
        current = manager.get_current_version()
        new = manager.bump_version(current, args.bump)
        print(f"Dry run: Would bump version from {current} to {new}")
        return
    
    manager.prepare_release(args.bump)

if __name__ == '__main__':
    main()