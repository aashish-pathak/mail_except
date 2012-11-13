import logging
from logging.handlers import SMTPHandler

""" Example smtp_host `smtp.gmail.com` """
SMTP_HOST      = ""
""" Example mail id `web@web.com` """
SMTP_USER_NAME = ""
""" Password for web@web.com """
SMTP_PASSWORD  = ""
""" From addresses / aliases if you want to use """
FROM_ADDR      = ""
""" Receiver email id's. You can provide multiple email addresses in an array """
TO_ADDR  = []
""" Subject line of an email """
SUBJECT        = ""

""" Override get_emit of SMTPHandler """
def get_emit():
   def emit(self, record):
      """
      Emit a record.
      Format the record and send it to the specified addressees.
      """
      try:
         import smtplib
         import string
         try:
            from email.utils import formatdate
         except ImportError:
            formatdate = self.date_time
         port = self.mailport
         if not port:
            port = smtplib.SMTP_PORT
         smtp = smtplib.SMTP(self.mailhost, port)        
         msg = self.format(record)
         import socket, os, pprint
         """ Using socket.gethostname() assuming hostname itself it fqdn for the machine. """
         msg = "%s\r\n\r\n------------------------------\r\nException occured on : \r\n-----------------------------\r\n%s" % (msg, socket.gethostname())
         msg = "%s\r\n\r\n------------------------------\r\nEnvironment\r\n-----------------------------\r\n%s" % (msg, pprint.pformat(dict(os.environ)))
         msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (self.fromaddr, string.join(self.toaddrs, ","), self.getSubject(record), formatdate(), msg)
         print "Mailhost: " + self.mailhost+" From: " +self.fromaddr +" To: " + str(self.toaddrs) +" User: " +self.username +" Password: " +self.password
         if self.username:
            smtp.starttls()
            smtp.login(self.username, self.password)
         smtp.sendmail(self.fromaddr, self.toaddrs, msg)
         print "DONE"
         smtp.quit()
      except (KeboardInterrupt, SystemExit):
         print "EXIT"
         raise
      except:
         print "ERROR"
         self.handleError(record)
   return emit
 
def init (smtp_host, smtp_username, smtp_password, from_addr, to_addr, subject):
  """ Initiate mail exception logger """  
  import socket
  import sys
  global SMTP_HOST, SMTP_USER_NAME, SMTP_PASSWORD, FROM_ADDR, TO_ADDR, SUBJECT
  
  SMTP_HOST      =    smtp_host      if 'smtp_host' in locals() else None
  SMTP_USER_NAME =    smtp_username  if 'smtp_username' in locals() else None
  SMTP_PASSWORD  =    smtp_password  if 'smtp_password' in locals() else None
  FROM_ADDR      =    from_addr      if 'from_addr' in locals() else None
  TO_ADDR        =    to_addr        if 'to_addr' in locals() else None
  SUBJECT        =    "[%s] %s" % (subject, socket.gethostname()) if 'subject' in locals() else None

  try:
    SMTPHandler.emit = get_emit()
    mail_logger = logging.getLogger("mail_logger")
    
    smtp_handler = logging.handlers.SMTPHandler(mailhost=(SMTP_HOST, 25), fromaddr=FROM_ADDR, toaddrs=TO_ADDR, subject=SUBJECT,credentials=(SMTP_USER_NAME, SMTP_PASSWORD))
    smtp_handler.setLevel(logging.ERROR)
    mail_logger.addHandler(smtp_handler)
    return mail_logger
  except Exception as e:
    print "Some error in initializing mail logger."
    print str(e)
    sys.exit(1)

if __name__ == "__main__":
  """ Initiate logger """
  init()