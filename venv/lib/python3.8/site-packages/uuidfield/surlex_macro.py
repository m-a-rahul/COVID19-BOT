# Register a surlex uuid macro.

try:
    import surlex
except ImportError:
    pass
else:
    surlex.register_macro('u', r'[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12}')
