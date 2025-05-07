# analysis/dependency_analyzer.py

"""
Analysis module for dependency detection and code analysis.
Parses files to identify imports, function calls, and other dependency indicators.
"""

import os
import ast
import re
import logging
from typing import Dict, List, Tuple, Set, Optional, Any
import importlib.util
import uuid

# Import only from utils, core, and io layers
# <<< *** Removed unused import *** >>>
# from cline_utils.dependency_system.core.key_manager import get_key_from_path
from cline_utils.dependency_system.utils.path_utils import normalize_path, is_subpath, get_file_type as util_get_file_type, get_project_root
from cline_utils.dependency_system.utils.config_manager import ConfigManager
from cline_utils.dependency_system.utils.cache_manager import cached, invalidate_dependent_entries

logger = logging.getLogger(__name__)

# Regular expressions (unchanged)
PYTHON_IMPORT_PATTERN = re.compile(r'^\s*from\s+([.\w]+)\s+import\s+(?:\(|\*|\w+)', re.MULTILINE)
PYTHON_IMPORT_MODULE_PATTERN = re.compile(r'^\s*import\s+([.\w]+(?:\s*,\s*[.\w]+)*)', re.MULTILINE)
JAVASCRIPT_IMPORT_PATTERN = re.compile(r'import(?:["\'\s]*(?:[\w*{}\n\r\s,]+)from\s*)?["\']([^"\']+)["\']'r'|\brequire\s*\(\s*["\']([^"\']+)["\']\s*\)'r'|import\s*\(\s*["\']([^"\']+)["\']\s*\)')
MARKDOWN_LINK_PATTERN = re.compile(r'\[(?:[^\]]+)\]\(([^)]+)\)')
HTML_A_HREF_PATTERN = re.compile(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(?P<url>[^"\']+?)\1', re.IGNORECASE)
HTML_SCRIPT_SRC_PATTERN = re.compile(r'<script\s+(?:[^>]*?\s+)?src=(["\'])(?P<url>[^"\']+?)\1', re.IGNORECASE)
HTML_LINK_HREF_PATTERN = re.compile(r'<link\s+(?:[^>]*?\s+)?href=(["\'])(?P<url>[^"\']+?)\1', re.IGNORECASE) # General link, check rel later
HTML_IMG_SRC_PATTERN = re.compile(r'<img\s+(?:[^>]*?\s+)?src=(["\'])(?P<url>[^"\']+?)\1', re.IGNORECASE)
CSS_IMPORT_PATTERN = re.compile(r'@import\s+(?:url\s*\(\s*)?["\']?([^"\')\s]+[^"\')]*?)["\']?(?:\s*\))?;', re.IGNORECASE)

# --- Main Analysis Function ---
@cached("file_analysis",
       key_func=lambda file_path, force=False: f"analyze_file:{normalize_path(file_path)}:{(os.path.getmtime(file_path) if os.path.exists(file_path) else 0)}:{force}")
def analyze_file(file_path: str, force: bool = False) -> Dict[str, Any]:
    """
    Analyzes a file to identify dependencies, imports, and other metadata.
    Uses caching based on file path, modification time, and force flag.

    Args:
        file_path: Path to the file to analyze
        force: If True, bypass the cache for this specific file analysis.
    Returns:
        Dictionary containing analysis results or error/skipped status.
    """
    norm_file_path = normalize_path(file_path)
    if not os.path.exists(norm_file_path) or not os.path.isfile(norm_file_path): return {"error": "File not found or not a file"}

    config_manager = ConfigManager(); project_root = get_project_root()
    excluded_dirs_rel = config_manager.get_excluded_dirs(); excluded_paths_rel = config_manager.get_excluded_paths(); excluded_extensions = set(config_manager.get_excluded_extensions())
    excluded_dirs_abs = {normalize_path(os.path.join(project_root, p)) for p in excluded_dirs_rel}; excluded_paths_abs = {normalize_path(os.path.join(project_root, p)) for p in excluded_paths_rel}
    if any(is_subpath(norm_file_path, excluded) for excluded in excluded_dirs_abs.union(excluded_paths_abs)) or \
       os.path.splitext(norm_file_path)[1].lower().lstrip('.') in excluded_extensions or \
       os.path.basename(norm_file_path).endswith("_module.md"):
        logger.debug(f"Skipping analysis of excluded/tracker file: {norm_file_path}"); return {"skipped": True, "reason": "Excluded path, extension, or tracker file"}

    try:
        file_type = util_get_file_type(norm_file_path)
        analysis_result: Dict[str, Any] = {"file_path": norm_file_path, "file_type": file_type, "imports": [], "links": []}
        try:
            with open(norm_file_path, 'r', encoding='utf-8') as f: content = f.read()
        except FileNotFoundError: return {"error": "File disappeared during analysis"}
        except UnicodeDecodeError as e: return {"error": "Encoding error", "details": str(e)}
        except Exception as e: logger.error(f"Error reading file {norm_file_path}: {e}", exc_info=True); return {"error": "File read error", "details": str(e)}

        if file_type == "py": _analyze_python_file(norm_file_path, content, analysis_result)
        elif file_type == "js": _analyze_javascript_file(norm_file_path, content, analysis_result)
        elif file_type == "md": _analyze_markdown_file(norm_file_path, content, analysis_result)
        elif file_type == "html": _analyze_html_file(norm_file_path, content, analysis_result)
        elif file_type == "css": _analyze_css_file(norm_file_path, content, analysis_result)
        analysis_result["size"] = os.path.getsize(norm_file_path)
        return analysis_result
    except Exception as e:
        logger.exception(f"Unexpected error analyzing {norm_file_path}: {e}")
        return {"error": "Unexpected analysis error", "details": str(e)}

# --- Analysis Helper Functions ---

def _analyze_python_file(file_path: str, content: str, result: Dict[str, Any]) -> None:
    """Analyzes Python file content using AST."""
    result["imports"] = [] # Reset imports, AST is primary source now
    result["functions"] = []
    result["classes"] = []
    result["calls"] = []
    result["attribute_accesses"] = []
    result["inheritance"] = []
    # result["references"] = [] # Keep optional general references if needed

    def _get_full_name_str(node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Name): return node.id
        if isinstance(node, ast.Attribute):
            # Recursively get the base part
            base = _get_full_name_str(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        if isinstance(node, ast.Subscript):
            base = _get_full_name_str(node.value)
            index_repr = "..."
            if isinstance(node.slice, ast.Constant):
                index_repr = repr(node.slice.value)
            elif isinstance(node.slice, ast.Name):
                index_repr = node.slice.id
            elif isinstance(node.slice, ast.Slice):
                 lower = _get_full_name_str(node.slice.lower) if node.slice.lower else ""
                 upper = _get_full_name_str(node.slice.upper) if node.slice.upper else ""
                 step = _get_full_name_str(node.slice.step) if node.slice.step else ""
                 index_repr = f"{lower}:{upper}:{step}".rstrip(":")
            return f"{base}[{index_repr}]" if base else f"[{index_repr}]"
        # <<< *** ADDED handling for Call node if needed in name chain *** >>>
        if isinstance(node, ast.Call):
             base = _get_full_name_str(node.func)
             return f"{base}()" if base else "()"
        if isinstance(node, ast.Constant):
             return repr(node.value)

        # logger.debug(f"Unhandled node type in _get_full_name_str: {type(node)}")
        return None # Unhandled complex types

    def _get_source_object_str(node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Attribute): return _get_full_name_str(node.value)
        if isinstance(node, ast.Call): return _get_full_name_str(node.func)
        if isinstance(node, ast.Subscript): return _get_full_name_str(node.value)
        return None
    try:
        tree = ast.parse(content, filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names: result["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                 module_name = node.module or ""; relative_prefix = "." * node.level
                 full_import_source = f"{relative_prefix}{module_name}"; result["imports"].append(full_import_source)
            elif isinstance(node, ast.FunctionDef): result["functions"].append({ "name": node.name, "line": node.lineno })
            elif isinstance(node, ast.AsyncFunctionDef): result["functions"].append({ "name": node.name, "line": node.lineno, "async": True })
            elif isinstance(node, ast.ClassDef):
                result["classes"].append({ "name": node.name, "line": node.lineno })
                # Inheritance
                for base in node.bases:
                    base_full_name = _get_full_name_str(base)
                    if base_full_name: result["inheritance"].append({"class_name": node.name, "base_class_name": base_full_name, "potential_source": base_full_name, "line": getattr(base, 'lineno', node.lineno)})
            elif isinstance(node, ast.Call):
                target_full_name = _get_full_name_str(node.func); potential_source = _get_source_object_str(node.func)
                if target_full_name: result["calls"].append({"target_name": target_full_name, "potential_source": potential_source, "line": node.lineno})
            elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
                 attribute_name = node.attr; potential_source = _get_full_name_str(node.value)
                 if potential_source: result["attribute_accesses"].append({"target_name": attribute_name, "potential_source": potential_source, "line": node.lineno})
    except SyntaxError as e: logger.warning(f"AST Syntax Error in {file_path}: {e}. Analysis may be incomplete."); result["error"] = f"AST Syntax Error: {e}"
    except Exception as e: logger.exception(f"Unexpected AST analysis error in {file_path}: {e}"); result["error"] = f"Unexpected AST analysis error: {e}"

def _analyze_javascript_file(file_path: str, content: str, result: Dict[str, Any]) -> None:
    """Analyzes JavaScript file content using regex."""
    import_matches = JAVASCRIPT_IMPORT_PATTERN.finditer(content); result["imports"] = [m.group(1) or m.group(2) or m.group(3) for m in import_matches if m]
    result["functions"] = []; result["classes"] = []
    try: # Function/Class regex
        func_pattern = re.compile(r'(?:async\s+)?function\s*\*?\s*([a-zA-Z_$][\w$]*)\s*\([^)]*\)'); arrow_pattern = re.compile(r'(?:const|let|var)\s+([a-zA-Z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>')
        for match in func_pattern.finditer(content): result["functions"].append({"name": match.group(1), "line": content[:match.start()].count('\n') + 1})
        for match in arrow_pattern.finditer(content): result["functions"].append({"name": match.group(1), "line": content[:match.start()].count('\n') + 1, "type": "arrow"})
        class_pattern = re.compile(r'class\s+([a-zA-Z_$][\w$]*)')
        for match in class_pattern.finditer(content): result["classes"].append({"name": match.group(1), "line": content[:match.start()].count('\n') + 1})
    except Exception as e: logger.warning(f"Regex error during JS analysis in {file_path}: {e}")

def _analyze_markdown_file(file_path: str, content: str, result: Dict[str, Any]) -> None:
    """Analyzes Markdown file content using regex."""
    result["links"] = []; result["code_blocks"] = []
    try: # Links
        for match in MARKDOWN_LINK_PATTERN.finditer(content):
            url = match.group(1);
            if not url.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:')): result["links"].append({"url": url, "line": content[:match.start()].count('\n') + 1})
    except Exception as e: logger.warning(f"Regex error during MD link analysis in {file_path}: {e}")
    try: # Code blocks
        code_block_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
        for match in code_block_pattern.finditer(content):
             lang = match.group(1) or "text"; block_content = match.group(2)
             result["code_blocks"].append({"language": lang.lower(), "line": content[:match.start()].count('\n') + 1})
    except Exception as e: logger.warning(f"Regex error during MD code block analysis in {file_path}: {e}")

def _analyze_html_file(file_path: str, content: str, result: Dict[str, Any]) -> None:
    """Analyzes HTML file content using regex."""
    result["links"] = [] # For <a> tags
    result["scripts"] = [] # For <script src="...">
    result["stylesheets"] = [] # For <link rel="stylesheet" href="...">
    result["images"] = [] # For <img src="...">

    def find_resources(pattern, type_list):
        try:
            for match in pattern.finditer(content):
                url = match.group("url")
                if url and not url.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:', 'data:')): type_list.append({"url": url, "line": content[:match.start()].count('\n') + 1})
        except Exception as e: logger.warning(f"Regex error during HTML {type(type_list).__name__} analysis in {file_path}: {e}")
    find_resources(HTML_A_HREF_PATTERN, result["links"]); find_resources(HTML_SCRIPT_SRC_PATTERN, result["scripts"]); find_resources(HTML_IMG_SRC_PATTERN, result["images"])
    try: # Stylesheets
        link_tag_pattern = re.compile(r'<link([^>]+)>', re.IGNORECASE); href_pattern = re.compile(r'href=(["\'])(?P<url>[^"\']+?)\1', re.IGNORECASE); rel_pattern = re.compile(r'rel=(["\'])stylesheet\1', re.IGNORECASE)
        for link_match in link_tag_pattern.finditer(content):
            tag_content = link_match.group(1); href_match = href_pattern.search(tag_content); rel_match = rel_pattern.search(tag_content)
            if href_match and rel_match:
                url = href_match.group("url")
                if url and not url.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:', 'data:')): result["stylesheets"].append({"url": url, "line": content[:link_match.start()].count('\n') + 1})
    except Exception as e: logger.warning(f"Regex error during HTML stylesheet analysis in {file_path}: {e}")

def _analyze_css_file(file_path: str, content: str, result: Dict[str, Any]) -> None:
    """Analyzes CSS file content using regex."""
    result["imports"] = [] # For @import rules

    try:
        for match in CSS_IMPORT_PATTERN.finditer(content):
             url = match.group(1)
             if url and not url.startswith(('#', 'http:', 'https:', 'data:')): result["imports"].append({"url": url.strip(), "line": content[:match.start()].count('\n') + 1})
    except Exception as e: logger.warning(f"Regex error during CSS import analysis in {file_path}: {e}")

# --- End of dependency_analyzer.py ---