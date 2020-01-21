import pytest
from db_manager import DbManager
from db_manager import DbManagerError


def test_get_instance():
    instance = DbManager.get_instance()
    assert type(instance) == DbManager


def test_run_sql():
    db = DbManager.get_instance()
    with pytest.raises(DbManagerError) as error_info:
        db.run_sql("blablala1")
        db.run_sql("INSERT INTO data VALUES (?,?,?,?)", [(1, 2, 3, 4)])
        db.run_sql("INSERT INTO cities VALUES (?,?,?,?,?)", [(3, "4", "5", "6", "&")])
