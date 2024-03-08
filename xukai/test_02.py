import pytest


@pytest.mark.usefixtures("init_class")
class TestAP:
    def test_1(self):
        print(1)
        assert 1==1

    def test_2(self):
        print(2)
        assert 1==1

if __name__ == '__main__':
    pytest.main()
