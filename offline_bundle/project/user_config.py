# Clever AI - User Configuration
# Personal settings for Jay's Clever AI system

# User Identity
USER_NAME = "Jay"
USER_EMAIL = "lapirfta@gmail.com"
USER_FULL_NAME = "Jordan Gallegos"

# Tailscale Configuration  
TAILSCALE_ENABLED = False  # Disabled for local-only isolation
TAILSCALE_HOSTNAME = "clever-ai-jay"
TAILSCALE_SSH_ENABLED = True

CLEVER_EXTERNAL_ACCESS = False  # Disabled to ensure local-only access
# Force binding to localhost only
CLEVER_HOST = "127.0.0.1"
CLEVER_PORT = 5000

# Security Settings
ALLOWED_TAILSCALE_DOMAINS = ["gmail.com", "googlemail.com"]
TRUSTED_EMAIL_DOMAINS = ["gmail.com"]

# Development Settings
DEBUG_MODE = False
VERBOSE_LOGGING = True

# Remote Access Notes
# - Tailscale provides secure tunnel without exposing to public internet
# - Only devices in your Tailscale network can access Clever
# - Maintains offline-first principle (no cloud AI dependencies)
# - Email used for Tailscale account identification only
