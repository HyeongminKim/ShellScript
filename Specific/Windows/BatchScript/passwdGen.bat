@ECHO OFF

echo Please wait until passwdGen.jar is running...
cd /D e:%HOMEPATH%\Dev\Java\workspace\PasswordsGenerator\src

echo.
echo NOTE: This window closes automatically when the passwdGen.jar exits.

java -jar -Dfile.encoding=ms949 passwdGen.jar

exit
