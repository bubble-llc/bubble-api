import smtplib
import yaml
import dkim
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
	
	def send_email_validation(self, username, email, verificaiton_code):
		
		# verification_link = "http://0.0.0.0:8000/email_validation?email={}&validation_code={}".format(email,verificaiton_code)
		verification_link = "https://bubblemedia.info/email_validation?email={}&validation_code={}".format(email,verificaiton_code)
		print(verification_link)
		msg = MIMEMultipart("alternative")
		msg['Subject'] = "Bubble Email Validation"
		msg['From'] = "Bubble Support <{}>".format(self.config['email'])
		msg['To'] = email
		
		
		text = """
		Congratulations {} for making a Bubble account!
		Please click the following link to verify your account: {}
		
		Thanks,
		
		Bubble Team
		""".format(username,verification_link)
		html = """
		<html>
		<body>
			<p>Congratulations {} for making a Bubble account!<br><br>
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

	def send_password_recovery(self, email, username, verificaiton_code):
		msg = MIMEMultipart("alternative")
		msg['Subject'] = "Bubble Password Recovery"
		msg['From'] = "Bubble Support <{}>".format(self.config['email'])
		msg['To'] = email
		
		
		text = """
		{}, 
		Please use the validation code below to recovery your password.
		Password Recovery Code: {}
		
		Thanks,
		
		Bubble Team
		""".format(username,verificaiton_code)
		html = """
		<html>
		<body>
			<p>{},<br><br>
			Please use the validation code below to recovery your password.<br><br>
			Password Recovery Code: {}<br><br>
			Thanks,<br><br>
			Bubble Team
			</p>
		</body>
		</html>
		""".format(username,verificaiton_code)
		
		part1 = MIMEText(text, "plain")
		part2 = MIMEText(html, "html")
		
		msg.attach(part1)
		msg.attach(part2)
		
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(self.config['email'], self.config['password'])

			with open("/Users/steventran/bubblemedia.info.20210719.pem") as fh:
				dkim_private_key = fh.read()
			headers = [b"To", b"From", b"Subject"]
			sig = dkim.sign(
				message=msg.as_bytes(),
				selector=str("20210719").encode(),
				domain="bubblemedia.info".encode(),
				privkey=dkim_private_key.encode(),
				include_headers=headers,
			)
			# add the dkim signature to the email message headers.
			# decode the signature back to string_type because later on
			# the call to msg.as_string() performs it's own bytes encoding...
			msg["DKIM-Signature"] = sig[len("DKIM-Signature: "):].decode()
			smtp.send_message(msg)