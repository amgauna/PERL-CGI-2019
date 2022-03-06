#!/usr/bin/perl

######### Begin optional setup ###########

# Will be displayed in login screen
$yourname = 'BlueChat';
# color of title on login screen
$titlecolor = '#800000';

# Rules are shown on login screen.
# add or delete as necessary. $rules[0], $rules[1], and so on.
$rules[0] = '1. Keep all foul language and sexual content in the Adult Channel.';
$rules[1] = '2. No Flaming allowed in any channel.';

# Image for background of login screen
$backgroundimage = '';

# Background color of login screen
$backgroundcolor = '#F0F0F0';

# Text color of login screen
$textcolor = '#000000';

# link color of login screen
$linkcolor = '#0000FF';

# Visited link color of login screen
$visitedcolor = '#0000FF';

# Active link color of login screen
$activecolor = '#FF0000';

# Any additional things you want added to
# the bottom of the login screen.
$additional = '<p><small><I><a href="javascript:history.back();">Go Back</a></small></I></p>';
# $additional .= 'You can add more stuff here.';
# $additional .= 'just uncomment these lines';

######### End Setup #############

&Parse_Form;

if (!$formdata{'cname'}) {
if ($backgroundimage ne '') {
  $backgroundimage = 'background="' . $backgroundimage . '"';
}
foreach $rule (@rules) {
 $TheRules .= $rule . '<br>';
}

&Mime;
print <<ENDHTML;
<html>
<head>
<title>$yourname</title>
<script language="JavaScript"><!--
function LogIn(){
var MyWindow;
var MyUrl;
if (!document.forms[0].cname.value) {alert('You need to enter a name to use'); return;}
MyUrl = 'bluechat.cgi' + '?cname=' + escape(document.forms[0].cname.value);
MyWindow = window.open(MyUrl, "BlueChat", "STATUS=NO,TOOLBAR=NO,LOCATION=NO,DIRECTORIES=NO,COPYHISTORY=NO,MENU=NO,RESISABLE=NO,SCROLLBARS=NO,TOP=50,LEFT=20,WIDTH=600,HEIGHT=400");
window.history.back();
}
// --></script>
</head>
<body bgcolor="$backgroundcolor" text="$textcolor" link="$linkcolor" vlink="$visitedcolor" alink="$activecolor" $backgroundimage>
<p align="center"><font color="$titlecolor"><strong><big><big>Welcome to $yourname</big></big></strong></font></p>
<p>$TheRules</p>
<form onsubmit="javascript:{return false;}">
  <div align="center"><center><p>Enter a name to use while chatting<br>
  <input type="text" name="cname" size="20"><br>
  <input type="button" value="Login" onclick="javascript:LogIn();"></p>
  </center></div>
</form>
<p align="center"><small>Color Codes Allowed in name:<br>
<strong><font color="#0000A8">`1</font> <font color="#007000">`2</font> <font
color="#008080">`3</font> <font color="#A80000">`4</font> <font color="#A800A8">`5</font> <font
color="#A85400">`6</font> <font color="#808080">`7</font> <font color="#505050">`8</font> <font
color="#5454FC">`9</font> <font color="#00B000">`0</font> <font color="#00A0A0">`!</font> <font
color="#FC5454">`\@</font> <font color="#FC54FC">`\#</font> <font color="#AAAA00">`\$</font> <font
color="#000000">`\%</font></strong><br>
<I>Example:</I> `1James = <font color="#0000A8">James</font></small></p>
<p>$additional</p>
<p><em><small>Version 2.4</small></em></p>
</body></html>
ENDHTML
exit;
}

if ($formdata{'cname'}){
my $cname = $formdata{'cname'};
$cname =~ s/\`\#/`A/g;
$cname =~ s/\#//g;
$cname =~ s/ /\%20/g;

&Mime;
print <<MAINHTML;
<html><head>
<title>$yourname Chat</title>
</head>
<frameset cols="150,*">
  <frameset rows="150,*">
    <frame name="logo" scrolling="no" noresize src="bc_logo.cgi">
    <frame name="commands" scrolling="no" noresize src="bc_commands.cgi?cname=$cname">
  </frameset>
  <frameset rows="*,40">
    <frame name="main" scrolling="auto" noresize src="bc_chat.cgi?cname=$cname&room=general&message=.me%20just%20entered%20this%20channel">
    <frame name="sendchat" target="main" scrolling="no" noresize src="bc_chatbar.cgi?cname=$cname" marginwidth="5" marginheight="5">
  </frameset>
  <noframes>
  <body>
  <p>This page uses frames, but your browser doesn't support them.</p>
  </body>
  </noframes></frameset></html>
MAINHTML
exit;
}

&Mime;
print <<ERRORHTML;
<html><head><title>Error</title></head><body>
<p><font color="#800000"><big><strong>BlueSparks Chat</strong></big></font></p>
<p>There was an error trying to run BlueSparks Chat script.</p>
</body></html>
ERRORHTML
exit;

# Parses the form
sub Parse_Form {
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
   @pairs = split(/&/, $ENV{'QUERY_STRING'});
} elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
      read (STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
      @pairs = split(/&/, $buffer);

        if ($ENV{'QUERY_STRING'}) {
          @getpairs = split(/&/, $ENV{'QUERY_STRING'});
          push(@pairs, @getpairs);
        }
} else {
    &ErrorMessage("Must use Post or Get.");
  }

foreach $pair (@pairs) {
  ($key, $value) = split(/=/, $pair);
  $key =~ tr/+/ /;
  $key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

  $value =~ s/<!--(.|\n)*-->//g;

if ($formdata{$key}) {
  $formdata{$key} .= ", $value";
} else {
  $formdata{$key} = $value;
  }
}
}

# Standard little error message routine
sub ErrorMessage
{
   my $msg = shift;
   print "Content-type: text/html\n\n$msg";
   exit;
}

# Prints a html file to the screen
sub Print_Htm {
 open(MYFILE, "<$_[0]") || &ErrorMessage("$_[0] not found in html directory");
 &Mime;
 print while <MYFILE>;
 close(MYFILE);
}

# Prints the mime header only
sub Mime {
  print "Content-type: text/html\nPragma: no-cache\n\n";
}
