import os
import sys
import re
from collections import defaultdict

# -----------------------------
#  PATHS & APP INFO
# -----------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_NAME = os.path.basename(APP_DIR)

VIEW_FILE = os.path.join(APP_DIR, "views.py")
URLS_FILE = os.path.join(APP_DIR, "urls.py")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates", APP_NAME)
NAV_FILE = os.path.join(TEMPLATES_DIR, "nav.html")
BASE_TEMPLATE = os.path.join(TEMPLATES_DIR, "base.html")
FOOTER_FILE = os.path.join(TEMPLATES_DIR, "footer.html")


# Pages that cannot be deleted or renamed
PROTECTED_PAGES = {"home", "nav", "footer", "sidebar"}


# -----------------------------
#  COLOURS (for CLI)
# -----------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"


def c(text, colour):
    return f"{colour}{text}{RESET}"


# -----------------------------
#  PAGE NAME HELPERS (support subfolders like 'reports/monthly')
# -----------------------------
def normalise_page_id(raw: str) -> str:
    """Clean user input like ' //Reports//Monthly/ ' â†’ 'reports/monthly'."""
    raw = raw.strip().strip("/").lower()
    raw = re.sub(r"/+", "/", raw)
    return raw


def valid_page_id(page_id: str) -> bool:
    """
    Check that each segment in 'reports/monthly' is valid:
    letters/numbers/underscore, starts with a letter.
    """
    if not page_id:
        return False
    parts = page_id.split("/")
    return all(re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", p) for p in parts)


def view_name_from_page(page_id: str) -> str:
    """'reports/monthly' â†’ 'reports_monthly' (for Python function name)."""
    return page_id.replace("/", "_")


def url_path_from_page(page_id: str) -> str:
    """'reports/monthly_report' â†’ 'reports/monthly-report' (for URL path)."""
    return "/".join(part.replace("_", "-") for part in page_id.split("/"))


# -----------------------------
#  HELPERS
# -----------------------------
def valid_page_name(name: str) -> bool:
    """Only allow: letters, numbers, underscore. Must start with a letter."""
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name))


def ensure_views_file():
    """Ensure views.py exists and imports render."""
    if not os.path.exists(VIEW_FILE):
        with open(VIEW_FILE, "w") as f:
            f.write("from django.shortcuts import render\n")
        print(c("âœ” Created views.py", GREEN))

    with open(VIEW_FILE, "r") as f:
        content = f.read()

    if "from django.shortcuts import render" not in content:
        with open(VIEW_FILE, "w") as f:
            f.write("from django.shortcuts import render\n\n" + content)
        print(c("âœ” Added 'render' import to views.py", GREEN))


def strip_bom(filepath):
    """Remove UTF-8 BOM (U+FEFF) if present in a file."""
    if not os.path.exists(filepath):
        return

    # utf-8-sig will read and automatically drop BOM if it exists
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = f.read()

    # write it back as normal UTF-8 with no BOM
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)


