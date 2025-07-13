PROJECT: Log Analyzer for Suspicious Activity

OVERVIEW
A script that scans system logs (/var/log/auth.log, /var/log/syslog, etc.) for suspicious activity such as failed login attempts, unauthorized access, or brute-force attacks.
It can alert administrators via email or display reports.
📜 Key Features:

Extract login failures and unauthorized SSH access.
Generate a summary report.
Email notifications for critical alerts.
📌 Commands Used: grep, awk, sed, mail, cat, tail

BRIEF
A Log Analyzer is a shell script that scans system logs for suspicious activities like:
✅ Multiple failed login attempts
✅ Unauthorized SSH access
✅ Unexpected system reboots
✅ Possible brute-force attacks

The script will:

Monitor /var/log/auth.log (for authentication failures)
Extract failed SSH logins, root login attempts, and multiple failed attempts from the same IP
Generate a summary report
Optionally send an email alert when suspicious activity is detected


Step 1: Understanding Log Files
Most Linux distributions store authentication logs in:
📌 Ubuntu/Debian: /var/log/auth.log
📌 CentOS/RHEL: /var/log/secure

Inside /var/log/auth.log, you'll find entries like:
Feb 20 12:05:43 server sshd[1234]: Failed password for root from 192.168.1.100 port 54321 ssh2
Feb 20 12:06:01 server sshd[1235]: Accepted password for user1 from 192.168.1.101 port 45231 ssh2
Feb 20 12:07:22 server sshd[1236]: Failed password for invalid user admin from 192.168.1.102 port 33221 ssh2

We will extract:

Failed logins
Root login attempts
Repeated failed attempts from the same IP (possible brute force attack)

Step 3: Running the Script
1️⃣ Give execution permission:

bash
Copy
Edit
chmod +x log_analyzer.sh
2️⃣ Run it:

bash
Copy
Edit
sudo ./log_analyzer.sh
Step 4: Automating with Cron Job
To run this script automatically, add it to crontab:

bash
Copy
Edit
sudo crontab -e
Add this line to run the script every hour:

bash
Copy
Edit
0 * * * * /path/to/log_analyzer.sh
Step 5: Enhancements (Optional)
✅ Send alerts via Telegram or Slack instead of email
✅ Store reports in a database for long-term tracking
✅ Auto-block attackers using iptables or fail2ban

Would you like me to help add any of these features? 🚀








