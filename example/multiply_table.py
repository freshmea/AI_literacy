from __future__ import annotations  # Python 3.7~3.10 호환용 (선택)
from typing import List, Tuple


class Gugudan:
    """구구단을 다양한 방식으로 출력/제어하기 위한 클래스"""

    def __init__(self, start_dan: int = 2, end_dan: int = 9, max_multiplier: int = 9) -> None:
        """
        구구단 설정을 위한 초기화 메소드.

        :param start_dan: 시작 단 (기본: 2단)
        :param end_dan: 마지막 단 (기본: 9단)
        :param max_multiplier: 곱해지는 수의 최대값 (기본: 9)
        """
        self.start_dan: int = start_dan
        self.end_dan: int = end_dan
        self.max_multiplier: int = max_multiplier

    def print_all(self) -> None:
        """인스턴스에 설정된 범위의 모든 구구단을 출력"""
        for dan in range(self.start_dan, self.end_dan + 1):
            self._print_one_dan(dan)
            print()

    def _print_one_dan(self, dan: int) -> None:
        """단일 단을 출력하는 내부 메소드(외부에 안 보여줘도 되는 보조 기능)"""
        print(f"=== {dan}단 ===")
        for i in range(1, self.max_multiplier + 1):
            print(f"{dan} x {i} = {dan * i}")

    def print_dan(self, dan: int) -> None:
        """특정 단만 출력 (인스턴스 설정과는 별개로 단 하나 지정)"""
        if dan < 1:
            print("단은 1 이상이어야 합니다.")
            return
        self._print_one_dan(dan)

    def get_table(self) -> List[List[Tuple[int, int, int]]]:
        """
        구구단 결과를 2차원 리스트 형태로 반환.
        => 나중에 파일 저장, GUI, 웹 등에서 재사용 가능.

        return 형식: [[(단, 곱하는수, 결과), ...], [...], ...]
        """
        table: List[List[Tuple[int, int, int]]] = []
        for dan in range(self.start_dan, self.end_dan + 1):
            row: List[Tuple[int, int, int]] = []
            for i in range(1, self.max_multiplier + 1):
                row.append((dan, i, dan * i))
            table.append(row)
        return table

    def update_range(self, start_dan: int | None = None,
                     end_dan: int | None = None,
                     max_multiplier: int | None = None) -> None:
        """
        인스턴스가 가진 구구단 범위를 동적으로 변경하는 메소드.
        None이 아닌 값만 업데이트.

        :param start_dan: 새 시작 단
        :param end_dan: 새 끝 단
        :param max_multiplier: 새 곱셈 최대값
        """
        if start_dan is not None:
            self.start_dan = start_dan
        if end_dan is not None:
            self.end_dan = end_dan
        if max_multiplier is not None:
            self.max_multiplier = max_multiplier


def main() -> None:
    """프로그램의 엔트리 포인트"""
    print("구구단 클래스를 이용해 구구단을 출력합니다.\n")

    # 기본 설정: 2단 ~ 9단, 1 ~ 9까지
    gugudan = Gugudan()

    # 1) 전체 출력
    gugudan.print_all()

    # 2) 특정 단만 출력 (예: 7단)
    print("=== 특정 단만 출력 (7단) ===")
    gugudan.print_dan(7)
    print()

    gugudan.print_dan(1)  # 1단 출력 예시 (유효성 검사 포함)

    # 3) 설정 변경: 3단 ~ 5단, 곱하는 수는 1 ~ 5까지만
    print("=== 범위 설정 변경: 3단 ~ 5단, 1~5 ===")
    gugudan.update_range(start_dan=3, end_dan=5, max_multiplier=5)
    gugudan.print_all()

    # 4) 데이터를 리스트로 받아서 다른 용도로 활용
    table = gugudan.get_table()
    print("=== get_table()로 받은 데이터 예시 (앞의 몇 개만 출력) ===")
    # 첫 번째 단의 앞 3개만 예시로 출력
    for dan, i, result in table[0][:3]:
        print(f"{dan} x {i} = {result}")


if __name__ == "__main__":
    main()
