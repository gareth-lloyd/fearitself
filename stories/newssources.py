from models import *

dailymail = NewsSource(id=1, name="Daily Mail", feed="http%3A%2F%2Fwww.dailymail.co.uk%2Fnews%2Findex.rss")
dailymail.save()

standard = NewsSource(id=2, name="Evening Standard", feed="http%3A%2F%2Fwww.thisislondon.co.uk%2Fstandard-home%2Frss%2F%3Fito%3D1588")
standard.save()

dailystar = NewsSource(id=3, name="Daily Star", feed="http%3A%2F%2Fwww.dailystar.co.uk%2Frss%2F1%2Fnews%2F")
dailystar.save()

sources = [dailymail, standard, dailystar]