#!/bin/bash

LOG_FILE="/var/log/auth.log"  # Change this if using CentOS/RHEL
ALERT_THRESHOLD=5  # Number of failed attempts before triggering an alert
REPORT_FILE="suspicious_activity_report.txt"

echo "=== Log Analysis Report ===" > "$REPORT_FILE"
echo "Date: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1️⃣ Find failed login attempts
echo "❌ Failed Login Attempts:" >> "$REPORT_FILE"
grep "Failed password" "$LOG_FILE" | awk '{print $1, $2, $3, $9, $11}' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 2️⃣ Find root login attempts
echo "⚠️ Root Login Attempts:" >> "$REPORT_FILE"
grep "Accepted password for root" "$LOG_FILE" | awk '{print $1, $2, $3, $9, $11}' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 3️⃣ Find brute-force attempts (IPs with multiple failures)
echo "🚨 Possible Brute Force Attacks:" >> "$REPORT_FILE"
grep "Failed password" "$LOG_FILE" | awk '{print $11}' | sort | uniq -c | sort -nr | awk -v threshold=$ALERT_THRESHOLD '$1 >= threshold {print "IP:", $2, "- Failed Attempts:", $1}' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 4️⃣ Send alert if brute-force detected
if grep -q "Possible Brute Force Attacks:" "$REPORT_FILE"; then
    echo "Brute-force attack detected! Sending alert..."
    mail -s "Security Alert: Brute Force Attack Detected" root@localhost < "$REPORT_FILE"
fi

echo "Analysis complete. Report saved in $REPORT_FILE"
