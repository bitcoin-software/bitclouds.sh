from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

access = AuthServiceProxy("http://ae059511:8s5r2X_EwFBrg1l6GMQvFfn2cqXFE73ud7MpPVZUx7I=@rpc.bitbsd.org:8332")
print(access.gettransaction('cc53e04e47ff4cd52cf1855a0dac7ac764c3ae3d23f3059e034515895967f3db'))
