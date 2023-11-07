import requests
import json
import smtplib
from email.mime.text import MIMEText

# Get the budget data
url = "https://csc-morpheus.anycloud.vn/api/budgets/7"

headers = {
    "accept": "application/json",
    "authorization": "Bearer CHANGE_ME"
}

response = requests.get(url, headers=headers, verify=False)

# Email configuration
smtp_server = "smtp.elasticemail.com"
smtp_port = 2525
smtp_username = "cuong.dq@csc-jsc.com"
smtp_password = "REPLACE_ME"
sender_email = "REPLACE_ME"
recipient_email = "REPLACE_ME"


# Load JSON data from the response content
data = json.loads(response.text)

# Extract intervals
intervals = data['budget']['stats']['intervals']

# Create an HTML table with the budget data, highlighting exceeded budgets
table = """
<table border="1" style="border-collapse: collapse; width: 100%;">
  <tr>
    <th>Month</th>
    <th>Budget</th>
    <th>Cost</th>
  </tr>
"""

for interval in intervals:
    if interval['cost'] > interval['budget']:
        table += f"""
        <tr style="background-color: #ffcccc;">
          <td>{interval['month']}</td>
          <td>{interval['budget']}</td>
          <td>{interval['cost']}</td>
        </tr>
        """
    else:
        table += f"""
        <tr>
          <td>{interval['month']}</td>
          <td>{interval['budget']}</td>
          <td>{interval['cost']}</td>
        </tr>
        """

table += "</table>"

# Create a text version of the email body
email_body = table

# If there is budget exceeding, add an alert message
for interval in intervals:
    budget = interval['budget']
    cost = interval['cost']
    interval_name = interval['month']
    
    if cost > budget:
        alert_message = f"Alert: Cost ({cost}) is greater than Budget ({budget}) for interval {interval_name}\n"
        email_body += alert_message

# If there are alerts, send an email
if any(cost > budget for interval in intervals for cost, budget in [(interval['cost'], interval['budget'])]):
    msg = MIMEText(email_body, 'html')
    msg['Subject'] = "Budget Alert and Budget Data"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Establish a secure session with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())

# Print the JSON response content
print("JSON response:")
print(response.text)
