
import sys
import smtplib

# get arguments
try:
	dist_list = sys.argv[1]
	msg = sys.argv[2]
except Exception as e:
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
	server.sendmail(sender, dist_list, msg)
	print ("Successfully sent email")
except Exception as e:
   print ("Error: unable to send email")
   print(e)