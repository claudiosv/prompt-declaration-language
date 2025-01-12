from pdl.pdl_interpreter import generate


def do_test(t, capsys):
    generate(t["file"], None, None, {}, None)
    captured = capsys.readouterr()
    output_string = captured.out
    output = output_string.split("\n")
    print(output)
    assert set(output) == set(t["errors"])


line = {
    "file": "tests/data/line/hello.pdl",
    "errors": [
        "",
        "tests/data/line/hello.pdl:0 - Missing required field: return",
        "tests/data/line/hello.pdl:0 - Missing required field: function",
        "tests/data/line/hello.pdl:2 - Field not allowed: documents",
    ],
}


def test_line(capsys):
    do_test(line, capsys)


line1 = {
    "file": "tests/data/line/hello1.pdl",
    "errors": [
        "",
        "tests/data/line/hello1.pdl:5 - Missing required field: num_iterations",
        "tests/data/line/hello1.pdl:7 - Field not allowed: num_iterationss",
    ],
}


def test_line1(capsys):
    do_test(line1, capsys)


line3 = {
    "file": "tests/data/line/hello3.pdl",
    "errors": [
        "",
        "Hello, World!",
        "tests/data/line/hello3.pdl:6 - Type errors during spec checking",
        "tests/data/line/hello3.pdl:6 -  World! should be of type <class 'int'>",
    ],
}


def test_line3(capsys):
    do_test(line3, capsys)


line4 = {
    "file": "tests/data/line/hello4.pdl",
    "errors": [
        "",
        "tests/data/line/hello4.pdl:5 - Missing required field: repeat",
        "tests/data/line/hello4.pdl:5 - Field not allowed: repeats",
    ],
}


def test_line4(capsys):
    do_test(line4, capsys)


line7 = {
    "file": "tests/data/line/hello7.pdl",
    "errors": [
        "",
        "tests/data/line/hello7.pdl:4 - Missing required field: lan",
        "tests/data/line/hello7.pdl:4 - Field not allowed: lans",
    ],
}


def test_line7(capsys):
    do_test(line7, capsys)


line8 = {
    "file": "tests/data/line/hello8.pdl",
    "errors": [
        "",
        "tests/data/line/hello8.pdl:4 - Missing required field: code",
        "tests/data/line/hello8.pdl:5 - Field not allowed: codea",
    ],
}


def test_line8(capsys):
    do_test(line8, capsys)


line9 = {
    "file": "tests/data/line/hello9.pdl",
    "errors": [
        "",
        "hello",
        "tests/data/line/hello9.pdl:3 - Type errors during spec checking",
        "tests/data/line/hello9.pdl:3 - hello should be of type <class 'int'>",
    ],
}


def test_line9(capsys):
    do_test(line9, capsys)


line10 = {
    "file": "tests/data/line/hello10.pdl",
    "errors": [
        "",
        "tests/data/line/hello10.pdl:7 - QUESTION should be an object",
    ],
}


def test_line10(capsys):
    do_test(line10, capsys)


line11 = {
    "file": "tests/data/line/hello11.pdl",
    "errors": [
        "",
        "tests/data/line/hello11.pdl:7 - Field not allowed: defss",
    ],
}


def test_line11(capsys):
    do_test(line11, capsys)


line12 = {
    "file": "tests/data/line/hello12.pdl",
    "errors": [
        "",
        "Hello! How are you?",
        "tests/data/line/hello12.pdl:9 - Type errors during spec checking",
        "tests/data/line/hello12.pdl:9 - How are you? should be of type <class 'bool'>",
    ],
}


def test_line12(capsys):
    do_test(line12, capsys)


line13 = {
    "file": "tests/data/line/hello13.pdl",
    "errors": [
        "",
        "0",
        "1",
        "tests/data/line/hello13.pdl:9 - Type errors during spec checking",
        "tests/data/line/hello13.pdl:9 - 1 should be of type <class 'str'>",
    ],
}


def test_line13(capsys):
    do_test(line13, capsys)


line14 = {
    "file": "tests/data/line/hello14.pdl",
    "errors": [
        "",
        "Hello, World!Bonjour le monde!",
        "tests/data/line/hello14.pdl:24 - Type errors in result of function call to translate",
        "tests/data/line/hello14.pdl:16 - Bonjour le monde! should be of type <class 'int'>",
    ],
}


def test_line14(capsys):
    do_test(line14, capsys)


line15 = {
    "file": "tests/data/line/hello15.pdl",
    "errors": [
        "",
        "Hello World!",
        "tests/data/line/hello15.pdl:6 - Variable is undefined: boolean",
        "tests/data/line/hello15.pdl:7 - 'something' is undefined",
        "{{ something }}",
    ],
}


def test_line15(capsys):
    do_test(line15, capsys)


line16 = {
    "file": "tests/data/line/hello16.pdl",
    "errors": [
        "",
        '{"bob": 20, "carol": 30}',
        "tests/data/line/hello16.pdl:8 - Type errors during spec checking",
        "tests/data/line/hello16.pdl:8 - 30 should be of type <class 'str'>",
    ],
}


