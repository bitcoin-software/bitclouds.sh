from jsonrpc import ServiceProxy

access = ServiceProxy("http://ae059511:8s5r2X_EwFBrg1l6GMQvFfn2cqXFE73ud7MpPVZUx7I=@rpc.bitbsd.org:8332")
print(access.getinfo())
