import os
import pytest
import pandas as pd
from courtconnector import build, find

@pytest.fixture
def graph():
    path = os.path.join(os.path.dirname(__file__), "players1.csv")
    df = pd.read_csv(path)
    return build(df)

def test_direct(graph):
    path = find(graph, "Jeff Teague", "Kyle Korver")
    assert len(path) == 2, "Direction connection"
    assert path[0] == "Jeff Teague" and path[1] == "Kyle Korver", "Connection found"

def test_indirect(graph):
    path = find(graph, "Jeff Teague", "LeBron James")
    assert len(path) == 3, "Indirect connection"
    assert path[0] == "Jeff Teague" and path[1] == "Rajon Rondo" and path[2] == "LeBron James", "Connection found"

def test_none(graph):
    path = find(graph, "Jeff Teague", "Fake Player")
    assert path == None, "No connection found"