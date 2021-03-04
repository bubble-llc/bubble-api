import smtplib
import yaml
from yaml import Loader
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# EMAIL_ADDRESS = 'steven@bubble.llc'
# EMAIL_PASSWORD = 'ygejlkjataaijrqk'

class EmailServer:
	def __init__(self, config_file):
		self.config = self.load_configuration(config_file)
		
	def load_configuration(self, config_file):
		print('Loading email configuration...')
		with open(config_file, 'r') as filehandle:
			config = yaml.load(filehandle.read(), Loader=Loader)
			return config
	
	def send_email(self, username, email, verificaiton_code):
		
		# verification_link = "http://0.0.0.0:8000/email_validation?email={}&validation_code={}".format(email,verificaiton_code)
		verification_link = "https://dashboard.stocksandshare.com/chitchat/email_validation?email={}&validation_code={}".format(email,verificaiton_code)
		print(verification_link)
		msg = MIMEMultipart("alternative")
		msg['Subject'] = "Bubble Email Validation"
		msg['From'] = self.config['email']
		msg['To'] = email
		
		
		text = """
		Congraduations {} for making a Bubble account!
		Please click the following link to verify your account: {}
		
		Thanks,
		
		Bubble Team
		""".format(username,verification_link)
		html = """
		<html>
		<body>
			<p>Congraduations {} for making a Bubble account!<br><br>
			Please click the following link to verify your account: <a href="{}">Verify Account</a><br><br>
			Thanks,<br><br>
			Bubble Team
			</p>
		</body>
		</html>
		""".format(username,verification_link)
		
		part1 = MIMEText(text, "plain")
		part2 = MIMEText(html, "html")
		
		msg.attach(part1)
		msg.attach(part2)
		
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(self.config['email'], self.config['password'])

			smtp.send_message(msg)