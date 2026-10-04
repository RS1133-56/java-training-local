#!/usr/bin/env python3
"""
研修進捗データ分析スクリプト

各Dayの実施日と実績時間を集計し、
予定との差異を可視化します。
"""

import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def parse_day_file(file_path):
    """Dayファイルから実施情報を抽出"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Day番号
    day_match = re.search(r'# Day (\d+)', content)
    day = int(day_match.group(1)) if day_match else None
    
    # Week情報
    week_match = re.search(r'- 予定: (Week \d+)', content)
    week = week_match.group(1) if week_match else None
    
    # 実施日
    date_match = re.search(r'- 実施日: (\d{4}/\d{2}/\d{2})', content)
    actual_date = date_match.group(1) if date_match else None
    
    # 予定時間
    planned_match = re.search(r'- 予定時間: (\d+)h', content)
    planned_hours = int(planned_match.group(1)) if planned_match else 8
    
    # 実績時間
    actual_match = re.search(r'- 実績時間: (\d+)h', content)
    actual_hours = int(actual_match.group(1)) if actual_match else None
    
    return {
        'day': day,
        'week': week,
        'actual_date': actual_date,
        'planned_hours': planned_hours,
        'actual_hours': actual_hours
    }

def analyze_progress(daily_tasks_dir):
    """進捗を分析"""
    
    data = []
    
    for day in range(1, 41):
        file_path = daily_tasks_dir / f'day-{day:02d}.md'
        
        if file_path.exists():
            info = parse_day_file(file_path)
            data.append(info)
    
    return data

def generate_report(data):
    """レポート生成"""
    
    print("="*60)
    print("研修進捗分析レポート")
    print("="*60)
    print()
    
    # 完了日数
    completed = [d for d in data if d['actual_hours'] is not None]
    total_days = len(data)
    completed_days = len(completed)
    
    print(f"📊 全体進捗: {completed_days}/{total_days}日 ({completed_days/total_days*100:.1f}%)")
    print()
    
    # Week別集計
    week_stats = defaultdict(lambda: {'total': 0, 'completed': 0, 'planned': 0, 'actual': 0})
    
    for d in data:
        week = d['week']
        week_stats[week]['total'] += 1
        week_stats[week]['planned'] += d['planned_hours']
        
        if d['actual_hours'] is not None:
            week_stats[week]['completed'] += 1
            week_stats[week]['actual'] += d['actual_hours']
    
    print("📅 Week別進捗:")
    print("-"*60)
    for week in sorted(week_stats.keys()):
        stats = week_stats[week]
        progress = stats['completed'] / stats['total'] * 100
        print(f"{week}: {stats['completed']}/{stats['total']}日 ({progress:.0f}%) | "
              f"予定{stats['planned']}h / 実績{stats['actual']}h")
    print()
    
    # 時間分析
    if completed:
        total_planned = sum(d['planned_hours'] for d in completed)
        total_actual = sum(d['actual_hours'] for d in completed)
        diff = total_actual - total_planned
        
        print("⏱️  時間分析:")
        print("-"*60)
        print(f"予定時間: {total_planned}h")
        print(f"実績時間: {total_actual}h")
        print(f"差分: {diff:+d}h ({diff/total_planned*100:+.1f}%)")
        print()
        
        # 時間超過トップ5
        overtime = [(d['day'], d['actual_hours'] - d['planned_hours']) 
                    for d in completed 
                    if d['actual_hours'] > d['planned_hours']]
        overtime.sort(key=lambda x: x[1], reverse=True)
        
        if overtime:
            print("⚠️  時間超過トップ5:")
            print("-"*60)
            for i, (day, diff) in enumerate(overtime[:5], 1):
                print(f"{i}. Day {day}: +{diff}h")
            print()
        
        # 時間短縮トップ5
        undertime = [(d['day'], d['planned_hours'] - d['actual_hours']) 
                     for d in completed 
                     if d['actual_hours'] < d['planned_hours']]
        undertime.sort(key=lambda x: x[1], reverse=True)
        
        if undertime:
            print("✅ 時間短縮トップ5:")
            print("-"*60)
            for i, (day, diff) in enumerate(undertime[:5], 1):
                print(f"{i}. Day {day}: -{diff}h")
            print()
    
    # 完了日付の分析
    dates = [d for d in completed if d['actual_date']]
    if dates:
        print("📆 実施期間:")
        print("-"*60)
        
        date_objs = [datetime.strptime(d['actual_date'], '%Y/%m/%d') for d in dates]
        start_date = min(date_objs)
        end_date = max(date_objs)
        duration = (end_date - start_date).days + 1
        
        print(f"開始日: {start_date.strftime('%Y/%m/%d')}")
        print(f"終了日: {end_date.strftime('%Y/%m/%d')}")
        print(f"期間: {duration}日")
        print()

def export_csv(data, output_path):
    """CSV形式でエクスポート"""
    
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # ヘッダー
        writer.writerow(['Day', 'Week', '実施日', '予定時間', '実績時間', '差分'])
        
        # データ
        for d in data:
            diff = d['actual_hours'] - d['planned_hours'] if d['actual_hours'] else ''
            writer.writerow([
                d['day'],
                d['week'],
                d['actual_date'] or '',
                d['planned_hours'],
                d['actual_hours'] or '',
                diff
            ])
    
    print(f"✅ CSVファイルを出力しました: {output_path}")

def main():
    """メイン処理"""
    
    daily_tasks_dir = Path(__file__).resolve().parent / 'daily-tasks'
    
    # データ収集
    print("データ収集中...")
    data = analyze_progress(daily_tasks_dir)
    
    # レポート生成
    generate_report(data)
    
    # CSV出力
    csv_path = Path(__file__).resolve().parent / 'progress-analysis.csv'
    export_csv(data, csv_path)
    
    print("="*60)
    print("分析完了！")
    print("="*60)

if __name__ == "__main__":
    main()
