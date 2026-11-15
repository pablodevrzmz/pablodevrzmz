# Records assets/strands-acp-client.gif with vhs (https://github.com/charmbracelet/vhs).
#   cd site/profile/demos && vhs strands-acp-client.tape
# The run is live: the Strands agent calls its model and Claude Code reads demos/sample.

Output ../assets/strands-acp-client.gif

Set Shell zsh
Set FontSize 16
Set Width 1200
Set Height 640
Set Padding 24
Set TypingSpeed 40ms
Set PlaybackSpeed 2.0
Set Theme "GitHub Dark"

Hide
Type "PROMPT='$ ' && clear" Enter
Show

Type "cat sample/retry.py" Enter
Sleep 2s
Type "python acp_demo.py" Enter
Wait@180s /\$\s*$/
Sleep 4s
