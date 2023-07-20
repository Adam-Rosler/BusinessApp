import imaplib
import gspread

class EmailFetcher():

    def __init__(self):
       self.imap = ""
       self.initializeImap()

    def initializeImap(self):
        user = ""
        password = ""
        imap_url = "imap.gmail.com"
        imap = imaplib.IMAP4_SSL(imap_url)
        imap.login(user,password)
        imap.select('INBOX')
        self.imap = imap


        

    def searchEmail(self, trackingNumber):
        # Check the email headers for the tracking number
        query = f'X-GM-RAW "{trackingNumber}"'
        _, searchResults = self.imap.uid('search', query)
        
        # Combine all matching emails into one string
        emailCombined = ''
        for emailUid in searchResults[0].split():
            _, emailData = self.imap.uid('fetch', emailUid, '(RFC822)')
            emailRaw = emailData[0][1].decode('utf-8')
            emailCombined += emailRaw.strip()
        
        return emailCombined.upper()

