"""
User Configuration Module - Personal settings for Jay's Clever AI system.

Why: Centralizes all user-specific configuration including identity, network
     settings, and preferences while maintaining offline-first architecture
     and supporting optional Tailscale integration for secure remote access.

Where: Imported by config.py and app.py during initialization to configure
       Clever AI with user-specific settings and security preferences.

How: Defines constants for user identity, network configuration, security
     settings, and development options with clear documentation for each
     setting and its security implications.
"""

# User Identity Configuration
USER_NAME = "Jay"
USER_EMAIL = "lapirfta@gmail.com" 
USER_FULL_NAME = "Jordan Gallegos"

# Tailscale Network Configuration
TAILSCALE_ENABLED = False  # Disabled for local-only isolation
TAILSCALE_HOSTNAME = "clever-ai-jay"
TAILSCALE_SSH_ENABLED = True

# External Access Control
CLEVER_EXTERNAL_ACCESS = False  # Disabled to ensure local-only access
CLEVER_HOST = "127.0.0.1"  # Force binding to localhost only
CLEVER_PORT = 5000

# Security and Access Control
ALLOWED_TAILSCALE_DOMAINS = ["gmail.com", "googlemail.com"]
TRUSTED_EMAIL_DOMAINS = ["gmail.com"]

# Development and Debug Settings
DEBUG_MODE = False
VERBOSE_LOGGING = True

# Remote Access Architecture Notes:
# - Tailscale provides secure tunnel without exposing to public internet
# - Only devices in your Tailscale network can access Clever
# - Maintains offline-first principle (no cloud AI dependencies)  
# - Email used for Tailscale account identification only
