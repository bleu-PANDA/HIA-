def get_svg_icon(name, size=20, color="currentColor", extra_style=""):
    """
    Returns an inline SVG string for the requested Lucide icon.
    """
    svg_paths = {
        "ClipboardList": (
            '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>'
            '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
            '<path d="M9 14h6"/><path d="M9 18h6"/><path d="M9 10h6"/>'
        ),
        "MessageCircle": (
            '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>'
        ),
        "Calendar": (
            '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>'
            '<line x1="16" x2="16" y1="2" y2="6"/>'
            '<line x1="8" x2="8" y1="2" y2="6"/>'
            '<line x1="3" x2="21" y1="10" y2="10"/>'
        ),
        "Clock3": (
            '<circle cx="12" cy="12" r="10"/>'
            '<polyline points="12 6 12 12 16.5 12"/>'
        ),
        "ShieldCheck": (
            '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
            '<path d="m9 11 2 2 4-4"/>'
        ),
        "User": (
            '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>'
            '<circle cx="12" cy="7" r="4"/>'
        ),
        "LogOut": (
            '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>'
            '<polyline points="16 17 21 12 16 7"/>'
            '<line x1="21" x2="9" y1="12" y2="12"/>'
        ),
        "Shield": (
            '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        ),
        "Stethoscope": (
            '<path d="M4.82 7.26A10 10 0 0 0 12 22a10 10 0 0 0 7.18-14.74"/>'
            '<path d="M12 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>'
            '<path d="M17 3h4v3a2 2 0 0 1-2 2h-2V3Z"/>'
            '<path d="M12 15a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/>'
        ),
        "Mail": (
            '<rect width="20" height="16" x="2" y="4" rx="2"/>'
            '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'
        ),
        "Lock": (
            '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
            '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
        ),
        "Eye": (
            '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>'
            '<circle cx="12" cy="12" r="3"/>'
        )
    }
    
    path_data = svg_paths.get(name)
    if not path_data:
        return ""
        
    style_attr = f' style="{extra_style}"' if extra_style else ''
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-{name.lower()}"{style_attr}>'
        f'{path_data}'
        f'</svg>'
    )

def get_image_base64(path):
    """
    Reads a local image file and returns its base64 data URL.
    """
    import base64
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except Exception:
        return ""

