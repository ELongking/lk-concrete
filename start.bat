@echo off

start cmd /k "D:/Redis/Redis-x64-5.0.14.1/redis-server.exe D:/Redis/Redis-x64-5.0.14.1/redis.windows.conf"

start cmd /k "D:/MongoSh/mongosh.exe --authenticationDatabase concreteDetails -u longking -p 19980917"
