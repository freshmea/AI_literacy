class PyramidPrinter:
    """별표로 피라미드를 출력하는 클래스"""
    
    def __init__(self, height: int = 5) -> None:
        """
        PyramidPrinter 초기화
        
        Args:
            height: 피라미드의 높이 (기본값: 5)
        """
        self.height = height
    
    def set_height(self, height: int) -> None:
        """
        피라미드 높이를 설정합니다
        
        Args:
            height: 설정할 높이
        """
        self.height = height
    
    def print_pyramid(self) -> None:
        """피라미드를 터미널에 출력합니다"""
        for i in range(1, self.height + 1):
            # 공백 출력 (높이 - 현재 줄 번호)
            spaces = ' ' * (self.height - i)
            # 별표 출력 (현재 줄 번호 * 2 - 1개)
            stars = '*' * (2 * i - 1)
            print(spaces + stars)

def main() -> None:
    """메인 함수 - 프로그램의 진입점"""
    try:
        height = int(input("피라미드의 높이를 입력하세요: "))
        if height > 0:
            pyramid = PyramidPrinter(height)
            pyramid.print_pyramid()
        else:
            print("양수를 입력해주세요.")
    except ValueError:
        print("올바른 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()
