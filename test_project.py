from project import read_items
import sqlite3
import pytest 

# pytest fixtures - objects that set up certain conditions that are used in testing
# functions that are called before running the actual test functions
# decorator to show next method is pytest fixture
# 
@pytest.fixture
def db():
    # set up in-memory database
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE test_grocery
        (item, quantity)"""
    )
    # sample data to be used
    test_data = [
        ("fruit snacks", "2 boxes"),
        ("bananas", 1),
        ("cherry tomatoes", "1 large container"),
        ("coffee beans", "3 bags")
    ]
    # add into database
    cur.executemany("INSERT INTO test_grocery VALUES(?, ?)", test_data)
    # yield produces values one at a time - optimizes memory usage 
    # (use when want to iterate over a sequence, but don't want to store entire seq in memory)
    yield con

# test if test database connected 
def test_db(db):
    cur = db
    assert len(list(cur.execute("SELECT * FROM test_grocery"))) == 4

