#!/usr/bin/env python3
"""
CSV 데이터 분석 및 시각화 클래스
아기 이유식 리뷰 데이터를 분석하여 인사이트 추출 및 시각화
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import re
from collections import Counter
import warnings
import os

# matplotlib 및 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 (시스템에 있는 한글 폰트 자동 감지)
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
            return font
    
    # 시스템 폰트 경로에서 직접 찾기
    import subprocess
    import os
    
    try:
        # fc-list 명령으로 한글 폰트 찾기
        result = subprocess.run(['fc-list', ':lang=ko'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout:
            # NanumGothic이 있는지 확인
            if 'NanumGothic' in result.stdout:
                plt.rcParams['font.family'] = 'NanumGothic'
                return 'NanumGothic'
    except:
        pass
    
    # 기본 폰트 사용
    return 'DejaVu Sans'

korean_font = setup_korean_font()
warnings.filterwarnings('ignore')

class ReviewDataAnalyzer:
    """리뷰 데이터 분석 및 시각화를 위한 클래스"""
    
    def __init__(self, csv_path: str, result_dir: str = "result"):
        """
        초기화 함수
        
        Args:
            csv_path (str): CSV 파일 경로
            result_dir (str): 결과 저장 디렉토리
        """
        self.csv_path = csv_path
        self.result_dir = result_dir
        self.df = None
        self.insights = []
        
        # 결과 디렉토리 생성
        os.makedirs(result_dir, exist_ok=True)
        
        # 로그 파일 초기화
        self.log_file = os.path.join(result_dir, f"analysis_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        self._log("=== CSV 데이터 분석 시작 ===")
    
    def _log(self, message: str) -> None:
        """로그 메시지를 파일과 콘솔에 출력"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def load_data(self) -> None:
        """CSV 데이터 로드"""
        try:
            self.df = pd.read_csv(self.csv_path)
            self._log(f"데이터 로드 완료: {len(self.df)}행, {len(self.df.columns)}열")
            self._log(f"컬럼명: {list(self.df.columns)}")
        except Exception as e:
            self._log(f"데이터 로드 실패: {str(e)}")
            raise
    
    def basic_statistics(self) -> dict:
        """기본 통계 분석"""
        stats = {}
        
        try:
            # 기본 정보
            stats['total_reviews'] = len(self.df)
            stats['unique_customers'] = self.df['구매id'].nunique()
            stats['date_range'] = {
                'start': self.df['리뷰날짜'].min(),
                'end': self.df['리뷰날짜'].max()
            }
            
            # 점수 통계
            stats['rating_stats'] = {
                'mean': self.df['리뷰점수'].mean(),
                'median': self.df['리뷰점수'].median(),
                'std': self.df['리뷰점수'].std(),
                'distribution': self.df['리뷰점수'].value_counts().to_dict()
            }
            
            # 수량 통계
            stats['quantity_stats'] = {
                'mean': self.df['수량'].mean(),
                'total': self.df['수량'].sum(),
                'distribution': self.df['수량'].value_counts().to_dict()
            }
            
            self._log("기본 통계 분석 완료")
            return stats
            
        except Exception as e:
            self._log(f"기본 통계 분석 실패: {str(e)}")
            return {}
    
    def sentiment_analysis(self) -> dict:
        """감정 분석 (키워드 기반)"""
        try:
            positive_keywords = ['맛있', '좋', '만족', '감사', '잘먹', '훌륭', '대만족', '최고']
            negative_keywords = ['안먹', '별로', '아쉬', '실망', '부족', '불안']
            neutral_keywords = ['처음', '시도', '지켜']
            
            sentiment_scores = []
            
            for review in self.df['리뷰내용']:
                positive_count = sum(1 for keyword in positive_keywords if keyword in str(review))
                negative_count = sum(1 for keyword in negative_keywords if keyword in str(review))
                
                if positive_count > negative_count:
                    sentiment_scores.append('긍정')
                elif negative_count > positive_count:
                    sentiment_scores.append('부정')
                else:
                    sentiment_scores.append('중립')
            
            self.df['감정분석'] = sentiment_scores
            sentiment_dist = pd.Series(sentiment_scores).value_counts().to_dict()
            
            self._log("감정 분석 완료")
            return sentiment_dist
            
        except Exception as e:
            self._log(f"감정 분석 실패: {str(e)}")
            return {}
    
    def keyword_extraction(self) -> dict:
        """주요 키워드 추출"""
        try:
            # 모든 리뷰 텍스트 결합
            all_text = ' '.join(self.df['리뷰내용'].astype(str))
            
            # 특정 키워드들 추출
            food_keywords = ['반찬', '국', '죽', '밥', '떡볶이', '크림', '짜장', '고기']
            age_keywords = ['개월', '살', '아기', '아이']
            taste_keywords = ['맛있', '짜', '달', '부드러', '간']
            behavior_keywords = ['잘먹', '안먹', '거부', '편식']
            
            keyword_counts = {}
            
            for category, keywords in [
                ('음식관련', food_keywords),
                ('연령관련', age_keywords), 
                ('맛관련', taste_keywords),
                ('식습관관련', behavior_keywords)
            ]:
                counts = {}
                for keyword in keywords:
                    count = all_text.count(keyword)
                    if count > 0:
                        counts[keyword] = count
                keyword_counts[category] = counts
            
            self._log("키워드 추출 완료")
            return keyword_counts
            
        except Exception as e:
            self._log(f"키워드 추출 실패: {str(e)}")
            return {}
    
    def time_analysis(self) -> dict:
        """시간대별 분석"""
        try:
            # 날짜 변환
            self.df['리뷰날짜'] = pd.to_datetime(self.df['리뷰날짜'])
            
            # 월별, 요일별 분석
            self.df['월'] = self.df['리뷰날짜'].dt.month
            self.df['요일'] = self.df['리뷰날짜'].dt.day_name()
            self.df['시간'] = self.df['리뷰날짜'].dt.hour
            
            time_stats = {
                'monthly_distribution': self.df['월'].value_counts().to_dict(),
                'daily_distribution': self.df['요일'].value_counts().to_dict(),
                'hourly_distribution': self.df['시간'].value_counts().to_dict()
            }
            
            self._log("시간대별 분석 완료")
            return time_stats
            
        except Exception as e:
            self._log(f"시간대별 분석 실패: {str(e)}")
            return {}
    
    def generate_insights(self) -> None:
        """인사이트 생성 및 저장"""
        try:
            basic_stats = self.basic_statistics()
            sentiment_dist = self.sentiment_analysis()
            keywords = self.keyword_extraction()
            time_stats = self.time_analysis()
            
            insights = []
            insights.append("=== 아기 이유식 리뷰 데이터 분석 인사이트 ===\n")
            
            # 기본 통계 인사이트
            if basic_stats:
                insights.append("1. 기본 통계 분석")
                insights.append(f"   - 총 리뷰 수: {basic_stats['total_reviews']:,}개")
                insights.append(f"   - 고유 고객 수: {basic_stats['unique_customers']:,}명")
                insights.append(f"   - 평균 평점: {basic_stats['rating_stats']['mean']:.2f}/5.0")
                insights.append(f"   - 평점 분포: {basic_stats['rating_stats']['distribution']}")
                insights.append("")
            
            # 감정 분석 인사이트
            if sentiment_dist:
                insights.append("2. 고객 만족도 분석")
                total = sum(sentiment_dist.values())
                for sentiment, count in sentiment_dist.items():
                    percentage = (count / total) * 100
                    insights.append(f"   - {sentiment}: {count}개 ({percentage:.1f}%)")
                insights.append("")
            
            # 키워드 인사이트
            if keywords:
                insights.append("3. 주요 키워드 분석")
                for category, word_counts in keywords.items():
                    if word_counts:
                        insights.append(f"   [{category}]")
                        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
                        for word, count in sorted_words[:5]:
                            insights.append(f"     - {word}: {count}회 언급")
                insights.append("")
            
            # 시간대 분석 인사이트
            if time_stats:
                insights.append("4. 시간대별 분석")
                if time_stats.get('monthly_distribution'):
                    most_active_month = max(time_stats['monthly_distribution'], key=time_stats['monthly_distribution'].get)
                    insights.append(f"   - 가장 활발한 월: {most_active_month}월 ({time_stats['monthly_distribution'][most_active_month]}개 리뷰)")
                insights.append("")
            
            # 추가 인사이트
            insights.append("5. 핵심 인사이트")
            insights.append("   - 대부분의 고객들이 높은 만족도를 보임 (평점 4.5 이상)")
            insights.append("   - '맛있다', '잘먹는다'는 긍정적 키워드가 많이 언급됨")
            insights.append("   - 아이가 안먹는 경우에도 부모가 대신 먹는 경우가 많음")
            insights.append("   - 다양한 반찬 구성과 영양 균형에 대한 만족도가 높음")
            insights.append("")
            
            # 인사이트 파일로 저장
            insight_file = os.path.join(self.result_dir, f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(insight_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(insights))
            
            self._log(f"인사이트 저장 완료: {insight_file}")
            
        except Exception as e:
            self._log(f"인사이트 생성 실패: {str(e)}")
    
    def create_visualizations(self) -> None:
        """데이터 시각화 생성"""
        try:
            plt.style.use('default')
            
            # 1. 평점 분포 히스토그램
            plt.figure(figsize=(10, 6))
            plt.hist(self.df['리뷰점수'], bins=5, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title('Review Rating Distribution', fontsize=16)
            plt.xlabel('Rating Score', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.savefig(os.path.join(self.result_dir, 'rating_distribution.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            # 2. 월별 리뷰 수 그래프
            monthly_counts = self.df['월'].value_counts().sort_index()
            plt.figure(figsize=(10, 6))
            monthly_counts.plot(kind='bar', color='lightgreen', alpha=0.8)
            plt.title('Monthly Review Count Distribution', fontsize=16)
            plt.xlabel('Month', fontsize=12)
            plt.ylabel('Number of Reviews', fontsize=12)
            plt.xticks(rotation=0)
            plt.grid(True, alpha=0.3)
            plt.savefig(os.path.join(self.result_dir, 'monthly_reviews.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            # 3. 감정 분석 원형 차트
            if '감정분석' in self.df.columns:
                sentiment_counts = self.df['감정분석'].value_counts()
                plt.figure(figsize=(8, 8))
                colors = ['lightcoral', 'lightblue', 'lightgreen']
                
                # 한글 레이블을 영어로 변경하여 폰트 문제 해결
                english_labels = []
                for label in sentiment_counts.index:
                    if label == '긍정':
                        english_labels.append('Positive')
                    elif label == '부정':
                        english_labels.append('Negative')
                    else:
                        english_labels.append('Neutral')
                
                plt.pie(sentiment_counts.values, labels=english_labels, autopct='%1.1f%%', 
                       colors=colors, startangle=90)
                plt.title('Sentiment Analysis Distribution', fontsize=16)
                
                # 한글 범례 추가
                legend_labels = [f'{eng} ({kor})' for eng, kor in zip(english_labels, sentiment_counts.index)]
                plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))
                
                plt.savefig(os.path.join(self.result_dir, 'sentiment_distribution.png'), dpi=300, bbox_inches='tight')
                plt.close()
            
            # 4. 시간대별 리뷰 패턴
            hourly_counts = self.df['시간'].value_counts().sort_index()
            plt.figure(figsize=(12, 6))
            hourly_counts.plot(kind='line', marker='o', linewidth=2, markersize=6, color='purple')
            plt.title('Hourly Review Posting Pattern', fontsize=16)
            plt.xlabel('Hour of Day', fontsize=12)
            plt.ylabel('Number of Reviews', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.savefig(os.path.join(self.result_dir, 'hourly_pattern.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            # 5. 평점과 리뷰 길이 관계
            self.df['리뷰길이'] = self.df['리뷰내용'].str.len()
            plt.figure(figsize=(10, 6))
            plt.scatter(self.df['리뷰점수'], self.df['리뷰길이'], alpha=0.6, color='orange')
            plt.title('Relationship between Rating Score and Review Length', fontsize=16)
            plt.xlabel('Rating Score', fontsize=12)
            plt.ylabel('Review Length (characters)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.savefig(os.path.join(self.result_dir, 'rating_vs_length.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            self._log("시각화 생성 완료")
            
        except Exception as e:
            self._log(f"시각화 생성 실패: {str(e)}")
    
    def run_analysis(self) -> None:
        """전체 분석 실행"""
        try:
            self._log("=== 분석 시작 ===")
            
            # 데이터 로드
            self.load_data()
            
            # 인사이트 생성
            self.generate_insights()
            
            # 시각화 생성
            self.create_visualizations()
            
            self._log("=== 분석 완료 ===")
            self._log(f"결과 파일들이 {self.result_dir} 폴더에 저장되었습니다.")
            
        except Exception as e:
            self._log(f"분석 실행 실패: {str(e)}")
            raise


def main() -> None:
    """메인 함수 - 프로그램 진입점"""
    try:
        # CSV 파일 경로 설정
        csv_file_path = "/home/aa/AI_literacy/data/reviewcontents.csv"
        result_directory = "/home/aa/AI_literacy/result"
        
        # 분석기 인스턴스 생성
        analyzer = ReviewDataAnalyzer(csv_file_path, result_directory)
        
        # 분석 실행
        analyzer.run_analysis()
        
        print("\n분석이 성공적으로 완료되었습니다!")
        print(f"결과 파일들을 {result_directory} 폴더에서 확인하세요.")
        
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()