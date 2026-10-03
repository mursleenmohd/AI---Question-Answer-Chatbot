from backend.tools import calculator
def test_calculator_add():
    result = calculator.invoke(
        {
            "a": 10,
            "b": 5,
            "operation": "add",
        }
    )
    assert result == 15

def test_calculator_multiply():
    result = calculator.invoke(
        {
            "a": 10,
            "b": 5,
            "operation": "multiply",
        }
    )
    assert result == 50