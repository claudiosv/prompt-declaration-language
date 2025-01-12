from pdl.pdl_ast import Program
from pdl.pdl_interpreter import (
    InterpreterState,
    contains_error,
    empty_scope,
    process_prog,
)

var_data = {
    "description": "Hello world with variable use",
    "document": [
        "Hello,",
        {
            "def": "NAME",
            "document": [
                {
                    "model": "watsonx/ibm/granite-34b-code-instruct",
                    "parameters": {
                        "decoding_method": "greedy",
                        "stop_sequences": ["!"],
                        "include_stop_sequence": False,
                        "mock_response": " World",
                    },
                }
            ],
        },
        "!\n",
        "Tell me about",
        {"get": "NAME"},
        "?\n",
    ],
}


def test_var():
    state = InterpreterState()
    data = Program.model_validate(var_data)
    document, _, _, _ = process_prog(state, empty_scope, data)
    assert document == "Hello, World!\nTell me about World?\n"


var_shared_scope_data = {
    "description": "Hello world with variable use",
    "document": [
        "Hello,",
        {
            "def": "NAME",
            "document": [
                {
                    "model": "watsonx/ibm/granite-34b-code-instruct",
                    "parameters": {
                        "decoding_method": "greedy",
                        "stop_sequences": ["!"],
                        "include_stop_sequence": False,
                        "mock_response": " World",
                    },
                }
            ],
        },
        {
            "def": "I",
            "lan": "python",
            "code": "result = NAME[::-1] + '!\\n'",
            "contribute": [],
        },
        {"get": "I"},
    ],
}


def test_code_shared_scope():
    state = InterpreterState()
    data = Program.model_validate(var_shared_scope_data)
    document, _, _, _ = process_prog(state, empty_scope, data)
    assert document == "Hello, WorlddlroW !\n"


var_shared_scope_mutate_data = {
    "description": "Hello world with variable use",
    "document": [
        "Hello, ",
        {
            "def": "NAME",
            "document": "foo",
            "contribute": [],
        },
        {
            "def": "I",
            "lan": "python",
            "code": {"document": ["NAME = NAME[::-1]\n", "result = NAME"]},
            "contribute": [],
        },
        {"get": "NAME"},
        {"get": "I"},
    ],
}


def test_code_shared_scope_no_mutate():
    """
    Python should be able to access variables in the PDL document scope,
    but any modifications should _not_ affect the document scope.
    """

    state = InterpreterState()
    data = Program.model_validate(var_shared_scope_mutate_data)
    document, _, _, _ = process_prog(state, empty_scope, data)
    assert document == "Hello, foooof"


code_var_data = {
    "description": "simple python",
    "document": [
        {
            "def": "I",
            "lan": "python",
            "code": ["result = 0"],
        },
    ],
}


def test_code_var():
    state = InterpreterState()
    data = Program.model_validate(code_var_data)
    document, _, scope, _ = process_prog(state, empty_scope, data)
    assert scope == {"context": [{"role": None, "content": document}], "I": 0}
    assert document == "0"


missing_var = {
    "description": "simple python",
    "document": [{"get": "somevar"}],
}


def test_missing_var():
    state = InterpreterState()
    data = Program.model_validate(missing_var)
    _, _, _, trace = process_prog(state, empty_scope, data)
    assert contains_error(trace)


missing_call = {
    "description": "simple python",
    "document": [{"call": "somevar"}],
}


def test_missing_call():
    state = InterpreterState()
    data = Program.model_validate(missing_call)
    _, _, _, trace = process_prog(state, empty_scope, data)
    assert contains_error(trace)