def ensure_urls_file():
    """Ensure urls.py exists, is clean (no BOM), and contains 'from . import views'."""
    # If file doesn't exist, create a clean one
    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, "w", encoding="utf-8") as f:
            f.write(
                "from django.urls import path\n"
                "from . import views\n\n"
                "urlpatterns = [\n"
                "]\n"
            )
        print("âœ” Created urls.py")
        return

    # Clean BOM if some editor or copy-paste added it
    strip_bom(URLS_FILE)

    # Now work with the cleaned file
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not any(line.strip() == "from . import views" for line in lines):
        for i, line in enumerate(lines):
            if line.startswith("from django.urls"):
                lines.insert(i + 1, "from . import views\n")
                break
        else:
            lines.insert(0, "from . import views\n")

        with open(URLS_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print("âœ” Added 'from . import views' to urls.py")


def ensure_nav_template():
    """Create templates/<app>/nav.html if missing."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    if os.path.exists(NAV_FILE):
        return

    with open(NAV_FILE, "w") as f:
        f.write(
            "{% load static %}\n"
            '<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">\n'
            '  <div class="container-fluid">\n'
            '  <a class="navbar-brand" href="/">'
            f'<img src="{{% static \'images/logo.png\' %}}" style="height: 40px; margin-top: -5px" />'
            f"    {APP_NAME.title()}"
            "    </a>"
            '    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav">\n'
            '      <span class="navbar-toggler-icon"></span>\n'
            "    </button>\n"
            '    <div class="collapse navbar-collapse" id="mainNav">\n'
            '      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">\n'
            "        <!-- AUTO-GENERATED NAV START -->\n"
            "        <!-- items will be injected by menu.py -->\n"
            "        <!-- AUTO-GENERATED NAV END -->\n"
            "      </ul>\n"
            "    </div>\n"
            "  </div>\n"
            "</nav>\n"
        )

    print(c(f"âœ” Created nav template: {NAV_FILE}", GREEN))


def ensure_footer_template():
    """Create templates/<app>/footer.html if missing."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    if os.path.exists(FOOTER_FILE):
        return

    with open(FOOTER_FILE, "w") as f:
        f.write(
            '<footer class="bg-dark text-white text-center py-3 mt-5">\n'
            '  <div class="container">\n'
            "    <small>&copy; 2025 Your Project Name. All rights reserved.</small>\n"
            "  </div>\n"
            "</footer>\n"
        )

    print(c(f"âœ” Created footer template: {FOOTER_FILE}", GREEN))


def ensure_base_template():
    """
    Create templates/<app>/base.html if missing and make sure it includes nav.html and footer.html.
    """
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    # Always ensure nav + footer exist first
    ensure_nav_template()
    ensure_footer_template()

    include_nav_double = f'{{% include "{APP_NAME}/nav.html" %}}'
    include_nav_single = f"{{% include '{APP_NAME}/nav.html' %}}"

    include_footer_double = f'{{% include "{APP_NAME}/footer.html" %}}'
    include_footer_single = f"{{% include '{APP_NAME}/footer.html' %}}"

    if not os.path.exists(BASE_TEMPLATE):
        # brand new base.html using nav + footer include
        with open(BASE_TEMPLATE, "w") as f:
            f.write(
                "<!DOCTYPE html>\n"
                "<html lang='en'>\n"
                "<head>\n"
                "    <meta charset='utf-8'>\n"
                "    <meta name='viewport' content='width=device-width, initial-scale=1'>\n"
                f"    <title>{{% block title %}}{APP_NAME.title()}{{% endblock %}}</title>\n"
                "    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>\n"
                "</head>\n"
                "<body class='bg-light'>\n"
                f'    {{% include "{APP_NAME}/nav.html" %}}\n'
                "    <div class='container my-4'>\n"
                "        {% block content %}{% endblock %}\n"
                "    </div>\n"
                f'    {{% include "{APP_NAME}/footer.html" %}}\n'
                "    <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'></script>\n"
                "</body>\n"
                "</html>\n"
            )

        print(c(f"âœ” Created base template: {BASE_TEMPLATE}", GREEN))
        return

    # If base.html already exists, ensure it has both includes
    with open(BASE_TEMPLATE, "r") as f:
        content = f.read()

    nav_present = include_nav_double in content or include_nav_single in content
    footer_present = (
        include_footer_double in content or include_footer_single in content
    )

    lines = content.splitlines(keepends=True)
    changed = False

    if not nav_present:
        include_line = f'    {{% include "{APP_NAME}/nav.html" %}}\n'
        inserted = False

        for i, line in enumerate(lines):
            if "<body" in line:
                lines.insert(i + 1, include_line)
                inserted = True
                break

        if not inserted:
            lines.insert(0, include_line)

        changed = True
        print(c("âœ” Updated base.html to include nav.html", GREEN))

    if not footer_present:
        footer_line = f'    {{% include "{APP_NAME}/footer.html" %}}\n'
        inserted = False

        # Try to insert before closing </body> or before the JS script
        for i, line in enumerate(lines):
            if "bootstrap.bundle.min.js" in line or "</body>" in line:
                lines.insert(i, footer_line)
                inserted = True
                break

        if not inserted:
            lines.append(footer_line)

        changed = True
        print(c("âœ” Updated base.html to include footer.html", GREEN))

    if changed:
        with open(BASE_TEMPLATE, "w") as f:
            f.writelines(lines)


# -----------------------------
#  CREATE PAGE (INLINE)
# -----------------------------
def create_view(page_name: str):
    ensure_views_file()

    with open(VIEW_FILE, "r") as f:
        content = f.read()

    view_name = view_name_from_page(page_name)
    func_def = f"def {view_name}(request):"

    if func_def in content:
        print(c(f"âš  View '{view_name}()' already exists. Skipping.", YELLOW))
        return

    template_ref = f"'{APP_NAME}/{page_name}.html'"

    with open(VIEW_FILE, "a") as f:
        f.write(
            f"\n\n"
            f"def {view_name}(request):\n"
            f"    return render(request, {template_ref})\n"
        )

    print(c(f"âœ” Added view function '{view_name}()' to views.py", GREEN))


def create_template(page_name: str):
    ensure_base_template()

    path = os.path.join(TEMPLATES_DIR, f"{page_name}.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        print(c(f"âš  Template '{page_name}.html' already exists. Skipping.", YELLOW))
        return

    last_part = page_name.split("/")[-1]
    nice_title = last_part.replace("_", " ").title()

    with open(path, "w") as f:
        f.write(
            "{% extends '" + APP_NAME + "/base.html' %}\n\n"
            "{% block title %}"
            + nice_title
            + " | "
            + APP_NAME.title()
            + "{% endblock %}\n\n"
            "{% block content %}\n"
            f"    <h1>{nice_title}</h1>\n"
            "    <p>This page was generated automatically by <code>menu.py</code>.</p>\n"
            "{% endblock %}\n"
        )

    print(c(f"âœ” Created template: {path}", GREEN))


def create_url(page_name: str):
    strip_bom(URLS_FILE)
    ensure_urls_file()

    view_name = view_name_from_page(page_name)
    url_path = url_path_from_page(page_name)

    with open(URLS_FILE, "r") as f:
        lines = f.readlines()

    new_route = f"    path('{url_path}/', views.{view_name}, name='{view_name}'),\n"

    if any(new_route.strip() == line.strip() for line in lines):
        print(c(f"âš  URL for '{page_name}' already exists. Skipping.", YELLOW))
        return

    for i, line in enumerate(lines):
        if line.strip() == "]":
            lines.insert(i, new_route)
            break

    with open(URLS_FILE, "w") as f:
        f.writelines(lines)

    print(c(f"âœ” Added URL route for '{page_name}' â†’ /{url_path}/", GREEN))


# -----------------------------
#  DELETE PAGE (INLINE)
# -----------------------------
def delete_view(page_name: str):
    if not os.path.exists(VIEW_FILE):
        print(
            c(f"âš  views.py not found, skipping view removal for '{page_name}'.", YELLOW)
        )
        return

    with open(VIEW_FILE, "r") as f:
        lines = f.readlines()

    view_name = view_name_from_page(page_name)
    func_pattern = f"def {view_name}(request):"
    start_idx = None

    for i, line in enumerate(lines):
        if line.strip().startswith(func_pattern):
            start_idx = i
            break

    if start_idx is None:
        print(c(f"âš  View function '{view_name}()' not found in views.py.", YELLOW))
        return

    end_idx = start_idx + 1
    while end_idx < len(lines):
        stripped = lines[end_idx].lstrip()
        if stripped.startswith("def ") and not stripped.startswith(func_pattern):
            break
        end_idx += 1

    while end_idx < len(lines) and lines[end_idx].strip() == "":
        end_idx += 1

    del lines[start_idx:end_idx]

    with open(VIEW_FILE, "w") as f:
        f.writelines(lines)

    print(c(f"âœ” Removed view function '{view_name}()' from views.py", GREEN))


def delete_template(page_name: str):
    path = os.path.join(TEMPLATES_DIR, f"{page_name}.html")

    if not os.path.exists(path):
        print(c(f"âš  Template '{page_name}.html' not found, skipping.", YELLOW))
        return

    os.remove(path)
    print(c(f"âœ” Deleted template: {path}", GREEN))


def delete_url(page_name: str):
    strip_bom(URLS_FILE)
    if not os.path.exists(URLS_FILE):
        print(
            c(f"âš  urls.py not found, skipping URL removal for '{page_name}'.", YELLOW)
        )
        return

    with open(URLS_FILE, "r") as f:
        lines = f.readlines()

    view_name = view_name_from_page(page_name)
    url_path = url_path_from_page(page_name)
    new_lines = []
    removed = False

    for line in lines:
        if (
            f"views.{view_name}" in line
            or f"name='{view_name}'" in line
            or f"'{url_path}/'" in line
        ):
            removed = True
            continue
        new_lines.append(line)

    if not removed:
        print(c(f"âš  No URL route found for '{page_name}' in urls.py.", YELLOW))
    else:
        with open(URLS_FILE, "w") as f:
            f.writelines(new_lines)
        print(c(f"âœ” Removed URL route for '{page_name}' from urls.py", GREEN))


# -----------------------------
#  PAGE LISTING
# -----------------------------
def get_pages():
    """Return list of page ids like 'page1' or 'reports/monthly'."""
    if not os.path.exists(TEMPLATES_DIR):
        return []

    pages = []

    for root, _, files in os.walk(TEMPLATES_DIR):
        for f in files:
            if not f.endswith(".html"):
                continue
            if f in {"base.html", "nav.html"}:
                continue

            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(
                full_path, TEMPLATES_DIR
            )  # e.g. 'reports/monthly.html'
            rel_no_ext = rel_path[:-5]  # remove '.html'
            page_id = rel_no_ext.replace(os.sep, "/")

            if page_id not in PROTECTED_PAGES:
                pages.append(page_id)

    return sorted(pages)


def list_pages():
    """Print all page templates, then wait for user input."""
    pages = get_pages()

    if not pages:
        print(c("âš  No page templates found (only maybe base.html).", YELLOW))
        input(c("\nPress any key to return to menu...", CYAN))
        return

    print(f"\n{c('Pages in app', CYAN)} {c(APP_NAME, BOLD)}:\n")
    for i, p in enumerate(pages, start=1):
        print(f" {c(i, CYAN)}. {p}")

    input(c("\nPress any key to continue...", CYAN))


# -----------------------------
#  NAVIGATION UPDATER
# -----------------------------
def update_navigation():
    """
    Update the navigation links in nav.html based on existing pages.

    Grouping (folder-based):
      - 'reports' root page â†’ top-level or first item in dropdown
      - 'reports/monthly', 'reports/summary' â†’ dropdown items under Reports
      - simple pages ('about') â†’ top-level links
    """
    pages = get_pages()

    if not os.path.exists(NAV_FILE):
        print(c("âš  nav.html not found, navigation not updated.", YELLOW))
        return

    def title_from(s):
        return s.replace("_", " ").title()

    singles = set()
    grouped = defaultdict(list)

    for page in pages:
        parts = page.split("/")
        if len(parts) == 1:
            singles.add(page)
        else:
            prefix = parts[0]
            grouped[prefix].append(page)

    handled = set()

    lines = []
    lines.append("        <!-- AUTO-GENERATED NAV START -->\n")

    # Dropdowns for grouped pages
    for prefix in sorted(grouped.keys()):
        group_pages = sorted(grouped[prefix])
        handled.update(group_pages)

        has_root = prefix in singles
        if has_root:
            handled.add(prefix)
            singles.discard(prefix)

        lines.append('        <li class="nav-item dropdown">\n')
        lines.append(
            f'          <a class="nav-link dropdown-toggle" href="#" role="button" '
            f'data-bs-toggle="dropdown" aria-expanded="false">{title_from(prefix)}</a>\n'
        )
        lines.append('          <ul class="dropdown-menu dropdown-menu-end">\n')

        # Root page /prefix/
        if has_root:
            slug = url_path_from_page(prefix)
            label = title_from(prefix)
            lines.append(
                f'            <li><a class="dropdown-item" href="/{slug}/">{label}</a></li>\n'
            )

        # Child pages /prefix/.../
        for p in group_pages:
            if p == prefix:
                continue
            slug = url_path_from_page(p)
            suffix = p.split("/")[-1]
            label = title_from(suffix)
            lines.append(
                f'            <li><a class="dropdown-item" href="/{slug}/">{label}</a></li>\n'
            )

        lines.append("          </ul>\n")
        lines.append("        </li>\n")

    # Simple pages (no folder)
    for page in sorted(pages):
        if page in handled:
            continue
        slug = url_path_from_page(page)
        label = title_from(page.split("/")[-1])
        lines.append(
            f'        <li class="nav-item"><a class="nav-link" href="/{slug}/">{label}</a></li>\n'
        )

    lines.append("        <!-- AUTO-GENERATED NAV END -->\n")

    nav_block = "".join(lines)

    with open(NAV_FILE, "r") as f:
        content = f.read()

    start_tag = "<!-- AUTO-GENERATED NAV START -->"
    end_tag = "<!-- AUTO-GENERATED NAV END -->"

    if start_tag in content and end_tag in content:
        start_idx = content.index(start_tag)
        end_idx = content.index(end_tag) + len(end_tag)
        new_content = content[:start_idx] + nav_block + content[end_idx:]
    else:
        split_lines = content.splitlines(keepends=True)
        inserted = False
        for i, line in enumerate(split_lines):
            if "navbar-nav" in line and "<ul" in line:
                split_lines.insert(i + 1, nav_block)
                inserted = True
                break
        if not inserted:
            split_lines.append("\n" + nav_block)
        new_content = "".join(split_lines)

    with open(NAV_FILE, "w") as f:
        f.write(new_content)

    print(c("âœ” Navigation in nav.html updated.", GREEN))


# -----------------------------
#  MENU ACTIONS
# -----------------------------
def run_createpages():
    """Ask for page names and create them (view + template + URL)."""
    names = input("Enter page name(s) to CREATE (space-separated): ").strip()
    if not names:
        print(c("No names entered, cancelled.\n", YELLOW))
        return

    raw_names = names.split()
    pages = []
    seen = set()

    for name in raw_names:
        page_id = normalise_page_id(name)
        if not valid_page_id(page_id):
            print(
                c(
                    f"âŒ Invalid page name '{name}'. Use letters, numbers, underscores and '/'.",
                    RED,
                )
            )
            continue
        if page_id not in seen:
            seen.add(page_id)
            pages.append(page_id)

    if not pages:
        print(c("No valid page names. Cancelled.\n", YELLOW))
        return

    print(f"\nCreating pages in app {c(APP_NAME, BOLD)}: {', '.join(pages)}\n")

    for page in pages:
        print(c(f"=== {page} ===", CYAN))
        create_view(page)
        create_template(page)
        create_url(page)
        print()

    update_navigation()
    print(c("ðŸŽ‰ All selected pages created successfully!\n", GREEN))


def run_deletepages():
    """Show numbered list of pages, allow name/number/range input, then delete."""
    pages = get_pages()
    if not pages:
        print(c("âš  No pages available to delete.", YELLOW))
        return

    print(f"\n{c('Pages in', CYAN)} {c(APP_NAME, BOLD)}:\n")
    for i, p in enumerate(pages, start=1):
        print(f" {c(i, CYAN)}. {p}")
    print()

    raw = input(
        "Enter page NAME(S), NUMBER(S), or RANGE(S) to delete (e.g. '2 5 home 3-4'):\n> "
    ).strip()

    if not raw:
        print(c("No input provided, cancelled.\n", YELLOW))
        return

    tokens = raw.split()
    selected = []
    seen = set()

    for item in tokens:
        if re.match(r"^\d+-\d+$", item):
            start_str, end_str = item.split("-")
            start = int(start_str)
            end = int(end_str)
            if start > end:
                start, end = end, start
            for n in range(start, end + 1):
                idx = n - 1
                if 0 <= idx < len(pages):
                    name = pages[idx]
                    if name not in seen:
                        seen.add(name)
                        selected.append(name)
                else:
                    print(c(f"âš  Number '{n}' is out of range, skipping.", YELLOW))
        elif item.isdigit():
            idx = int(item) - 1
            if 0 <= idx < len(pages):
                name = pages[idx]
                if name not in seen:
                    seen.add(name)
                    selected.append(name)
            else:
                print(c(f"âš  Number '{item}' is out of range, skipping.", YELLOW))
        else:
            name = item.lower()
            if name in pages and name not in seen:
                seen.add(name)
                selected.append(name)
            elif name not in pages:
                print(c(f"âš  Page '{name}' not found, skipping.", YELLOW))

    if not selected:
        print(c("No valid pages selected. Cancelled.\n", YELLOW))
        return

    selected = [p for p in selected if p not in PROTECTED_PAGES]

    if not selected:
        print(c("ðŸš« Selected pages are protected and cannot be deleted.", RED))
        return

    print("\nYou are about to delete these pages:")
    for p in selected:
        print(" -", c(p, RED))

    confirm = input(c("Are you sure? (y/N): ", YELLOW)).strip().lower()
    if confirm not in ("y", "yes"):
        print(c("Deletion cancelled.\n", YELLOW))
        return

    for page_name in selected:
        print(c(f"\n=== Deleting page: {page_name} ===", CYAN))
        delete_view(page_name)
        delete_template(page_name)
        delete_url(page_name)

    update_navigation()
    print(c("\nðŸ—‘ï¸  Done deleting requested pages.\n", GREEN))


# -----------------------------
#  RENAME PAGE
# -----------------------------
def rename_in_views(old: str, new: str):
    if not os.path.exists(VIEW_FILE):
        print(c("âš  views.py not found, skipping views rename.", YELLOW))
        return

    with open(VIEW_FILE, "r") as f:
        content = f.read()

    old_def = f"def {view_name_from_page(old)}(request):"
    new_def = f"def {view_name_from_page(new)}(request):"

    if old_def not in content:
        print(c(f"âš  View '{old}()' not found in views.py.", YELLOW))
        return

    content = content.replace(old_def, new_def)

    old_tpl = f"'{APP_NAME}/{old}.html'"
    new_tpl = f"'{APP_NAME}/{new}.html'"
    content = content.replace(old_tpl, new_tpl)

    with open(VIEW_FILE, "w") as f:
        f.write(content)

    print(c(f"âœ” Renamed view '{old}' â†’ '{new}' in views.py", GREEN))


def rename_in_template(old: str, new: str):
    old_path = os.path.join(TEMPLATES_DIR, f"{old}.html")
    new_path = os.path.join(TEMPLATES_DIR, f"{new}.html")

    if not os.path.exists(old_path):
        print(c(f"âš  Template '{old}.html' not found, skipping.", YELLOW))
        return

    if os.path.exists(new_path):
        print(c(f"âš  Template '{new}.html' already exists, not overwriting.", YELLOW))
        return

    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    os.rename(old_path, new_path)
    print(c(f"âœ” Renamed template '{old}.html' â†’ '{new}.html'", GREEN))


def rename_in_urls(old: str, new: str):
    strip_bom(URLS_FILE)
    if not os.path.exists(URLS_FILE):
        print(c("âš  urls.py not found, skipping urls rename.", YELLOW))
        return

    with open(URLS_FILE, "r") as f:
        lines = f.readlines()

    old_url = url_path_from_page(old)
    new_url = url_path_from_page(new)
    old_view = view_name_from_page(old)
    new_view = view_name_from_page(new)

    new_lines = []
    changed_any = False

    for line in lines:
        original = line

        if (
            f"views.{old_view}" in line
            or f"name='{old_view}'" in line
            or f"'{old_url}/'" in line
        ):
            line = line.replace(f"views.{old_view}", f"views.{new_view}")
            line = line.replace(f"name='{old_view}'", f"name='{new_view}'")
            line = line.replace(f"'{old_url}/'", f"'{new_url}/'")
            changed_any = True

        new_lines.append(line)

    if not changed_any:
        print(c(f"âš  No URL entry found for '{old}' in urls.py.", YELLOW))
    else:
        with open(URLS_FILE, "w") as f:
            f.writelines(new_lines)
        print(c(f"âœ” Updated URL route from '{old}' â†’ '{new}' in urls.py", GREEN))


def run_rename_page():
    pages = get_pages()

    if not pages:
        print(c("âš  No pages available to rename.", YELLOW))
        return

    print(f"\n{c('Pages in', CYAN)} {c(APP_NAME, BOLD)}:\n")
    for i, p in enumerate(pages, start=1):
        print(f" {c(i, CYAN)}. {p}")
    print()

    old_input = input("Enter OLD page name or number: ").strip().lower()
    if not old_input:
        print(c("Old page value cannot be empty.\n", YELLOW))
        return

    if old_input.isdigit():
        idx = int(old_input) - 1
        if 0 <= idx < len(pages):
            old = pages[idx]
        else:
            print(c("âš  Number out of range.\n", YELLOW))
            return
    else:
        old = old_input

    if old in PROTECTED_PAGES:
        print(c(f"ðŸš« '{old}' is a protected page and cannot be renamed.\n", RED))
        return

    if old not in pages:
        print(c(f"âš  Page '{old}' not found.\n", YELLOW))
        return

    new = input("Enter NEW page name: ").strip().lower()

    if not new:
        print(c("New page name cannot be empty.\n", YELLOW))
        return

    if not valid_page_name(new):
        print(
            c(
                "âŒ Invalid new page name. Use letters, numbers, underscores; start with a letter.\n",
                RED,
            )
        )
        return

    if old == new:
        print(c("Old and new names are the same, nothing to do.\n", YELLOW))
        return

    print(
        f"\nRenaming page {c(old, CYAN)} â†’ {c(new, CYAN)} in app {c(APP_NAME, BOLD)}...\n"
    )
    rename_in_views(old, new)
    rename_in_template(old, new)
    rename_in_urls(old, new)
    update_navigation()
    print(c("\nâœ… Rename process complete.\n", GREEN))


# -----------------------------
#  MAIN MENU LOOP
# -----------------------------
def main():
    while True:
        print(f"\n{c('=== Django App Menu for', CYAN)} {c(APP_NAME, BOLD)} ===")
        print(c("1.", CYAN), "Create page(s)")
        print(c("2.", CYAN), "Delete page(s)")
        print(c("3.", CYAN), "Rename a page")
        print(c("4.", CYAN), "List pages")
        print(c("5.", CYAN), "Update navigation only")
        print(c("6.", CYAN), "Exit")

        choice = input("Choose an option (1â€“6): ").strip()

        if choice == "1":
            run_createpages()
        elif choice == "2":
            run_deletepages()
        elif choice == "3":
            run_rename_page()
        elif choice == "4":
            list_pages()
        elif choice == "5":
            update_navigation()
        elif choice == "6":
            print("Goodbye ðŸ‘‹")
            break
        else:
            print(c("Invalid choice, try again.\n", YELLOW))


if __name__ == "__main__":
    main()
