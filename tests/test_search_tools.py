import sys

sys.path.insert(0, "..")


def test_search_imports():
    """Test that search can be imported."""
    try:
        from tools import search_web
        from config import Config

        print(f"✅ Search imported, Provider: {Config.SEARCH_PROVIDER}")
        return True
    except Exception as e:
        print(f"❌ Search import failed: {e}")
        return False


if __name__ == "__main__":
    if test_search_imports():
        print("\n🎉 Search tests passed!")
    else:
        print("\n❌ Search tests failed")
