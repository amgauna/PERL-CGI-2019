#!/usr/bin/perl

# Please do not remove the BlueSparks ad unless you
# place a link someplace on your site to:
# http://www.bluesparks.com/

# The easiest way to remove the BlueSparks ad
# is to create a html file named logo.htm and place
# it in the same directory as the cgi files.
# BlueChat will display logo.htm instead of the BlueSparks ad.
# But please link to BlueSparks first.

print "Content-type: text/html\n\n";

if (-e 'logo.htm') {
 if (open(MYFILE, 'logo.htm')){
   print while <MYFILE>;
   close(MYFILE);
   exit;
 }
}

print <<LOGOHTML;
<html><head><title>Logo</title></head>
<body bgcolor="#F0F0F0" text="#000000" vlink="#0000FF" alink="#FF0000">
<p align="center"><font color="#800000"><strong>BlueSparks</strong></font><br>
<font color="#004080">Free Chat<br>Free Games<br>Free Everything</font></p>
<p align="center"><a href="http://www.bluesparks.com/" target="_blank"><small>www.bluesparks.com</small></a></p>
</body></html>
LOGOHTML
exit;
