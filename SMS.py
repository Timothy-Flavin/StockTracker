import smtplib
carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

def send(message, number, usr, pswrd):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
  to_number = str(number)+carriers['att']
  print(to_number)
  auth = (usr, pswrd)

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
  try:
        
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail( auth[0], to_number, message)
  except ValueError:
    print(ValueError)
    print("Was unable to send message, but the stock data should still have been reported in the terminal")
	# Send text message through SMS gateway of destination number
	