def test_line16(capsys):
    do_test(line16, capsys)


line17 = {
    "file": "tests/data/line/hello17.pdl",
    "errors": [
        "",
        "tests/data/line/hello17.pdl:3 - Type errors during spec checking",
        "tests/data/line/hello17.pdl:3 - hello should be of type <class 'int'>",
    ],
}


def test_line17(capsys):
    do_test(line17, capsys)


line18 = {
    "file": "tests/data/line/hello18.pdl",
    "errors": ["", "0", "1", "tests/data/line/hello18.pdl:13 - 'J' is undefined"],
}


def test_line18(capsys):
    do_test(line18, capsys)


line19 = {
    "file": "tests/data/line/hello19.pdl",
    "errors": [
        "",
        "Hello,",
        "tests/data/line/hello19.pdl:6 - 'models' is undefined",
        "tests/data/line/hello19.pdl:6 - Type errors during spec checking",
        "tests/data/line/hello19.pdl:6 - None should be of type <class 'int'>",
    ],
}


def test_line19(capsys):
    do_test(line19, capsys)


line20 = {
    "file": "tests/data/line/hello20.pdl",
    "errors": [
        "",
        "tests/data/line/hello20.pdl:3 - 'NAME' is undefined",
        "Who is{{ NAME }}?",
    ],
}


def test_line20(capsys):
    do_test(line20, capsys)


line21 = {
    "file": "tests/data/line/hello21.pdl",
    "errors": ["", "tests/data/line/hello21.pdl:3 - 'QUESTION' is undefined"],
}


def test_line21(capsys):
    do_test(line21, capsys)


line22 = {
    "file": "tests/data/line/hello22.pdl",
    "errors": [
        "",
        "tests/data/line/hello22.pdl:4 - 'I' is undefined",
        "{{ I }}",
    ],
}


def test_line22(capsys):
    do_test(line22, capsys)


line23 = {
    "file": "tests/data/line/hello23.pdl",
    "errors": [
        "",
        "tests/data/line/hello23.pdl:5 - 'I' is undefined",
        "{{ I }}",
    ],
}


def test_line23(capsys):
    do_test(line23, capsys)


line24 = {
    "file": "tests/data/line/hello24.pdl",
    "errors": [
        "",
        "Hello, World!",
        "tests/data/line/hello24.pdl:24 - 'GEN1' is undefined",
        "tests/data/line/hello24.pdl:25 - 'GEN2' is undefined",
        "tests/data/line/hello24.pdl:23 - Type errors during function call to translate",
        "tests/data/line/hello24.pdl:21 - None should be of type <class 'str'>",
        "tests/data/line/hello24.pdl:25 - None should be of type <class 'str'>",
        "tests/data/line/hello24.pdl:21 - Type errors during spec checking",
        "tests/data/line/hello24.pdl:24 - None should be of type <class 'str'>",
    ],
}


def test_line24(capsys):
    do_test(line24, capsys)


line25 = {
    "file": "tests/data/line/hello25.pdl",
    "errors": [
        "",
        "Hello, World!",
        "tests/data/line/hello25.pdl:15 - 'sentence1' is undefined",
        "{{ translateText(sentence2) }}",
    ],
}

# Leaving this out for now, since we can't mock the model result
# def test_line25(capsys):
#    do_test(line25, capsys)


line26 = {
    "file": "tests/data/line/hello26.pdl",
    "errors": [
        "",
        "tests/data/line/hello26.pdl:13 - 'questions2' is undefined",
        "tests/data/line/hello26.pdl:13 - Values inside the For block must be lists",
        "tests/data/line/hello26.pdl:12 - Lists inside the For block must be of the same length",
        "Here is the code:",
        "```json",
        "{",
        '  "bob": "20",',
        '  "carol": "30"',
        "}",
    ],
}


def test_line26(capsys):
    do_test(line26, capsys)


line28 = {
    "file": "tests/data/line/hello28.pdl",
    "errors": [
        "Hello! ",
        "tests/data/line/hello28.pdl:9 - 'QUESTION1' is undefined",
        "{{ QUESTION1 }}",
        "",
    ],
}


def test_line28(capsys):
    do_test(line28, capsys)


line29 = {
    "file": "tests/data/line/hello29.pdl",
    "errors": [
        "Hello! ",
        "tests/data/line/hello29.pdl:10 - 'QUESTION1' is undefined",
        "tests/data/line/hello29.pdl:11 - 'QUESTION2' is undefined",
        "tests/data/line/hello29.pdl:13 - 'QUESTION3' is undefined",
        "tests/data/line/hello29.pdl:15 - 'QUESTION4' is undefined",
        "null",
        "",
    ],
}


def test_line29(capsys):
    do_test(line29, capsys)


line30 = {
    "file": "tests/data/line/hello30.pdl",
    "errors": [
        "",
        "tests/data/line/hello30.pdl:7 - Values inside the For block must be lists",
        "[]",
    ],
}


def test_line30(capsys):
    do_test(line30, capsys)
