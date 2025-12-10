class RectanglePrinter:
    """문자를 사용하여 사각형을 출력하는 클래스"""
    
    def __init__(self, width: int = 10, height: int = 5, char: str = '*') -> None:
        """
        RectanglePrinter 초기화
        
        Args:
            width: 사각형의 너비 (기본값: 10)
            height: 사각형의 높이 (기본값: 5)
            char: 사각형을 그릴 문자 (기본값: '*')
        """
        self.width = width
        self.height = height
        self.char = char
    
    def set_dimensions(self, width: int, height: int) -> None:
        """
        사각형의 크기를 설정합니다
        
        Args:
            width: 설정할 너비
            height: 설정할 높이
        """
        self.width = width
        self.height = height
    
    def set_char(self, char: str) -> None:
        """
        사각형을 그릴 문자를 설정합니다
        
        Args:
            char: 설정할 문자
        """
        self.char = char
    
    def print_rectangle(self, filled: bool = True) -> None:
        """
        사각형을 터미널에 출력합니다
        
        Args:
            filled: True면 채워진 사각형, False면 테두리만 출력 (기본값: True)
        """
        for i in range(self.height):
            if filled:
                print(self.char * self.width)
            else:
                if i == 0 or i == self.height - 1:
                    # 첫 번째와 마지막 줄은 완전히 채움
                    print(self.char * self.width)
                else:
                    # 가운데 줄은 양쪽 끝만 문자로 채움
                    print(self.char + ' ' * (self.width - 2) + self.char)

def main() -> None:
    """메인 함수 - 프로그램의 진입점"""
    try:
        width = int(input("사각형의 너비를 입력하세요: "))
        height = int(input("사각형의 높이를 입력하세요: "))
        char = input("사용할 문자를 입력하세요 (기본값: *): ") or '*'
        filled = input("채워진 사각형을 원하시나요? (y/n, 기본값: y): ").lower() != 'n'
        
        if width > 0 and height > 0:
            rectangle = RectanglePrinter(width, height, char)
            rectangle.print_rectangle(filled)
        else:
            print("너비와 높이는 양수여야 합니다.")
    except ValueError:
        print("올바른 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()
