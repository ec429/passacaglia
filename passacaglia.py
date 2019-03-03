#!/usr/bin/python
import argparse
import base64
import getpass
import hashlib

def mince(*args):
    l = max(len(s) for s in args)
    ing = [list(s) + [''] * (l - len(s)) for s in args]
    return ''.join(''.join(part) for part in zip(*ing))

def generate(site, phrase, mxl=12):
    # Why mince, when the pbkdf will mix them together anyway?
    # Well, it's just an extra way of making life that little bit harder for
    # rainbow tables -- a table of pbkdf(site + phrase) is more likely to be
    # work shared with attacks on other software.
    meat = mince(site, phrase)
    # This is a fixed salt.  Aren't those bad?  Well yes, _when used in a
    # password database_.  But we're not using it for that purpose, but simply
    # to make existing rainbow tables inapplicable.  The only practical way to
    # vary it would be per-user, making it a pepper (users could, if they want
    # to be extra secure, change the salt in their copy of passacaglia); but
    # (a) that would mean changing it on every device they run passacaglia
    # (b) at that point it's just another passphrase.
    # If you want to use your whole device as a hardware token, or perhaps run
    # passacaglia _on_ a hardware token device, you could replace this salt
    # with some long random bit-string.
    salt = b'Pcaglia muritic natrum'
    # The arbitrariness of the number of rounds is another way to avoid work-
    # sharing.
    stew = hashlib.pbkdf2_hmac('sha256', meat.encode("utf8"), salt, 333429)
    return base64.b64encode(stew)[:mxl]

def main(site=None, quiet=False, **kwargs):
    if site is None:
        site = raw_input("" if quiet else "Site name: ")
    phrase = getpass.getpass("" if quiet else "Passphrase: ")
    pw = generate(site, phrase, **kwargs)
    if quiet:
        print(pw)
    else:
        print("Your password is: " + pw.decode("utf8"))

def parse_opts():
    parser = argparse.ArgumentParser(description='Generate (or regenerate) password for a site.')
    # "Maximum" length?  Well, if you put something huge here you'll run out of
    # bits in the output of the hash function.  Currently the limit is 32.
    parser.add_argument('-l', '--len', type=int, help='Maximum length of password to generate.', default=12)
    parser.add_argument('-s', '--site', type=str, help='Name of site to generate password for.', default=None)
    # For use in scripts, etc.
    parser.add_argument('-q', '--quiet', action='store_true', help='Output nothing but the password.')
    # Why no argument to specify the passphrase?  Because we don't want it to
    # ever appear in someone's .bash_history; it should only ever come through
    # stdin (which it is up to the user to properly secure).
    return parser.parse_args()

if __name__ == '__main__':
    opts = parse_opts()
    main(site=opts.site, mxl=opts.len, quiet=opts.quiet)
