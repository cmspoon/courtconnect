import os
import pytest
import pandas as pd
from courtconnector import build, find

@pytest.fixture
def graph():
    path = os.path.join(os.path.dirname(__file__), "players2.csv")
    df = pd.read_csv(path)
    return build(df)

def test_direct3(graph):
    path1 = find(graph, "Jeff Teague", "Player A")
    path2 = find(graph, "Player A", "Kyle Korver")
    assert (len(path1) + len(path2)) == 4, "Direction connection"
    assert path1[0] == "Jeff Teague" and path1[1] == "Player A" and path2[1] == "Kyle Korver", "Connection found"

def test_indirect3(graph):
    path1 = find(graph, "Jeff Teague", "Player B")
    path2 = find(graph, "Player B", "Al Horford")
    path3 = find(graph, "Al Horford", "Player C")
    path4 = find(graph, "Player C", "Kyle Korver")
    assert (len(path1) + len(path2) + len(path3) + len(path4)) == 8, "Indirect connection"
    assert path1[0] == "Jeff Teague" and path3[0] == "Al Horford" and path4[1] == "Kyle Korver", "Connection found"

def test_none3(graph):
    path1 = find(graph, "Jeff Teague", "FakePlayer D")
    path2 = find (graph, "FakePlayer D", "FakePlayer E")
    assert path1 == None and path2 == None, "No three-man weave found"
