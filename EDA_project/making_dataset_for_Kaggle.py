# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 19:12:45 2023

@author: Soo.Y
"""
from glob import glob
import pandas as pd

pd.set_option('display.max_columns', None)


file_list = glob(r"./data/*")  # 파일 경로

data = pd.read_csv(file_list[1], encoding='euc-kr')

data = data.iloc[:, 0:(data.shape[1]-7)]  # 치아관련 데이터 삭제, 치석 데이터 null 수 : 621,422개
data = data.iloc[:, 2:(data.shape[1])]  # 기준년도, 가입자 일련번호 삭제

# 그외 null data 삭제
final_data = data.dropna()
# 컬럼 순서 변경 및 분석할 컬럼 선정
final_data = final_data[['성별코드', '연령대코드(5세단위)', '신장(5Cm단위)', '체중(5Kg단위)', '허리둘레',
                         '시력(좌)', '시력(우)', '청력(좌)', '청력(우)', '수축기혈압', '이완기혈압',
                         '식전혈당(공복혈당)', '총콜레스테롤', 'HDL콜레스테롤', 'LDL콜레스테롤', '트리글리세라이드',
                         '혈색소', '요단백', '혈청크레아티닌', '(혈청지오티)AST', '(혈청지오티)ALT', '감마지티피',
                         '흡연상태', "음주여부"]]

# 성별 수치형을 문자형으로 변경
mask = final_data['성별코드'] == 1
final_data['성별코드'][mask] = "Male"
mask = final_data['성별코드'] == 2
final_data['성별코드'][mask] = "Female"

# 나이 그룹을 수치형으로 변경
final_data['연령대코드(5세단위)'].value_counts()

age_index = {group_num: age_num for group_num, age_num in zip(range(1, 19), range(0, 90, 5))}

for xx in final_data['연령대코드(5세단위)'].unique():
    if xx in age_index.keys():
        mask = final_data['연령대코드(5세단위)'] == xx
        final_data.loc[mask, ('연령대코드(5세단위)')] = age_index.get(xx)
    else:
        print('Not change data')

# 컬럼 이름 변경
final_data.rename(columns={
    '성별코드': 'sex', '연령대코드(5세단위)': 'age', '신장(5Cm단위)': 'height', '체중(5Kg단위)': 'weight',
    '허리둘레': 'waistline', '시력(좌)': 'sight_left', '시력(우)': 'sight_right',
    '청력(좌)': 'hear_left', '청력(우)': 'hear_right',
    '수축기혈압': 'SBP', '이완기혈압': 'DBP',
    '식전혈당(공복혈당)': 'BLDS',
    '총콜레스테롤': 'tot_chole', 'HDL콜레스테롤': 'HDL_chole', 'LDL콜레스테롤': 'LDL_chole',
    '트리글리세라이드': 'triglyceride',
    '혈색소': 'hemoglobin', '요단백': 'urine_protein', '혈청크레아티닌': 'serum_creatinine',
    '(혈청지오티)AST': 'SGOT_AST', '(혈청지오티)ALT': 'SGOT_ALT', '감마지티피': 'gamma_GTP',
                '흡연상태': 'SMK_stat_type_cd', "음주여부": 'DRK_YN'
}, inplace=True)

# CSV 저장하기
# final_data.to_csv("output.csv", index=False)
