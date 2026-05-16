import pytest

from service import read_csv


class TestDataImport():

    def test_normal_import(self):
        path = "./data/input/forge1d_demand.csv"
        (header, body) = read_csv(path)

        assert header == (['part_id', 'length', 'qty'])
        assert body[0] == ({'part_id':'ST01', 'length':'2245', 'qty':'1'})
        assert len(body) == 34

