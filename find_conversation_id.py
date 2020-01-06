from skpy import Skype, SkypeChats

# Run this to get recent messages, consequently conversation ids
sk = Skype("nishizuka23", "curioso")
skc = SkypeChats(sk)
skc.recent()
