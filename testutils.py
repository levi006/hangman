def test_input(*args):
    """Utility function for testing raw_input."""
    import sys
    from cStringIO import StringIO
    inputs = StringIO("\n".join(args) + "\n")
    sys.stdin = inputs