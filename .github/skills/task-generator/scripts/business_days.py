#!/usr/bin/env python3
"""
Business Day Calculator and Task Timeline Generator
Matches Brendon's Power Automate flow exactly - calculates business days (excluding weekends)

Supports two modes:
  - Initial engagement: Full 15-task template (T-28 to T+3)
  - Journey follow-on: Streamlined 12-task template (T-21 to T+3) for sessions
    where customer relationship and context are already established
"""

from datetime import datetime, timedelta
import csv
import json
import os
from typing import List, Dict, Tuple, Optional

# Exact task template from Power Automate flow - used for FIRST session
ENGAGEMENT_TASKS = [
    {"title": "Schedule Internal Precall", "offset": 28},
    {"title": "Research customer", "offset": 22},
    {"title": "Execute Internal Precall", "offset": 21},
    {"title": "Draft Agenda", "offset": 20},
    {"title": "Schedule Customer Precall", "offset": 20},
    {"title": "Execute Customer Precall", "offset": 14},
    {"title": "Schedule internal resources", "offset": 14},
    {"title": "Validate Agenda with ATU", "offset": 10},
    {"title": "Validate Agenda with Customer", "offset": 7},
    {"title": "Prep Demos", "offset": 7},
    {"title": "Confirm all Customer pre-work is completed", "offset": 3},
    {"title": "Send Satisfaction Survey to customer", "offset": 0},
    {"title": "Conduct MSFT Debrief", "offset": -2},
    {"title": "Share Engagement Materials with Customer", "offset": -2},
    {"title": "Complete Engagement Close out form", "offset": -3}
]

# Streamlined template for follow-on sessions in a customer journey
# Omits "Research customer" (already known) and "Schedule Internal Precall" (replaced
# with session-specific prep). Shorter lead time since relationships are established.
JOURNEY_SESSION_TASKS = [
    {"title": "Schedule Internal Session Prep", "offset": 21},
    {"title": "Execute Internal Session Prep", "offset": 14},
    {"title": "Draft Session Agenda", "offset": 14},
    {"title": "Schedule Customer Precall", "offset": 14},
    {"title": "Execute Customer Precall", "offset": 10},
    {"title": "Schedule internal resources", "offset": 10},
    {"title": "Validate Agenda with ATU", "offset": 7},
    {"title": "Validate Agenda with Customer", "offset": 5},
    {"title": "Prep Demos / Session Materials", "offset": 5},
    {"title": "Confirm all Customer pre-work is completed", "offset": 3},
    {"title": "Send Satisfaction Survey to customer", "offset": 0},
    {"title": "Conduct MSFT Debrief", "offset": -2},
    {"title": "Share Session Materials with Customer", "offset": -2},
    {"title": "Complete Session Close out", "offset": -3}
]


def calculate_business_days(target_date: datetime, days_offset: int) -> datetime:
    """
    Calculate business day offset from target date (excludes weekends).
    Positive offset = days before engagement (T-minus)
    Negative offset = days after engagement (T-plus)
    
    Args:
        target_date: The engagement date
        days_offset: Number of business days before (positive) or after (negative)
    
    Returns:
        Calculated date
    """
    # Direction: positive offset means go backwards (T-28 is 28 business days BEFORE)
    direction = -1 if days_offset > 0 else 1
    days_to_move = abs(days_offset)
    
    result = target_date
    days_moved = 0
    
    while days_moved < days_to_move:
        result += timedelta(days=direction)
        
        # Only count weekdays (Monday=0, Sunday=6)
        if result.weekday() < 5:  # Monday to Friday
            days_moved += 1
    
    return result


