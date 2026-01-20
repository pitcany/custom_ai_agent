import sys

sys.path.insert(0, "..")


def test_copy_file():
    """Test copy_file tool."""
    from tools import copy_file, write_file
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "source.txt"
        dst = Path(tmpdir) / "dest.txt"

        write_file.invoke({"path": str(src), "content": "test content"})
        result = copy_file.invoke({"source": str(src), "destination": str(dst)})

        assert "Successfully copied" in result
        assert dst.exists()
        assert dst.read_text() == "test content"

    print("✅ Copy file test passed")


def test_delete_file():
    """Test delete_file tool."""
    from tools import delete_file, write_file
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "to_delete.txt"
        write_file.invoke({"path": str(test_file), "content": "delete me"})

        result = delete_file.invoke({"path": str(test_file)})

        assert "Successfully deleted" in result or "not found" in result.lower()
        assert not test_file.exists()

    print("✅ Delete file test passed")


def test_search_files():
    """Test search_files tool."""
    from tools import search_files, write_file
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        write_file.invoke({"path": f"{tmpdir}/file1.txt", "content": "content 1"})
        write_file.invoke({"path": f"{tmpdir}/file2.txt", "content": "content 2"})
        write_file.invoke({"path": f"{tmpdir}/other.py", "content": "code"})

        result = search_files.invoke({"directory": tmpdir, "pattern": "file*.txt"})

        assert "Found 2 files" in result
        assert "file1.txt" in result and "file2.txt" in result
        assert "other.py" not in result

    print("✅ Search files test passed")


if __name__ == "__main__":
    test_copy_file()
    test_delete_file()
    test_search_files()
    print("\n🎉 All file tools tests passed!")
