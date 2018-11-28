
import sys
import smtplib

def send(dist_list, subject, msg):

	if dist_list is None or msg is None:
		print("argument is missing.")
		print(e)
		exit(1)

	dist_list = dist_list.split()
	sender = 'develeapcourse@gmail.com'

	#send email
	print("conecting gmail...")
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.connect("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(sender, 'deve1234')
		print("sending..")
		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail(sender, dist_list, message)
		print ("Successfully sent email")
	except Exception as e:
	   print ("Error: unable to send email")
	   print(e)