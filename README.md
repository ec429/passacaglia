Passacaglia
===========

A zero-storage password manager.
--------------------------------

Most password manager software works by keeping an encrypted database of
passwords, either on local disk or 'in the cloud' on a remote server (often,
though not always, run by the promoter of the software).

**Passacaglia is different.**

Passacaglia relies entirely on _passphrase-based password derivation_.  This
uses the mathematical technique of password-based key derivation (PBKDF) to
combine a _single global passphrase_ with a _per-account identifier_
(typically the name or domain-name of the website on which the account
resides) as inputs to a hashing- and key-stretching function (specifically,
PKCS#5 PBKDF2 HMAC with SHA-256), to generate a _per-account password_.

Advantages
----------

The big advantage of the Passacaglia design is that there is no password
database.  This means there is nothing to keep synchronised between multiple
devices (or store on a remote server); no motherlode of encrypted passwords
to potentially get compromised by an attacker who can then try to crack it
at their leisure.  Instead, only the few passwords for sites that get
individually compromised are potentially available to the attacker, vastly
reducing the data available to try to crack your pass-phrase.

As well as the security advantages, this is also good for usability: if you
need to log in on a brand new device, all you need to do is install the
software and type in your passphrase; no need to transfer a database across.

Disadvantages
-------------

Of course there is a downside as well: your passphrase is now a single point
of failure (unless you use a per-user salt; see comments in generate()), so
if an attacker steals or guesses your passphrase, they can calculate all of
your passwords (at least if they know what name you used for each site).

If, for instance, SHA-256 gets broken _really badly_, an attacker might be
able, working from a single (site, password) combination, to work backwards
to calculate the passphrase you used.  (This can be somewhat mitigated by
using a _really good_ passphrase and not-too-long per-account passwords: if
the passphrase has more entropy than the password then it can't be uniquely
reconstructed even with unbounded computation, as password generation is not
injective.  But if an attacker collects multiple passwords generated from
the same passphrase, he can overcome this hurdle.)

And of course there are endless ways of accidentally releasing a passphrase
into the wild (from writing it down and losing the piece of paper, to having
your fingers watched by a shoulder-surfing attacker, to using a keyboard
bugged by the NSA).  This last suggests a usage model that avoids typing the
passphrase too often; see the next section.

Hybrid Usage
------------

Instead of running Passacaglia every time you log in, it may be best to use
it _in conjunction with_ the password-storage features of your browser, or
some other conventional local-storage password manager.
That is, at least when running on a trusted system, only run Passacaglia
once per account per device, to populate the locally saved password.  The
job of Passacaglia (and your passphrase!) is then confined to allowing you
to, in effect, carry around your entire password database in your head.

The downside of this model is, of course, that the local storage is now an
attack vector, losing the security advantages of Passacaglia.  One possible
response is to only save _some_ passwords locally (those for frequently-
accessed or low-value accounts), while sticking to the pure-Passacaglia
model for more sensitive credentials.  The choice of which passwords to save
could even be varied per-device, bearing in mind that (e.g.) your smartphone
is a lot more vulnerable than your home desktop PC.

Dependencies
------------

Passacaglia requires Python; it will run on both Python 2.7 and Python 3.6.
All library functions used come from the Python Standard Library.
