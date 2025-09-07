# Clever AI - User Configuration
# Personal settings for Jay's Clever AI system

# User Identity
USER_NAME = "Jay"
USER_EMAIL = "lapirfta@gmail.com"
USER_FULL_NAME = "Jordan Gallegos"

# Tailscale Configuration  
TAILSCALE_ENABLED = True
TAILSCALE_HOSTNAME = "clever-ai-jay"
TAILSCALE_SSH_ENABLED = True

# Network Configuration
CLEVER_EXTERNAL_ACCESS = True  # Allow external access via Tailscale
CLEVER_HOST = "0.0.0.0"  # Listen on all interfaces when Tailscale is active
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
