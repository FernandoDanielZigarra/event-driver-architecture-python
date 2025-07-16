def test_env_loaded():
    import os
    assert os.getenv("DATABASE_NAME") == "postgres"
    assert os.getenv("DATABASE_USER") == "postgres"
