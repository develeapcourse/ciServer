
import sys
import smtplib


try:
	msg = sys.argv[1]
except Exception as e:
	print("argument is missing.")
	print(e)
	exit(1)


sender = 'develeapcourse@gmail.com'

dist_list = ['orlykul@gmail.com',
			'lonnychetrit@gmail.com',
			'Bittanraphael@gmail.com',
			'zvitam@hotmail.com',
			'michael.52@msn.com',
			'adam.promo@gmail.com',
			'danny.konstadt@gmail.com',
			'moria8035@gmail.com']


try:
   server = smtplib.SMTP("smtp.gmail.com", 587)
   server.connect("smtp.gmail.com", 587)
   print(1)
   server.ehlo()
   server.starttls()
   print(2)
   server.login(sender, 'deve1234')
   print(3)
   print ("Successfully sent email")
except Exception as e:
   print ("Error: unable to send email")
   print(e)
   exit(1)

server.sendmail(sender, dist_list, msg)