def generate_task_timeline(
    customer_name: str,
    engagement_date: str,  # YYYY-MM-DD format
    assignee: str = "Brendon Colburn",
    session_type: str = "initial",
    session_label: Optional[str] = None
) -> List[Dict]:
    """
    Generate complete task timeline with business day calculations.
    Returns list of tasks ready for Planner CSV import.

    Args:
        customer_name: Customer name for task titles
        engagement_date: Session date in YYYY-MM-DD format
        assignee: Person assigned to tasks
        session_type: "initial" for first engagement, "followon" for journey sessions
        session_label: Optional label for bucket (e.g. "Session 2 - Envisioning").
                       If not provided, defaults to "{date} - {customer}"
    """
    
    # Parse engagement date
    eng_date = datetime.strptime(engagement_date, "%Y-%m-%d")
    
    # Select task template based on session type
    task_template_list = JOURNEY_SESSION_TASKS if session_type == "followon" else ENGAGEMENT_TASKS
    
    # Bucket name - supports custom labeling for journey sessions
    if session_label:
        bucket_name = f"{engagement_date} - {customer_name} - {session_label}"
    else:
        bucket_name = f"{engagement_date} - {customer_name}"
    
    tasks = []
    
    # Build a short session tag for task names in follow-on sessions
    # e.g. "[3/12]" so you see "Textron Systems [3/12] - Validate Agenda with Customer"
    if session_type == "followon":
        session_tag = f"[{eng_date.month}/{eng_date.day}]"
    else:
        session_tag = None
    
    for task_template in task_template_list:
        # Calculate due date using business days
        due_date = calculate_business_days(eng_date, task_template["offset"])
        
        # Task title includes customer name and session tag for follow-on sessions
        if session_tag:
            task_title = f"{customer_name} {session_tag} - {task_template['title']}"
        else:
            task_title = f"{customer_name} - {task_template['title']}"
        
        # Format for Planner CSV import
        task = {
            "Task Name": task_title,
            "Assignment": assignee,
            "Start date": due_date.strftime("%m/%d/%Y"),
            "Due date": due_date.strftime("%m/%d/%Y"),
            "Bucket": bucket_name,
            "Progress": "Not started",
            "Priority": "Medium",
            "Labels": "Add label"
        }
        
        tasks.append(task)
    
    return tasks


def generate_journey_tasks(
    customer_name: str,
    sessions: List[Dict],
    assignee: str = "Brendon Colburn"
) -> Dict[str, List[Dict]]:
    """
    Generate task timelines for multiple sessions in a customer journey.
    
    Args:
        customer_name: Customer name
        sessions: List of dicts with keys: date (YYYY-MM-DD), label (optional str), 
                  type ("initial" | "followon")
        assignee: Person assigned to tasks
    
    Returns:
        Dict mapping session date to list of tasks
    """
    all_session_tasks = {}
    
    for session in sessions:
        session_date = session["date"]
        session_label = session.get("label")
        session_type = session.get("type", "followon")
        
        tasks = generate_task_timeline(
            customer_name=customer_name,
            engagement_date=session_date,
            assignee=assignee,
            session_type=session_type,
            session_label=session_label
        )
        
        all_session_tasks[session_date] = tasks
    
    return all_session_tasks


def save_journey_tasks(
    customer_name: str,
    session_tasks: Dict[str, List[Dict]],
    output_dir: str,
    combined: bool = True
) -> List[str]:
    """
    Save journey session tasks as per-session CSVs and optionally a combined CSV.
    
    Args:
        customer_name: Customer name for filename
        session_tasks: Dict from generate_journey_tasks()
        output_dir: Directory to write CSV files
        combined: If True, also write a combined CSV with all sessions
    
    Returns:
        List of created file paths
    """
    created_files = []
    all_tasks = []
    
    for session_date, tasks in sorted(session_tasks.items()):
        # Per-session file: tasks_YYYY-MM-DD.csv
        filename = f"tasks_{session_date}.csv"
        filepath = os.path.join(output_dir, filename)
        save_tasks_csv(tasks, filepath)
        created_files.append(filepath)
        all_tasks.extend(tasks)
    
    if combined and len(session_tasks) > 1:
        combined_path = os.path.join(output_dir, "tasks_all_sessions.csv")
        save_tasks_csv(all_tasks, combined_path)
        created_files.append(combined_path)
    
    return created_files


def save_tasks_csv(tasks: List[Dict], output_path: str) -> str:
    """Save tasks to CSV format for Microsoft Planner import"""
    if not tasks:
        return None
    
    fieldnames = [
        "Task Name",
        "Assignment",
        "Start date",
        "Due date",
        "Bucket",
        "Progress",
        "Priority",
        "Labels"
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)
    
    return output_path


