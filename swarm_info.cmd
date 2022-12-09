@echo off
SET DOCKERHOST="swarm-manager"
SET CMDLINE="echo --- MANAGER IP && ip addr | grep eth1 | grep inet && echo --- NODE && docker node ls && echo --- STACK && docker stack ls && echo --- SERVICE && docker service ls && echo --- IMAGE && docker image ls && echo --- NETWORK  && docker network ls && echo --- VOLUME && docker volume ls"
:loop
cls
%CD%/app/src/main/bin/docker-machine-Windows-0.16.2x86_64.exe ssh %DOCKERHOST% %CMDLINE%
timeout /t 5 /nobreak
goto loop