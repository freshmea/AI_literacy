#!/usr/bin/env python3
"""
심장 마비 데이터: 선형 회귀 분석 (Feature -> Target)
기본값: age(나이) -> thalachh(최대 심박수)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
import sys
import matplotlib.font_manager as fm

# 한글 폰트 설정
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

class HeartRegressionAnalyzer:
    def __init__(self, data_path, result_dir, feature_col='age', target_col='thalachh'):
        """
        초기화 함수
        
        Args:
            data_path (str): 데이터 파일 경로
            result_dir (str): 결과 저장 디렉토리
            feature_col (str): 독립 변수 컬럼명 (기본값: 'age')
            target_col (str): 종속 변수 컬럼명 (기본값: 'thalachh')
        """
        self.data_path = data_path
        self.result_dir = result_dir
        self.feature_col = feature_col
        self.target_col = target_col
        self.df = None
        self.model = None
        self.results = None
        
        os.makedirs(self.result_dir, exist_ok=True)
        setup_korean_font()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"데이터 로드 완료: {len(self.df)}행")
            
            # 컬럼 존재 여부 확인
            if self.feature_col not in self.df.columns:
                raise ValueError(f"Feature column '{self.feature_col}' not found in data.")
            if self.target_col not in self.df.columns:
                raise ValueError(f"Target column '{self.target_col}' not found in data.")
                
        except Exception as e:
            print(f"데이터 로드 실패: {e}")
            sys.exit(1)

    def perform_regression(self):
        # X: feature_col (Feature), y: target_col (Target)
        X = self.df[[self.feature_col]]
        y = self.df[self.target_col]

        # 선형 회귀 모델 학습
        self.model = LinearRegression()
        self.model.fit(X, y)

        # 예측
        y_pred = self.model.predict(X)

        # 결과 저장
        self.results = self.df[[self.feature_col, self.target_col]].copy()
        self.results[f'predicted_{self.target_col}'] = y_pred
        self.results['error'] = self.results[self.target_col] - self.results[f'predicted_{self.target_col}']

        # 계수 및 절편
        slope = self.model.coef_[0]
        intercept = self.model.intercept_
        
        return slope, intercept

    def calculate_metrics(self):
        y_true = self.results[self.target_col]
        y_pred = self.results[f'predicted_{self.target_col}']

        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        metrics = {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2 Score': r2
        }
        return metrics

    def visualize(self, slope, intercept):
        plt.figure(figsize=(10, 6))
        
        # 산점도 (실제 데이터)
        sns.scatterplot(data=self.results, x=self.feature_col, y=self.target_col, alpha=0.6, label='Actual Data')
        
        # 회귀선
        # X 범위에 따른 Y값 계산
        x_range = np.linspace(self.results[self.feature_col].min(), self.results[self.feature_col].max(), 100)
        y_range = slope * x_range + intercept
        plt.plot(x_range, y_range, color='red', linewidth=2, label=f'Regression Line (y={slope:.4f}x + {intercept:.4f})')

        plt.title(f'Relationship between {self.feature_col} and {self.target_col}', fontsize=14)
        plt.xlabel(self.feature_col, fontsize=12)
        plt.ylabel(self.target_col, fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        output_path = os.path.join(self.result_dir, f'heart_{self.target_col}_{self.feature_col}_regression.png')
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"시각화 저장 완료: {output_path}")

    def save_results(self, metrics, slope, intercept):
        # 결과 CSV 저장
        csv_path = os.path.join(self.result_dir, f'heart_{self.target_col}_prediction_comparison.csv')
        self.results.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"예측 결과 CSV 저장 완료: {csv_path}")

        # 메트릭 및 모델 정보 텍스트 저장
        txt_path = os.path.join(self.result_dir, f'heart_{self.target_col}_{self.feature_col}_regression_metrics.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"=== 선형 회귀 분석 결과 ({self.feature_col} -> {self.target_col}) ===\n\n")
            f.write(f"모델 수식: {self.target_col} = {slope:.4f} * {self.feature_col} + {intercept:.4f}\n")
            f.write(f"계수 (Coefficient): {slope:.4f}\n")
            f.write(f"절편 (Intercept): {intercept:.4f}\n\n")
            f.write("=== 성능 지표 ===\n")
            for k, v in metrics.items():
                f.write(f"{k}: {v:.4f}\n")
        print(f"분석 결과 텍스트 저장 완료: {txt_path}")

    def run(self):
        self.load_data()
        slope, intercept = self.perform_regression()
        metrics = self.calculate_metrics()
        self.visualize(slope, intercept)
        self.save_results(metrics, slope, intercept)
        
        print("\n=== 분석 요약 ===")
        print(f"Feature: {self.feature_col}")
        print(f"Target: {self.target_col}")
        print(f"계수: {slope:.4f}")
        print(f"절편: {intercept:.4f}")
        print(f"R2 Score: {metrics['R2 Score']:.4f}")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'heart.csv')
    result_dir = os.path.join(os.path.dirname(current_dir), 'result')
    
    # 기본값 사용 (age -> thalachh)
    # 다른 컬럼을 분석하려면: HeartRegressionAnalyzer(data_path, result_dir, feature_col='chol', target_col='thalachh')
    analyzer = HeartRegressionAnalyzer(data_path, result_dir)
    analyzer.run()

if __name__ == "__main__":
    main()