def format_task_summary(tasks: List[Dict], session_label: Optional[str] = None) -> str:
    """Format tasks for display in preview"""
    summary = []
    
    if session_label:
        summary.append(f"SESSION: {session_label}")
        summary.append("")
    
    # Split at the engagement day (offset 0) - pre-engagement vs post
    pre_tasks = [t for t in tasks if t.get("_offset", 1) > 0] if any("_offset" in t for t in tasks) else tasks[:len(tasks)-3]
    post_tasks = [t for t in tasks if t.get("_offset", 1) <= 0] if any("_offset" in t for t in tasks) else tasks[len(tasks)-3:]
    
    summary.append("PRE-SESSION TASKS:")
    for task in tasks[:-3]:  # All except last 3 (post-engagement)
        summary.append(f"  {task['Due date']} - {task['Task Name']}")
    
    summary.append("\nPOST-SESSION TASKS:")
    for task in tasks[-3:]:  # Last 3 are post-engagement
        summary.append(f"  {task['Due date']} - {task['Task Name']}")
    
    return "\n".join(summary)


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate engagement task timelines with business day calculations",
        epilog="""
Examples:
  # Initial engagement (full 15-task template)
  python business_days.py "Contoso" "2026-03-15"

  # Journey follow-on session (streamlined 12-task template)
  python business_days.py "Textron Systems" "2026-03-12" --followon --label "Session 2 - Envisioning"

  # Multiple journey sessions at once
  python business_days.py "Textron Systems" "2026-03-12" "2026-03-31" --followon --output /path/to/journey/folder
        """
    )
    parser.add_argument("customer", help="Customer name")
    parser.add_argument("dates", nargs="+", help="Engagement date(s) in YYYY-MM-DD format")
    parser.add_argument("--followon", action="store_true", 
                        help="Use follow-on session template (shorter lead time, no research task)")
    parser.add_argument("--labels", nargs="*", 
                        help="Session labels (one per date, e.g. 'Session 2' 'Session 3')")
    parser.add_argument("--output", "-o", 
                        help="Output directory (default: current directory)")
    parser.add_argument("--assignee", default="Brendon Colburn",
                        help="Task assignee (default: Brendon Colburn)")
    
    args = parser.parse_args()
    
    session_type = "followon" if args.followon else "initial"
    output_dir = args.output or "."
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    if len(args.dates) == 1:
        # Single session mode (backward compatible)
        date = args.dates[0]
        label = args.labels[0] if args.labels else None
        
        tasks = generate_task_timeline(args.customer, date, args.assignee, session_type, label)
        
        print(f"\n{'='*60}")
        print(f"ENGAGEMENT: {args.customer}")
        print(f"DATE: {date}")
        print(f"TYPE: {'Follow-on Session' if args.followon else 'Initial Engagement'}")
        if label:
            print(f"LABEL: {label}")
        print(f"{'='*60}\n")
        
        print(format_task_summary(tasks, label))
        
        # Save CSV - use session-specific naming for journey sessions
        if args.followon:
            output_file = os.path.join(output_dir, f"tasks_{date}.csv")
        else:
            output_file = os.path.join(output_dir, f"tasks.csv")
        save_tasks_csv(tasks, output_file)
        print(f"\n✅ Tasks saved to: {output_file}")
    
    else:
        # Multi-session mode (journey)
        labels = args.labels or [None] * len(args.dates)
        if len(labels) < len(args.dates):
            labels.extend([None] * (len(args.dates) - len(labels)))
        
        sessions = []
        for date, label in zip(args.dates, labels):
            sessions.append({
                "date": date,
                "label": label,
                "type": session_type
            })
        
        session_tasks = generate_journey_tasks(args.customer, sessions, args.assignee)
        
        print(f"\n{'='*60}")
        print(f"JOURNEY: {args.customer}")
        print(f"SESSIONS: {len(args.dates)}")
        print(f"TYPE: {'Follow-on Sessions' if args.followon else 'Initial Engagements'}")
        print(f"{'='*60}")
        
        for date, label in zip(args.dates, labels):
            tasks = session_tasks[date]
            print(f"\n--- {date} {'(' + label + ') ' if label else ''}---\n")
            print(format_task_summary(tasks, label))
        
        created = save_journey_tasks(args.customer, session_tasks, output_dir)
        print(f"\n✅ Files created:")
        for f in created:
            print(f"   {f}")
