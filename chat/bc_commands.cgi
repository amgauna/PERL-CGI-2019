#!/usr/bin/perl

# The channels.
# For a single channel chat, comment out all the channels.
# Or add channels if you want.
$channels[0] = 'General';
$channels[1] = 'Adult';
$channels[2] = 'Teen';

my $thechannels = '';

if (@channels) {
$thechannels = "Channel<br>\n";
$thechannels .= "<select name=\"Channel\" size=\"1\" onchange=\"javascript:ChangeChannel();\">\n";
  my $xyz = 0;
  foreach $channel (@channels) {
   if (!$xyz++) {$thechannels .= '<option selected value="' . $channel . '">' . $channel . "</option>\n";}
   else {$thechannels .= '<option value="' . $channel . '">' . $channel . "</option>\n";}  
  }
$thechannels .= "</select>\n";
}

print "Content-type: text/html\n\n";

print <<COMMANDWINDOW;
<html><head>
<script LANGUAGE="javascript"><!--
 function LogOff() {
     if (!(parent.window.confirm("Are you SURE you want to Log Off now?"))) { return; }
     parent.sendchat.document.forms[0].message.value = '.me just logged off.';
     parent.sendchat.document.forms[0].submit();
	 document.write('<html><body><center><p>Logging you off<br>Please wait</p><p>This window will close in 3 seconds</p></center></body></html>');
     setTimeout('parent.window.close();',3000); 
}
function IC(col){
  parent.sendchat.document.forms[0].chat_input.value += '`' + col;
  parent.sendchat.document.forms[0].chat_input.focus();
return;
}
function SendAction(){
var MyAction;
MyAction = window.prompt('Send a Generic Action to Chat.', '');
if (!MyAction) {return;}
parent.sendchat.document.forms[0].message.value = '.me ' + MyAction;
parent.sendchat.document.forms[0].submit();
return;
}
function ChangeChannel(){
var chan;
chan = document.forms[0].Channel.options[document.forms[0].Channel.selectedIndex].text;
parent.sendchat.document.forms[0].room.value = chan;
parent.sendchat.document.forms[0].message.value = '.me just entered this channel.';
parent.sendchat.document.forms[0].submit();
return;
}
//--></script>
</head>
<body BGCOLOR="#F0F0F0" TEXT="#000000" LINK="#0000FF" VLINK="#0000FF" ALINK="#FF0000">
<form>
<center><p><input type="button" value="&nbsp;&nbsp;Log Off&nbsp;&nbsp;" onclick="javascript:LogOff();"><br>
<input type="button" value="Send Action" onclick="javascript:SendAction();">
</p>

<p><small><strong><font color="#0000A8">Color Codes</font></strong></small>
<span  ID="MySpan">
<table border="0" cellpadding="0">
  <tr>
    <a href="javascript:IC(1)"><td width="22" height="12" bgcolor="#0000A8" align="center"><font color="#FFFFFF"><strong><small>`1</small></strong></font></td></a>
    <a href="javascript:IC(2)"><td width="22" height="12" bgcolor="#007000" align="center"><font color="#FFFFFF"><strong><small>`2</small></strong></font></td></a>
    <a href="javascript:IC(3)"><td width="22" height="12" bgcolor="#008080" align="center"><font color="#FFFFFF"><strong><small>`3</small></strong></font></td></a>
    <a href="javascript:IC(4)"><td width="22" height="12" bgcolor="#A80000" align="center"><font color="#FFFFFF"><strong><small>`4</small></strong></font></td></a>
    <a href="javascript:IC(5)"><td width="22" height="12" bgcolor="#A800A8" align="center"><font color="#FFFFFF"><strong><small>`5</small></strong></font></td></a>
  </tr>
  <tr>
    <a href="javascript:IC(6)"><td width="22" height="12" bgcolor="#A85400" align="center"><font color="#FFFFFF"><strong><small>`6</small></strong></font></td></a>
    <a href="javascript:IC(7)"><td width="22" height="12" bgcolor="#808080" align="center"><font color="#FFFFFF"><strong><small>`7</small></strong></font></td></a>
    <a href="javascript:IC(8)"><td width="22" height="12" bgcolor="#505050" align="center"><font color="#FFFFFF"><strong><small>`8</small></strong></font></td></a>
    <a href="javascript:IC(9)"><td width="22" height="12" bgcolor="#5454FC" align="center"><font color="#FFFFFF"><strong><small>`9</small></strong></font></td></a>
    <a href="javascript:IC(0)"><td width="22" height="12" bgcolor="#00B000" align="center"><font color="#FFFFFF"><strong><small>`0</small></strong></font></td></a>
  </tr>
  <tr>
    <a href="javascript:IC('!')"><td width="22" height="12" bgcolor="#00A0A0" align="center"><font color="#FFFFFF"><strong><small>`!</small></strong></font></td></a>
    <a href="javascript:IC('\@')"><td width="22" height="12" bgcolor="#FC5454" align="center"><font color="#FFFFFF"><strong><small>`\@</small></strong></font></td></a>
    <a href="javascript:IC('\#')"><td width="22" height="12" bgcolor="#FC54FC" align="center"><font color="#FFFFFF"><strong><small>`\#</small></strong></font></td></a>
    <a href="javascript:IC('\$')"><td width="22" height="12" bgcolor="#AAAA00" align="center"><font color="#FFFFFF"><strong><small>`\$</small></strong></font></td></a>
    <a href="javascript:IC('\%')"><td width="22" height="12" bgcolor="#000000" align="center"><font color="#FFFFFF"><strong><small>`\%</small></strong></font></td></a>
  </tr>
</table></span></p>
<SCRIPT LANGUAGE="JavaScript"><!--
if (document.all) {document.all("MySpan").style.cursor = 'hand';}
//--></SCRIPT>

<p>$thechannels</p>

</center></form>
</body></html>
COMMANDWINDOW
exit;