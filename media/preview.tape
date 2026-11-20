# From the repository root: vhs media/preview.tape
Output media/preview.gif

Set Shell bash
Set Theme "Dracula"
Set FontSize 21
Set Width 960
Set Height 310
Set Padding 20
Set Framerate 15
Set TypingSpeed 34ms
Set CursorBlink false
Set LoopOffset 81%

Env PYTHONPATH "src"
Env FORCE_COLOR "3"
Env PYTHON_BASIC_REPL "1"
Env PYTHONSTARTUP "/dev/null"
Env PYTHON_HISTORY "/dev/null"

Type "python3 -q"
Enter
Sleep 500ms
Type "import coloredstrings as cs"
Enter
Type "print(cs.green('PASS'), 'test_read_config')"
Enter
Sleep 650ms
Type "print(cs.white.on.red.bold(' FAIL '), 'test_missing_key')"
Enter
Sleep 650ms
Type "key = cs.yellow('port')"
Enter
Type "print(cs.dim(f'  expected {key} in server.toml'))"
Enter
Sleep 3s
