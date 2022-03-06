#!/usr/bin/perl

&Parse_Form;

my $cname = $formdata{'cname'};

&Mime;
print <<MYHTM;

<html><head>
<SCRIPT LANGUAGE="javascript">
<!--
function SubmitMyForm()
{
  document.forms[0].message.value = document.forms[0].chat_input.value;
  document.forms[0].chat_input.value='';
  document.forms[0].chat_input.focus();
  return(true);
}
//-->
</SCRIPT></head>
<BODY BGCOLOR="#F0F0F0" TEXT="#000000" LINK="#0000FF" VLINK="#800080" ALINK="#FF0000">
<form method="POST" action="bc_chat.cgi" target="main" OnSubmit="javascript:SubmitMyForm();">
<input type="hidden" name="cname" value="$cname">
<input type="hidden" name="room" value="general">
<input type="hidden" name="message" value="">
<p><input type="text" name="chat_input" size="46" maxlength="255" AUTOCOMPLETE="OFF">
<input type="submit" value="Send"></p>
</form></body></html>
MYHTM
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

# Prints the mime header only
sub Mime {
  print "Content-type: text/html\nPragma: no-cache\n\n";
}
