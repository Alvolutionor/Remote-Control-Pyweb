 @echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
REM
start /b ./ding -config=./ding.cfg -subdomain=timedemo 8080
