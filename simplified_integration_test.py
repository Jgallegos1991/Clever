#!/usr/bin/env python3
"""
Simplified Integration Test for Enhanced Clever AI System

Why: Validates core enhanced capabilities without external dependencies
Where: Tests essential system enhancements for perfect conversational capability
How: Tests system validation, conversation engine, and file access without scheduler

Connects to:
    - system_validator.py: Tests comprehensive system validation
    - enhanced_conversation_engine.py: Tests conversation processing
    - debug_config.py: Uses debugging and logging capabilities
    - All core modules: Integration testing across system components
"""


# Add project root to path
sys.path.insert(0, "/workspaces/projects")

try:
    from system_validator import SystemValidator, validate_system_startup
    from enhanced_conversation_engine import EnhancedConversationEngine
    from debug_config import get_debugger

    print("✅ All enhanced modules imported successfully")
except ImportError as _e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_system_validation():
    """Test comprehensive system validation"""
    print("\n🔍 Testing System Validation...")

    try:
        validation_report = validate_system_startup()

        if validation_report["overall_status"] == "PASS":
            print(
                "✅ System validation passed - "
                f"{validation_report['passed_checks']}"
                f"/{validation_report['total_checks']} checks"
            )
            return True
        else:
            print(
                "❌ System validation failed - "
                f"{validation_report['critical_issues']} critical issues"
            )
            return False

    except Exception as _e:
        print(f"❌ Validation test failed: {e}")
        return False


def test_enhanced_conversation():
    """Test enhanced conversation capabilities"""
    print("\n💬 Testing Enhanced Conversation Engine...")

    try:
        engine = EnhancedConversationEngine()

        # Test conversation processing
        result = engine.process_conversation(
            "Analyze the current system and provide an overview"
        )

        success = (
            bool(result.get("response"))
            and len(result.get("response", "")) > 50
            and bool(result.get("analysis"))
        )

        if success:
            print(
                "✅ Enhanced conversation test passed - "
                f"Response length: {len(result.get('response', ''))}"
            )
            print(f"    Analysis provided: {bool(result.get('analysis'))}")
            print(f"    Memory context: {bool(result.get('memory_context'))}")
            return True
        else:
            print("❌ Enhanced conversation test failed - insufficient response")
            return False

    except Exception as _e:
        print(f"❌ Conversation test failed: {e}")
        return False


def test_file_access():
    """Test file access capability"""
    print("\n📁 Testing File Access Capability...")

    try:
        engine = EnhancedConversationEngine()

        # Test reading a specific file using the actual method
        config_path = Path("/workspaces/projects/config.py")
        if config_path.exists():
            content = engine._safe_read_file(config_path)
            file_read_success = bool(content and len(content) > 10)
        else:
            file_read_success = False

        # Test file operations identification
        operations = engine._identify_file_operations(
            "Read the config file and tell me about the settings"
        )
        operations_success = len(operations) > 0

        success = file_read_success and operations_success

        if success:
            print(
                "✅ File access test passed - "
                f"config.py readable, {len(operations)} operations identified"
            )
            return True
        else:
            print("❌ File access test failed")
            return False

    except Exception as _e:
        print(f"❌ File access test failed: {e}")
        return False


def test_conversation_with_file_analysis():
    """Test conversation with file analysis capability"""
    print("\n🔗 Testing Conversation with File Analysis...")

    try:
        engine = EnhancedConversationEngine()

        # Test complex request that requires file access
        result = engine.process_conversation(
            "Tell me about the configuration settings available in this project"
        )

        success = (
            bool(result.get("response"))
            and len(result.get("response", "")) > 100
            and "config" in result.get("response", "").lower()
        )

        if success:
            print("✅ File analysis conversation test passed")
            return True
        else:
            print("❌ File analysis conversation test failed")
            return False

    except Exception as _e:
        print(f"❌ File analysis test failed: {e}")
        return False


def main():
    """Run simplified integration test"""
    print("🚀 Starting Simplified Integration Test")
    print("=" * 50)

    tests = [
        ("System Validation", test_system_validation),
        ("Enhanced Conversation", test_enhanced_conversation),
        ("File Access", test_file_access),
        ("Conversation with File Analysis", test_conversation_with_file_analysis),
    ]

    passed = 0
    total = len(tests)
    results = []

    for test_name, test_func in tests:
        print(f"\n Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                passed += 1
        except Exception as _e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Final results
    print("\n" + "=" * 50)
    print("🏁 SIMPLIFIED INTEGRATION TEST RESULTS")
    print("=" * 50)

    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")

    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED ({passed}/{total})")
        print("🔥 Clever AI enhanced capabilities validated!")
        print("💬 System ready for maximum conversational capability!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} tests failed ({passed}/{total} passed)")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
