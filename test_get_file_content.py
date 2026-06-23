from functions.get_file_content import get_file_content


def test() -> None:
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    result = get_file_content("calculator", "main.py")
    print(f"1. {result}")

    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"2. {result}")

    result = get_file_content("calculator", "/bin/cat")
    print(f"3. {result}")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"4. {result}")

if __name__ == "__main__":
    test()