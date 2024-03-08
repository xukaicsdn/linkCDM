import pytest


class TestApi:  # 声明可以被pytest识别的测试类

    @classmethod
    def find_yaml_case(cls):
        pass

    def test_1(self):
        print(1)
        assert 1 == 1

    # @pytest.mark.usefixtures("init_class")
    def test_2(self, init_class):
        aa = init_class
        print(aa, 888888888888)
        assert 1 == 1

    @pytest.fixture
    def my_fixture(self):
        return "Hello, Fixture!"

    def test_func1(self, request: pytest.FixtureRequest):
        my_fixture_value = request.getfixturevalue("init_class")
        print(my_fixture_value)  # Output: Hello, Fixture!

    @pytest.fixture
    def req(self, request: pytest.FixtureRequest):
        return request

    @pytest.mark.skip
    def test_func2(self, req):
        my_fixture_value = req.getfixturevalue("my_fixture")
        print(my_fixture_value)  # Output: Hello, Fixture!


session=''

def test_A():
    session='123'

@pytest.mark.skipif(session != "",reason='session 不存在')
def test_B():
    print(session)


if __name__ == '__main__':
    pytest.main(['-v', '-s',  __file__])
    # pytest.main([__file__,'-v', '-s, "-k", "TestAnimal"])