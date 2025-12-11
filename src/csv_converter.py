import pandas as pd
import os
from pathlib import Path
from typing import Optional, List

class ExcelToCsvConverter:
    """Excel 파일을 CSV 파일로 변환하는 클래스"""
    
    def __init__(self, excel_file_path: str = "/home/aa/AI_literacy/data/reviewcontents.xlsx"):
        """
        ExcelToCsvConverter 클래스 초기화
        
        Args:
            excel_file_path (str): 변환할 Excel 파일 경로, 기본값은 '/home/aa/AI_literacy/data/reviewcontents.xlsx'
        """
        self.excel_file_path: str = excel_file_path
        self.df: Optional[pd.DataFrame] = None
        self.output_directory: str = os.path.dirname(os.path.abspath(excel_file_path))
        
    def check_file_exists(self) -> bool:
        """
        Excel 파일이 존재하는지 확인합니다.
        
        Returns:
            bool: 파일 존재 여부
        """
        return os.path.exists(self.excel_file_path)
    
    def load_excel_file(self, sheet_name: Optional[str] = None) -> bool:
        """
        Excel 파일을 로드합니다.
        
        Args:
            sheet_name (Optional[str]): 로드할 시트 이름, 기본값은 None (첫 번째 시트)
        
        Returns:
            bool: 로드 성공 여부
        """
        try:
            if not self.check_file_exists():
                print(f"오류: '{self.excel_file_path}' 파일을 찾을 수 없습니다.")
                return False
            
            print(f"Excel 파일 로드 중: {self.excel_file_path}")
            
            # 특정 시트를 지정하지 않으면 첫 번째 시트만 로드
            if sheet_name is None:
                # 첫 번째 시트 이름을 가져와서 명시적으로 로드
                sheet_names = self.get_sheet_names()
                if sheet_names:
                    first_sheet = sheet_names[0]
                    self.df = pd.read_excel(self.excel_file_path, sheet_name=first_sheet)
                else:
                    self.df = pd.read_excel(self.excel_file_path, sheet_name=0)
            else:
                self.df = pd.read_excel(self.excel_file_path, sheet_name=sheet_name)
            
            print(f"파일 로드 완료! 데이터 크기: {self.df.shape}")
            return True
            
        except Exception as e:
            print(f"Excel 파일 로드 중 오류 발생: {str(e)}")
            return False
    
    def get_sheet_names(self) -> List[str]:
        """
        Excel 파일의 시트 이름들을 가져옵니다.
        
        Returns:
            List[str]: 시트 이름 리스트
        """
        try:
            excel_file = pd.ExcelFile(self.excel_file_path)
            return excel_file.sheet_names
        except Exception as e:
            print(f"시트 정보를 가져오는 중 오류 발생: {str(e)}")
            return []
    
    def display_data_info(self) -> None:
        """로드된 데이터의 기본 정보를 출력합니다."""
        if self.df is None:
            print("데이터가 로드되지 않았습니다.")
            return
        
        print("\n=== 데이터 정보 ===")
        print(f"데이터 형태: {self.df.shape}")
        print(f"컬럼: {list(self.df.columns)}")
        print("\n첫 5행:")
        print(self.df.head())
    
    def convert_to_csv(self, output_filename: Optional[str] = None, encoding: str = 'utf-8') -> bool:
        """
        로드된 데이터를 CSV 파일로 저장합니다.
        
        Args:
            output_filename (Optional[str]): 출력 CSV 파일명, 기본값은 None (자동 생성)
            encoding (str): 파일 인코딩, 기본값은 'utf-8'
        
        Returns:
            bool: 변환 성공 여부
        """
        if self.df is None:
            print("변환할 데이터가 없습니다. 먼저 Excel 파일을 로드하세요.")
            return False
        
        try:
            # 출력 파일명 설정
            if output_filename is None:
                base_name = Path(self.excel_file_path).stem
                output_filename = f"{base_name}.csv"
            
            # 같은 디렉토리에 저장할 전체 경로 생성
            output_path = os.path.join(self.output_directory, output_filename)
            
            print(f"CSV 파일로 변환 중: {output_path}")
            self.df.to_csv(output_path, index=False, encoding=encoding)
            print(f"변환 완료! 파일이 저장되었습니다: {output_path}")
            return True
            
        except Exception as e:
            print(f"CSV 변환 중 오류 발생: {str(e)}")
            return False
    
    def convert_all_sheets_to_csv(self, encoding: str = 'utf-8') -> bool:
        """
        Excel 파일의 모든 시트를 각각 별도의 CSV 파일로 변환합니다.
        
        Args:
            encoding (str): 파일 인코딩, 기본값은 'utf-8'
        
        Returns:
            bool: 모든 변환 성공 여부
        """
        sheet_names = self.get_sheet_names()
        if not sheet_names:
            return False
        
        success_count = 0
        base_name = Path(self.excel_file_path).stem
        
        for sheet_name in sheet_names:
            print(f"\n시트 '{sheet_name}' 변환 중...")
            if self.load_excel_file(sheet_name):
                output_filename = f"{base_name}_{sheet_name}.csv"
                if self.convert_to_csv(output_filename, encoding):
                    success_count += 1
        
        print(f"\n총 {success_count}/{len(sheet_names)}개 시트 변환 완료")
        return success_count == len(sheet_names)

def main() -> None:
    """메인 함수 - 프로그램의 진입점"""
    print("=== Excel to CSV 변환기 시작 ===\n")
    
    # ExcelToCsvConverter 인스턴스 생성
    converter = ExcelToCsvConverter("/home/aa/AI_literacy/data/reviewcontents.xlsx")
    
    # 파일 존재 여부 확인
    if not converter.check_file_exists():
        print("변환을 종료합니다.")
        return
    
    # 시트 정보 출력
    sheet_names = converter.get_sheet_names()
    if sheet_names:
        print(f"발견된 시트: {sheet_names}")
    
    # Excel 파일 로드 및 변환
    if converter.load_excel_file():
        # 데이터 정보 출력
        converter.display_data_info()
        
        # CSV로 변환
        if converter.convert_to_csv():
            print("\n변환이 성공적으로 완료되었습니다!")
        else:
            print("\n변환 중 오류가 발생했습니다.")
    else:
        print("Excel 파일 로드에 실패했습니다.")
    
    print("\n=== Excel to CSV 변환기 종료 ===")

if __name__ == "__main__":
    main()
