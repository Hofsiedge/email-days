import getpass, imaplib, time

IMAP_SERVER = 'imap.yandex.ru'
IMAP_PORT = 993

# Compute sum of (unread email sending date) * (days being unread)
def compute_email_days(login: str, password: str) -> float:
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as M:
        M.login(login, password)
        M.select('INBOX', readonly=True)
        typ, msgnums = M.search(None, 'UNSEEN')
        if typ != 'OK':
            print(f'Something went wrong: received typ={typ}')
            return

        inbox_len = len(msgnums[0].split())
        print(f'Unread messages: {inbox_len}')

        current_time = time.time()
        DAY = 60 * 60 * 24
        email_days = 0

        # M.fetch takes limited number of messages, so email number list is split in chunks
        pack_start = 0
        PACK_SIZE = 1000

        while pack_start < inbox_len:
            typ, data = M.fetch(
                b','.join(msgnums[0].split()[pack_start : pack_start + PACK_SIZE]),
                'INTERNALDATE',
            )
            for i, datestring in enumerate(data):
                email_days += (current_time - time.mktime(imaplib.Internaldate2tuple(datestring))) / DAY

            pack_start += PACK_SIZE

        return email_days


if __name__ == '__main__':
    login, password = input('Login: '), getpass.getpass('Password: ')
    print(compute_email_days(login, password))

