import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import io
from statistics import median, mode, mean
import pandas as pd
from collections import defaultdict

DATA_FILE = "OEPS_data.json"

STOP_WORDS = set([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will',
    'with', 'i', 'you', 'your', 'we', 'they', 'them', 'their', 'this', 'these', 'those',
    'am', 'have', 'had', 'do', 'does', 'did', 'but', 'or', 'not', 'no', 'so', 'what', 'which'
])

def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def filter_data_by_date_range(data, start_date, end_date):
    return [entry for entry in data if start_date <= datetime.fromisoformat(entry['date']) <= end_date]

import pandas as pd

def generate_score_trend_visualization(filtered_data):
    # Convert data to pandas DataFrame
    df = pd.DataFrame([(datetime.fromisoformat(entry['date']), entry['total score']) for entry in filtered_data],
                      columns=['date', 'score'])
    
    # Resample data to monthly averages
    monthly_avg = df.set_index('date').resample('QE')['score'].mean()
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_avg.index, monthly_avg.values, marker='o')
    plt.title('Average Scores by Quarter')
    plt.xlabel('Date')
    plt.ylabel('Average Total Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Add value labels on the points
    for x, y in zip(monthly_avg.index, monthly_avg.values):
        plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    return ('Average Monthly Scores Over Time', img_buffer)

def generate_temporal_analysis(filtered_data):
    exam_dates = [datetime.fromisoformat(entry['date']) for entry in filtered_data]
    
    # Aggregate by quarter
    exams_per_quarter = defaultdict(int)
    for date in exam_dates:
        quarter = f"{date.year} Q{(date.month-1)//3 + 1}"
        exams_per_quarter[quarter] += 1
    
    # Sort quarters chronologically
    sorted_quarters = sorted(exams_per_quarter.items(), key=lambda x: datetime.strptime(x[0], "%Y Q%m"))
    
    # Calculate overall trend
    if len(sorted_quarters) > 1:
        first_half = sum(count for _, count in sorted_quarters[:len(sorted_quarters)//2])
        second_half = sum(count for _, count in sorted_quarters[len(sorted_quarters)//2:])
        trend = "Increasing" if second_half > first_half else "Decreasing"
    else:
        trend = "Not enough data to determine trend"
    
    # Find the busiest quarter
    busiest_quarter = max(exams_per_quarter, key=exams_per_quarter.get)
    
    return {
        "quarters": sorted_quarters,
        "trend": trend,
        "busiest_quarter": busiest_quarter,
        "busiest_quarter_count": exams_per_quarter[busiest_quarter]
    }

# Helper function to create report visualizations
def generate_visualizations(filtered_data):
    visualizations = []

    # Pie chart of band distribution
    plt.figure(figsize=(8, 6))
    band_counts = Counter(entry['band'] for entry in filtered_data)
    plt.pie(band_counts.values(), labels=band_counts.keys(), autopct='%1.1f%%')
    plt.title('Distribution of Bands')
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    visualizations.append(('Band Distribution', img_buffer))
    plt.close()

    # Score trends over time
    score_trend_vis = generate_score_trend_visualization(filtered_data)
    visualizations.append(score_trend_vis)

    # Bar chart of average scores by question
    question_scores = [[], [], []]
    for entry in filtered_data:
        for i, question in enumerate(entry['questions']):
            question_scores[i].append(question['question score'])

    avg_scores = [sum(scores) / len(scores) if scores else 0 for scores in question_scores]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(['Question 1', 'Question 2', 'Question 3'], avg_scores)
    plt.title('Average Scores by Question Type')
    plt.ylabel('Average Score')
    plt.ylim(0, 3)  # Set y-axis limit from 0 to 3

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')

    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    visualizations.append(('Average Scores by Question', img_buffer))
    plt.close()

    # Word cloud of examiner notes
    all_notes = ' '.join([note for entry in filtered_data for question in entry['questions'] for note in question['notes']])
    words = [word.lower() for word in all_notes.split() if word.lower() not in STOP_WORDS and len(word) > 3]
    filtered_text = ' '.join(words)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Examiner Notes (Stop Words Removed)')
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    visualizations.append(('Examiner Notes Word Cloud', img_buffer))
    plt.close()

    # Common words
    common_words = Counter(words).most_common(10)
    
    plt.figure(figsize=(10, 5))
    plt.bar([word for word, count in common_words], [count for word, count in common_words])
    plt.title('Top 10 Most Common Words in Examiner Notes (Stop Words Removed)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    visualizations.append(('Common Words in Notes', img_buffer))
    plt.close()

    # Scoring by examiner
    examiner_scores = {}
    for entry in filtered_data:
        examiner = entry['examiner']
        score = entry['total score']
        if examiner not in examiner_scores:
            examiner_scores[examiner] = []
        examiner_scores[examiner].append(score)

    plt.figure(figsize=(12, 6))
    plt.boxplot(examiner_scores.values(), tick_labels=examiner_scores.keys())
    plt.title('Score Distribution by Examiner')
    plt.xlabel('Examiner')
    plt.ylabel('Total Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    visualizations.append(('Score Distribution by Examiner', img_buffer))
    plt.close()
    
    return visualizations, examiner_scores

# Helper function to generate visualizations of the EAP requirement data
def generate_eap_requirement_visualization(filtered_data):
    # Count EAP requirements
    eap_counts = Counter(entry['EAP requirement'] for entry in filtered_data)
    
    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(eap_counts.values(), labels=eap_counts.keys(), autopct='%1.1f%%')
    plt.title('EAP Requirements Distribution')
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

# Helper function to generate a report, will call other functions
def create_report(start_date, end_date):
    data = load_data()
    filtered_data = filter_data_by_date_range(data, start_date, end_date)
    visualizations, examiner_scores = generate_visualizations(filtered_data)
    temporal_data = generate_temporal_analysis(filtered_data)
    
    if not filtered_data:
        print(f"No data available for the selected period.")
        return

    doc = SimpleDocTemplate(f"ITA_Report_{start_date.date()}_to_{end_date.date()}.pdf", pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # First page
    elements.append(Paragraph(f"ITA Assessment Report - {start_date.date()} to {end_date.date()}", styles['Title']))

    # Basic statistics
    total_exams = len(filtered_data)
    
    # Band breakdown
    band_counts = Counter(entry['band'] for entry in filtered_data)
    pass_rate = sum(band_counts[band] for band in ['Low Pass', 'High Pass']) / total_exams if total_exams > 0 else 0
    
    # Score statistics
    scores = [entry['total score'] for entry in filtered_data]
    avg_score = mean(scores) if scores else 0
    median_score = median(scores) if scores else 0
    min_score = min(scores) if scores else 0
    max_score = max(scores) if scores else 0
    
    # Question-specific statistics
    question_scores = [[], [], []]
    for entry in filtered_data:
        for i, question in enumerate(entry['questions']):
            question_scores[i].append(question['question score'])
    avg_question_scores = [mean(scores) if scores else 0 for scores in question_scores]
    
    # EAP Requirement summary
    eap_counts = Counter(entry['EAP requirement'] for entry in filtered_data)
    
    # Examiner statistics
    examiners = set(entry['examiner'] for entry in filtered_data)
    exams_per_examiner = total_exams / len(examiners) if examiners else 0
    
    # Add statistics to the report
    elements.append(Paragraph("Summary Statistics", styles['Heading2']))
    elements.append(Paragraph(f"Total Examinations: {total_exams}", styles['Normal']))
    elements.append(Paragraph(f"Pass Rate: {pass_rate:.2%}", styles['Normal']))
    elements.append(Paragraph(f"Band Distribution:", styles['Normal']))
    for band, count in band_counts.items():
        elements.append(Paragraph(f"  - {band}: {count} ({count/total_exams:.2%})", styles['Normal']))
    
    elements.append(Paragraph("Score Statistics", styles['Heading3']))
    elements.append(Paragraph(f"Average Score: {avg_score:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Median Score: {median_score:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Score Range: {min_score:.2f} - {max_score:.2f}", styles['Normal']))
    
    elements.append(Paragraph("Question-specific Statistics", styles['Heading3']))
    for i, avg in enumerate(avg_question_scores):
        elements.append(Paragraph(f"Question {i+1} Average: {avg:.2f}", styles['Normal']))
    
    elements.append(Paragraph("EAP Requirement Summary", styles['Heading3']))
    for req, count in eap_counts.items():
        elements.append(Paragraph(f"{req}: {count} ({count/total_exams:.2%})", styles['Normal']))
    
    elements.append(Paragraph("Examiner Statistics", styles['Heading3']))
    elements.append(Paragraph(f"Total Examiners: {len(examiners)}", styles['Normal']))
    elements.append(Paragraph(f"Average Exams per Examiner: {exams_per_examiner:.2f}", styles['Normal']))
    
    # Examiner scoring analysis
    elements.append(Paragraph("Examiner Scoring Analysis", styles['Heading3']))
    for examiner, scores in examiner_scores.items():
        avg_score = mean(scores)
        elements.append(Paragraph(f"{examiner}: Average Score = {avg_score:.2f}, Number of Exams = {len(scores)}", styles['Normal']))

    # Temporal analysis
    elements.append(Paragraph("Temporal Analysis", styles['Heading3']))
    elements.append(Paragraph(f"Busiest Quarter: {temporal_data['busiest_quarter']} with {temporal_data['busiest_quarter_count']} exams", styles['Normal']))
    elements.append(Paragraph(f"Overall Trend: {temporal_data['trend']}", styles['Normal']))

    # Create a table for the quarterly data
    quarter_data = [["Quarter", "Number of Exams"]]
    for quarter, count in temporal_data['quarters']:
        quarter_data.append([quarter, str(count)])

    quarter_table = Table(quarter_data)
    quarter_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(quarter_table)

    # Add a visualization of the quarterly data
    plt.figure(figsize=(12, 6))
    quarters, counts = zip(*temporal_data['quarters'])
    plt.bar(quarters, counts)
    plt.title('Number of Exams per Quarter')
    plt.xlabel('Quarter')
    plt.ylabel('Number of Exams')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    elements.append(Image(img_buffer, width=500, height=300))

    elements.append(PageBreak())

    # Second page - EAP Requirements
    elements.append(Paragraph("EAP Requirements Analysis", styles['Title']))
    
    eap_img_buffer = generate_eap_requirement_visualization(filtered_data)
    elements.append(Image(eap_img_buffer, width=400, height=300))
    
    elements.append(PageBreak())

    # Remaining visualizations
    for title, img_buffer in visualizations:
        elements.append(Paragraph(title, styles['Heading2']))
        elements.append(Image(img_buffer, width=500, height=300))
        elements.append(PageBreak())

    doc.build(elements)
    print(f"Report generated: ITA_Report_{start_date.date()}_to_{end_date.date()}.pdf")
    
def get_report_period():
    while True:
        choice = input("Select reporting period:\n1. Last 365 days\n2. Custom year range\nEnter your choice (1 or 2): ")
        if choice == '1':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            return start_date, end_date
        elif choice == '2':
            while True:
                try:
                    start_year = int(input("Enter start year: "))
                    end_year = int(input("Enter end year: "))
                    if start_year <= end_year:
                        return datetime(start_year, 1, 1), datetime(end_year, 12, 31)
                    else:
                        print("Start year must be less than or equal to end year.")
                except ValueError:
                    print("Please enter valid year numbers.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

def main():
    start_date, end_date = get_report_period()
    create_report(start_date, end_date)

if __name__ == "__main__":
    main()