import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class PandasDemo:
    """판다스 기본 기능을 데모하는 클래스"""

    def __init__(self, data: Optional[Dict] = None):
        """
        PandasDemo 클래스 초기화

        Args:
            data (Optional[Dict]): 초기 데이터, 기본값은 None
        """
        if data is None:
            # 기본 샘플 데이터 생성
            self.df = pd.DataFrame({
                'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
                'age': [25, 30, 35, 28, 32],
                'city': ['Seoul', 'Busan', 'Seoul', 'Daegu', 'Seoul'],
                'salary': [50000, 60000, 70000, 55000, 65000]
            })
        else:
            self.df = pd.DataFrame(data)
    
    def display_basic_info(self) -> None:
        """데이터프레임의 기본 정보를 출력합니다."""
        print("=== 데이터프레임 기본 정보 ===")
        print("데이터프레임 형태:", self.df.shape)
        print("\n데이터 타입:")
        print(self.df.dtypes)
        print("\n첫 5행:")
        print(self.df.head())
        print("\n통계 요약:")
        print(self.df.describe())
    
    def filter_data(self, column: str, value, condition: str = "equal") -> pd.DataFrame:
        """
        조건에 따라 데이터를 필터링합니다.
        
        Args:
            column (str): 필터링할 컬럼명
            value: 필터링 값
            condition (str): 조건 ('equal', 'greater', 'less'), 기본값은 'equal'
        
        Returns:
            pd.DataFrame: 필터링된 데이터프레임
        """
        if condition == "equal":
            return self.df[self.df[column] == value]
        elif condition == "greater":
            return self.df[self.df[column] > value]
        elif condition == "less":
            return self.df[self.df[column] < value]
        else:
            raise ValueError("condition은 'equal', 'greater', 'less' 중 하나여야 합니다.")
    
    def group_analysis(self, group_by: str, agg_column: str = "salary") -> pd.DataFrame:
        """
        그룹별 분석을 수행합니다.
        
        Args:
            group_by (str): 그룹화할 컬럼명
            agg_column (str): 집계할 컬럼명, 기본값은 'salary'
        
        Returns:
            pd.DataFrame: 그룹별 집계 결과
        """
        return self.df.groupby(group_by)[agg_column].agg(['mean', 'sum', 'count'])
    
    def add_new_column(self, column_name: str, values: List) -> None:
        """
        새로운 컬럼을 추가합니다.
        
        Args:
            column_name (str): 새 컬럼명
            values (List): 컬럼 값들
        """
        if len(values) != len(self.df):
            raise ValueError("values의 길이가 데이터프레임의 행 수와 일치해야 합니다.")
        self.df[column_name] = values
    
    def save_to_csv(self, filename: str = "demo_output.csv") -> None:
        """
        데이터프레임을 CSV 파일로 저장합니다.
        
        Args:
            filename (str): 저장할 파일명, 기본값은 'demo_output.csv'
        """
        self.df.to_csv(filename, index=False, encoding='utf-8')
        print(f"데이터가 {filename}에 저장되었습니다.")

def main() -> None:
    """메인 함수 - 프로그램의 진입점"""
    print("=== 판다스 데모 프로그램 시작 ===\n")
    
    # PandasDemo 인스턴스 생성
    demo = PandasDemo()
    
    # 기본 정보 출력
    demo.display_basic_info()
    
    # 데이터 필터링 테스트
    print("\n=== 데이터 필터링 테스트 ===")
    seoul_people = demo.filter_data('city', 'Seoul')
    print("서울 거주자:")
    print(seoul_people)
    
    high_salary = demo.filter_data('salary', 60000, 'greater')
    print("\n연봉 60000 초과자:")
    print(high_salary)
    
    # 그룹 분석 테스트
    print("\n=== 그룹 분석 테스트 ===")
    city_analysis = demo.group_analysis('city')
    print("도시별 연봉 분석:")
    print(city_analysis)
    
    # 새 컬럼 추가 테스트
    print("\n=== 새 컬럼 추가 테스트 ===")
    experience_years = [3, 5, 8, 4, 6]
    demo.add_new_column('experience', experience_years)
    print("경력 컬럼 추가 후:")
    print(demo.df)
    
    # CSV 저장 테스트
    print("\n=== CSV 저장 테스트 ===")
    demo.save_to_csv()
    
    print("\n=== 판다스 데모 프로그램 종료 ===")

if __name__ == "__main__":
    main()
