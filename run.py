import srp

# Consider enabling RFC5054 compatibility for interoperation with non pysrp SRP-6a implementations
#pysrp.rfc5054_enable()

# The salt and verifier returned from srp.create_salted_verification_key() should be
# stored on the server.
salt, vkey = srp.create_salted_verification_key( 'testuser', 'testpassword' )

class AuthenticationFailed (Exception):
    pass

# ~~~ Begin Authentication ~~~

usr      = srp.User( 'testuser', 'testpassword' )
uname, A = usr.start_authentication()

# The authentication process can fail at each step from this
# point on. To comply with the SRP protocol, the authentication
# process should be aborted on the first failure.

# Client => Server: username, A
svr      = srp.Verifier( uname, salt, vkey, A )
s,B      = svr.get_challenge()

if s is None or B is None:
    raise AuthenticationFailed()

# Server => Client: s, B
M        = usr.process_challenge( s, B )

if M is None:
    raise AuthenticationFailed()

# Client => Server: M
HAMK     = svr.verify_session( M )

if HAMK is None:
    raise AuthenticationFailed()

# Server => Client: HAMK
usr.verify_session( HAMK )

# At this point the authentication process is complete.

assert usr.authenticated()
assert svr.authenticated()
