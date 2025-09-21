"""
User Configuration - Jay's Personal Cognitive Partnership Settings

Why: Jay's personalized configuration for authentic relationship building with Clever.
     Stores preferences that help Clever become the perfect digital brain extension
     and cognitive partner while maintaining complete privacy and local control.

Where: Core of Clever's single-user design - imported by all systems that need to
       understand Jay's preferences, communication style, and cognitive enhancement
       needs for authentic partnership.

How: Personal settings that enable Clever to grow as Jay's life companion and
     digital other half. Supports organic relationship building without fake
     familiarity - real connection that develops over time.
"""

# User Identity Configuration
USER_NAME = "Jay"
USER_EMAIL = "lapirfta@gmail.com"
USER_FULL_NAME = "Jordan Gallegos"

# Family and Personal Details
FAMILY_INFO = {
    "mom": "Lucy",
    "brothers": ["Ronnie", "Peter"],
    "sons": {
        "Josiah": {"lives_with": "Jay", "location": "local"},
        "Jonah": {"lives_with": "mom", "location": "Tijuana"}
    }
}

# Clever's Personality Settings
CLEVER_PERSONALITY = {
    "relationship_level": "childhood_friend",  # How familiar Clever should be
    "casual_speech": True,  # Use casual language and slang
    "remember_family": True,  # Reference family members naturally
    "street_smart": True,  # Use street-smart, natural speech patterns
    "check_in_frequency": "often"  # How often to ask about family
}


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
