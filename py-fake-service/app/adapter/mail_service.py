import os
import mailbox


class MailService:
    MAILSET_PATH = os.join(os.environ('HOME'), 'mailset', 'mediumtagged'))

    def __init__(self):
        self.mails = MailSet()

    def load_mailset(self):
        mbox_filenames = [filename for filename in os.listdir(MAILSET_PATH) if mbox.startswith('mbox')]
        boxes = (mailbox.mbox(os.path.join(MAILSET_PATH, mbox)) for mbox in mbox_filenames) 

        for box in boxes:
            message = box.popitem()
            self.mails.add(message[1])

        
