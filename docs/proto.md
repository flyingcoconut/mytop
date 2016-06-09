#mytop#

##Protocole##
mytop protocol is json based

S: Server (plugin)
C: client

C: {"method": "status", "params": {}}
S: {"result": "unconfigured"}

##Errors##

##Methods##

###setconfigs###

C: {"method": "setconfigs", "params": {"configs": {"host": "localhost"}}}
S: {"result": null}



###getconfigs###

Parameters

- configs

###init###

Parameters

- None

eg.

C: {"method": "init", "params": {} }
S: {"result": null}

###term###

Parameters

- None

eg.

C: {"method": "term", "params": {} }
S: {"result": null}


###status###

Liste of methods

- term
