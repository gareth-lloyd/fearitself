from models import *

dailymail = NewsSource(id=1, name="Daily Mail", feed="http%3A%2F%2Fwww.dailymail.co.uk%2Fnews%2Findex.rss")
dailymail.save()

standard = NewsSource(id=2, name="Evening Standard", feed="http%3A%2F%2Fwww.thisislondon.co.uk%2Fstandard-home%2Frss%2F%3Fito%3D1588")
standard.save()

dailystar = NewsSource(id=3, name="Daily Star", feed="http%3A%2F%2Fwww.dailystar.co.uk%2Frss%2F1%2Fnews%2F")
dailystar.save()

mirror = NewsSource(id=4, name="Mirror", feed="http%3A%2F%2Fwww.mirror.co.uk%2Fnews%2Frss.xml")
mirror.save()

telegraph = NewsSource(id=5, name="Telegraph", feed="http%3A%2F%2Fwww.telegraph.co.uk%2Fnews%2Frss")
telegraph.save()

express = NewsSource(id=6, name="Express", feed="http%3A%2F%2Fwww.express.co.uk%2Frss%2Fuknews.xml")
express.save()

sun = NewsSource(id=7, name="Sun", feed="http%3A%2F%2Fwww.thesun.co.uk%2Fsol%2Fhomepage%2Ffeeds%2Frss%2Farticle312900.ece")
sun.save()

guardian = NewsSource(id=8, name="Guardian", feed="http%3A%2F%2Fwww.guardian.co.uk%2Frssfeed%2F0%2C%2C1%2C00.xml")
guardian.save()

sources = [dailymail, standard, dailystar, mirror, telegraph, express, sun, guardian]