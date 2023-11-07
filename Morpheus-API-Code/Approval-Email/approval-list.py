import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate

# Replace with the appropriate URL for approvals
url = "https://csc-morpheus.anycloud.vn/api/approvals"

headers = {
    "accept": "application/json",
    "authorization": "Bearer CHANGE_ME"
}

response = requests.get(url, headers=headers, verify=False)

approvals_data = response.json()  # Convert the response to JSON format

# Check if the response contains "1 requested" status
if any(approval.get("status") == "1 requested" for approval in approvals_data["approvals"]):
    # Extract the relevant data for creating a table
    table_data = []
    for approval in approvals_data["approvals"]:
        table_data.append([
            approval["id"],
            approval["name"],
            approval["requestType"],
            approval["account"]["name"],
            approval["approver"]["name"],
            approval["dateCreated"],
            approval["lastUpdated"],
            approval["requestBy"]
        ])

    # Create and print the table
    headers = ["ID", "Name", "Request Type", "Account Name", "Approver Name", "Date Created", "Last Updated", "Requested By"]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    # Email configuration
    smtp_server = "smtp.elasticemail.com"
    smtp_port = 2525
    smtp_username = "cuong.dq@csc-jsc.com"
    smtp_password = "REPLACE_ME"
    sender_email = "REPLACE_ME"
    recipient_email = "REPLACE_ME"

    # Create email body
    email_body = """
<html>
  <body>
    <h2>Approval Alert</h2>
"""

# Add the tabular JSON data to the email body
    email_body += """
    <h3>Approval List</h3>
    <table style="border: 1px solid black; border-collapse: collapse;">
    <tr>
        <th style="border: 1px solid black; padding: 10px;">ID</th>
        <th style="border: 1px solid black; padding: 10px;">Name</th>
        <th style="border: 1px solid black; padding: 10px;">Request Type</th>
        <th style="border: 1px solid black; padding: 10px;">Account Name</th>
        <th style="border: 1px solid black; padding: 10px;">Approver Name</th>
        <th style="border: 1px solid black; padding: 10px;">Date Created</th>
        <th style="border: 1px solid black; padding: 10px;">Last Updated</th>
        <th style="border: 1px solid black; padding: 10px;">Requested By</th>
    </tr>
    """

    # Add each row of the tabular JSON data
    for approval in approvals_data["approvals"]:
        email_body += f"""
        <tr>
        <td style="border: 1px solid black; padding: 10px;">{approval['id']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['name']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['requestType']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['account']['name']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['approver']['name']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['dateCreated']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['lastUpdated']}</td>
        <td style="border: 1px solid black; padding: 10px;">{approval['requestBy']}</td>
        </tr>
        """

    # Close the table and body tags
    email_body += """
    </table>
    </body>
    </html>
    """

    # Email subject
    subject = "Approval Email List"

    # Send the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'html'))

    # Establish a secure session with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())

# Print the JSON response content
print("JSON response:")
print(response.text)
