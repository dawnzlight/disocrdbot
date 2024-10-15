@echo off
setlocal

REM DriverをPostsgreSQLに指定
set GOOSE_DRIVER=postgres
set GOOSE_DBSTRING=host=localhost port=5432 user=sakura password=password dbname=discordbot-development

cd ./migrations

if "%1" == "up" (
    echo goose %GOOSE_DRIVER% %GOOSE_DBSTRING% up
    goose up
) else if "%1" == "down" (
    goose %GOOSE_DRIVER% %GOOSE_DBSTRING% down
) else if "%1" == "create" (
    if "%2" == "" (
        echo Invalid command. Use "up", "down", or "create".
    ) else (
        goose create %2 sql
    )
) else (
    echo Invalid command. Use "up", "down", or "create".
)

cd ..

endlocal