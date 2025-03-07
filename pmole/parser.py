"""
Module for parsing and processing Python imports.
"""

import sys
import re
import os
from typing import List, Dict, Optional, Set
from pathlib import Path


class ImportNode:
    """Node for representing import hierarchy."""
    def __init__(self, name: str, parent: Optional['ImportNode'] = None):
        self.name = name
        self.parent = parent
        self.children: Dict[str, 'ImportNode'] = {}

    def full_path(self) -> str:
        """Get full dotted path for the node."""
        parts = []
        current = self
        while current:
            if current.name:
                parts.append(current.name)
            current = current.parent
        return '.'.join(reversed(parts))

    def __repr__(self) -> str:
        return f"<ImportNode {self.full_path()}>"


def parse_imports(content: str) -> List[str]:
    """
    Parse import statements from Python code content.
    Handles multi-line imports with parentheses.
    """
    imports = []
    in_import = False
    current_import = []
    paren_stack = 0
    import_pattern = re.compile(r'^\s*(from |import )', re.MULTILINE)

    for line in content.split('\n'):
        line = line.split('#')[0].strip()  # Remove comments
        if not line:
            continue

        if import_pattern.match(line):
            in_import = True
            paren_stack = 0

        if in_import:
            current_import.append(line)
            paren_stack += line.count('(')
            paren_stack -= line.count(')')

            if paren_stack == 0 and line.endswith(')'):
                in_import = False
                import_line = ' '.join(current_import).replace('(', '').replace(')', '')
                imports.append(import_line)
                current_import = []
            elif not line.endswith('\\') and paren_stack == 0:
                in_import = False
                imports.append(' '.join(current_import))
                current_import = []

    return imports


def normalize_import(import_stmt: str) -> List[str]:
    """Normalize import statement to individual modules."""
    # Handle from ... import ...
    from_import_match = re.match(r'^from\s+([\w.]+)\s+import\s+(.+)$', import_stmt)
    if from_import_match:
        module = from_import_match.group(1)
        imports = [i.strip() for i in from_import_match.group(2).split(',')]
        return [f"{module}.{imp}" for imp in imports if not re.match(r'^\w+\s*=', imp)]

    # Handle direct imports
    direct_import_match = re.match(r'^import\s+(.+)$', import_stmt)
    if direct_import_match:
        imports = [i.strip() for i in direct_import_match.group(1).split(',')]
        return [imp.split(' as ')[0] for imp in imports]

    return []


def build_import_tree(modules: List[str]) -> ImportNode:
    """Build hierarchical tree from list of modules."""
    root = ImportNode("")
    for module in modules:
        current = root
        for part in module.split('.'):
            if part not in current.children:
                current.children[part] = ImportNode(part, current)
            current = current.children[part]
    return root


def module_to_path(module: str, current_file: Path, base_dir: Path) -> Optional[Path]:
    """Convert module path to filesystem path."""
    # Convert module name to file path
    module_path = base_dir / Path(str(module.replace('.', '/')) + '.py')
    print(f"🔍 Module path: {module_path} from base {base_dir}")
    if module_path.exists():
        return module_path
    return None


def process_file(filepath: str, processed: Set[str], contents: List[str], base_dir: Path) -> None:
    """Process single file and its imports."""
    verbose = os.environ.get('PMOLE_VERBOSE') == '1'
    
    abs_path = Path(filepath).resolve()
    if verbose:
        print(f"🔍 Processing file: {abs_path}")
    
    if str(abs_path) in processed:
        if verbose:
            print(f"⏩ Skipping already processed: {abs_path}")
        return

    processed.add(str(abs_path))

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {abs_path}: {e}", file=sys.stderr)
        return

    # Get relative path for output
    try:
        rel_path = abs_path.relative_to(base_dir)
    except ValueError:
        rel_path = abs_path

    # Add file content to results with relative path
    contents.append(f"FILE PATH\n[{rel_path}]\nFILE CONTENT\n[{content}]")

    # Parse and process imports
    imports = parse_imports(content)
    if verbose:
        print(f"📦 Found {len(imports)} raw imports in {abs_path}")
        for i, imp in enumerate(imports, 1):
            print(f"  {i}. {imp}")

    all_modules = []
    for imp in imports:
        normalized = normalize_import(imp)
        if verbose and normalized:
            print(f"🔧 Normalized import: {imp} → {normalized}")
        all_modules.extend(normalized)

    # Build import tree
    import_tree = build_import_tree(all_modules)

    # Process tree nodes
    stack = [import_tree]
    while stack:
        node = stack.pop()
        
        # Modified node processing logic
        if node.parent is None:
            # Process children of root node
            stack.extend(node.children.values())
            continue

        module_path = node.full_path()
        print(f"🔍 Node Module path: {module_path}")
        found_path = module_to_path(module_path, abs_path, base_dir)
        
        if verbose:
            print(f"🌳 Processing node: {module_path}")
            print(f"   🗺️  Converted to path: {found_path}")

        if found_path and found_path.exists():
            if verbose:
                print(f"   ✅ Valid path found, recursing into: {found_path}")
            process_file(str(found_path), processed, contents, base_dir)

        stack.extend(node.children.values())
