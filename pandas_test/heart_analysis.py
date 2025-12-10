#!/usr/bin/env python3
"""
심장 마비 데이터 분석 및 시각화 클래스
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# 한글 폰트 설정 (이전 코드 재사용)
import matplotlib.font_manager as fm

def setup_korean_font():
    """한글 폰트 설정"""
    korean_fonts = [
        'NanumGothic', 'NanumBarunGothic', 'NanumMyeongjo',
        'Malgun Gothic', 'AppleGothic', 'Batang', 'Dotum',
        'UnDotum', 'Gulim', 'UnGulim', 'NotoSansCJK',
        'Noto Sans CJK KR', 'Source Han Sans'
    ]
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in korean_fonts:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            plt.rcParams['axes.unicode_minus'] = False
            return font
    
    # 시스템 폰트 경로에서 직접 찾기 (Linux)
    import subprocess
    try:
        result = subprocess.run(['fc-list', ':lang=ko'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout:
            if 'NanumGothic' in result.stdout:
                plt.rcParams['font.family'] = 'NanumGothic'
                plt.rcParams['axes.unicode_minus'] = False
                return 'NanumGothic'
    except:
        pass
    
    return 'DejaVu Sans'

class HeartDiseaseAnalyzer:
    """심장 마비 데이터 분석기"""

    def __init__(self, data_path: str, result_dir: str = "../result"):
        """
        초기화 함수
        
        Args:
            data_path (str): 데이터 파일 경로
            result_dir (str): 결과 저장 디렉토리
        """
        self.data_path = data_path
        self.result_dir = result_dir
        self.df = None
        self.column_meanings = {
            'age': '나이 (Age)',
            'sex': '성별 (Sex) (1=남성, 0=여성)',
            'cp': '흉통 유형 (Chest Pain Type) (0-3)',
            'trtbps': '안정 시 혈압 (Resting Blood Pressure) (mm Hg)',
            'chol': '콜레스테롤 (Cholesterol) (mg/dl)',
            'fbs': '공복 혈당 (Fasting Blood Sugar) > 120 mg/dl (1=True, 0=False)',
            'restecg': '안정 시 심전도 결과 (Resting ECG)',
            'thalachh': '최대 심박수 (Max Heart Rate Achieved)',
            'exng': '운동 유발 협심증 (Exercise Induced Angina) (1=Yes, 0=No)',
            'oldpeak': 'ST 우울 (ST Depression Induced by Exercise)',
            'slp': 'ST 분절 기울기 (Slope of the Peak Exercise ST Segment)',
            'caa': '주요 혈관 수 (Number of Major Vessels) (0-3)',
            'thall': '탈륨 스트레스 테스트 결과 (Thallium Stress Test)',
            'output': '심장 마비 발생 여부 (Target) (1=발생 가능성 높음, 0=낮음)'
        }
        
        # 결과 디렉토리 생성
        os.makedirs(self.result_dir, exist_ok=True)
        
        # 폰트 설정
        setup_korean_font()

    def load_data(self) -> None:
        """데이터 로드"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"데이터 로드 완료: {len(self.df)}행, {len(self.df.columns)}열")
        except Exception as e:
            print(f"데이터 로드 실패: {e}")
            sys.exit(1)

    def analyze_correlation(self) -> pd.DataFrame:
        """상관관계 분석"""
        if self.df is None:
            raise ValueError("데이터가 로드되지 않았습니다.")
        
        correlation_matrix = self.df.corr()
        return correlation_matrix

    def save_column_meanings(self) -> None:
        """컬럼 의미를 텍스트 파일로 저장"""
        output_path = os.path.join(self.result_dir, 'heart_column_meanings.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=== 심장 마비 데이터 컬럼 의미 분석 ===\n\n")
            for col, meaning in self.column_meanings.items():
                f.write(f"{col}: {meaning}\n")
        print(f"컬럼 의미 저장 완료: {output_path}")

    def save_correlation_table(self, corr_matrix: pd.DataFrame) -> None:
        """상관관계 표를 CSV로 저장"""
        output_path = os.path.join(self.result_dir, 'heart_correlation_table.csv')
        corr_matrix.to_csv(output_path, encoding='utf-8-sig')
        print(f"상관관계 표 저장 완료: {output_path}")

    def plot_heatmap(self, corr_matrix: pd.DataFrame) -> None:
        """상관관계 히트맵 시각화 및 저장"""
        plt.figure(figsize=(14, 12))
        
        # 마스크 생성 (상삼각행렬 가리기 위함, 선택사항이지만 가독성에 좋음)
        # mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, 
                    annot=True, 
                    fmt='.2f', 
                    cmap='coolwarm', 
                    center=0,
                    square=True,
                    linewidths=.5,
                    cbar_kws={"shrink": .5})
        
        plt.title('Heart Disease Feature Correlation Matrix', fontsize=20)
        plt.tight_layout()
        
        output_path = os.path.join(self.result_dir, 'heart_heatmap.png')
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"히트맵 저장 완료: {output_path}")

    def run(self) -> None:
        """전체 분석 실행"""
        self.load_data()
        self.save_column_meanings()
        
        corr_matrix = self.analyze_correlation()
        self.save_correlation_table(corr_matrix)
        self.plot_heatmap(corr_matrix)
        print("모든 분석이 완료되었습니다.")

def main():
    # 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'heart.csv')
    result_dir = os.path.join(os.path.dirname(current_dir), 'result')
    
    analyzer = HeartDiseaseAnalyzer(data_path, result_dir)
    analyzer.run()

if __name__ == "__main__":
    main()
