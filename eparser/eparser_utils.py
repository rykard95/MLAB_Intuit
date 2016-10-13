import os
import re

def fileList(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if filename.endswith(('.eml')):
                matches.append(os.path.join(root, filename))

    if len(matches) == 0:
        print("INVALID FILE PATH")

    return matches

def pullout (m):
    """Extracts content from an e-mail message.
    This works for multipart and nested multipart messages too.
    m   -- email.Message() or mailbox.Message()
    Returns tuple(Text, Html, Files, Length)
    Text  -- All text from all parts.
    Html  -- All HTMLs from all parts
    Files -- Dictionary mapping extracted file to message ID it belongs to.
    Length -- Chain length.
    """
    Html = ""
    Text = ""
    Files = {}
    Length = 0
    if not m.is_multipart():
        if m.get_filename(): # It's an attachment
            return Text, Html, Files, 1
        # Not an attachment!
        # See where this belongs. Text, Html or some other data:
        cp = m.get_content_type()
        if cp=="text/plain": Text += str(m.get_payload(decode=True))
        elif cp=="text/html": Html += str(m.get_payload(decode=True))
        else:
            # Something else!
            # Extract a message ID and a file name if there is one:
            # This is some packed file and name is contained in content-type header
            # instead of content-disposition header explicitly
            return Text, Html, Files, 1
    # This IS a multipart message.
    # So, we iterate over it and call pullout() recursively for each part.
    y = 0
    while 1:
        # If we cannot get the payload, it means we hit the end:
        try:
            pl = m.get_payload(y)
        except: break
        # pl is a new Message object which goes back to pullout
        t, h, f, p = pullout(pl)
        Text += t; Html += h; Files.update(f); Length += p
        y += 1
    return Text, Html, Files, Length

def extract (msgfile):
    """Extracts all data from e-mail, including From, To, etc., and returns it as a dictionary.
    """
    Text, Html, Files, Length = pullout(msgfile)
    Text = Text.strip(); Html = Html.strip()
    Text = re.sub('<[^<]+?>', '', Text)
    return Text, Html, Files, Length
