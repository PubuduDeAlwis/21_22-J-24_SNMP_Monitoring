from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from snmp_get import snmp_get
CLIENT_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
message = snmp_get()
service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

emailMsg = message
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'www.kkpdealwis@gmail.com'
mimeMessage['subject'] = 'Aquaponic Server Resource Utilization'
mimeMessage.attach(MIMEText(emailMsg, 'html'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)
