class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def format_header(text):
    return f"{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}"

def format_success(text):
    return f"{Colors.GREEN}✓ {text}{Colors.ENDC}"

def format_error(text):
    return f"{Colors.FAIL}✗ {text}{Colors.ENDC}"

def format_warning(text):
    return f"{Colors.WARNING}! {text}{Colors.ENDC}"

def format_info(text):
    return f"{Colors.CYAN}ℹ {text}{Colors.ENDC}"

def format_manga_title(text):
    return f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.ENDC}"
