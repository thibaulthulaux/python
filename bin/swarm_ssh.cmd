@echo off
SET DOCKERHOST="swarm-manager"
%CD%/app/src/main/bin/docker-machine-Windows-0.16.2x86_64.exe ssh %DOCKERHOST%