#!/usr/bin/perl

use Socket;

############## SPECIAL FORM VARIABLES ############################
#required:    comma delimited list of required entry fields
#data_order:  comma delimited list indicating what fields to actually
#             print and in what order.
#outputfile:  the name of the file to save the data in if using a file.
#             the file will automatically be named ending with .bout
#emailfile:   the name of the file to hold only the sender e-mail address
#             the file will automatically be named ending with .bemf
#ok_url:      URL to go to if successful
#not_ok_url   URL to go to if unsuccessful
#submit_to:   email address of person to input receive data by mail
#             this can be a comma seperated list of e-mail addresses
#cc_to:       email address of Cc Recipient
#             this can be a comma seperated list of e-mail addresses
#submit_by:   email address of person completing form
#autorespond: NO LONGER USED AS OF JAN 31, 2000
#automessage: text to print for autoconfirmation e-mail
#             the file will automatically be named ending with .baut
#form_id:     name of form for e-mail subject
#countfile:   name of file for serial number counter
#             the file will automatically be named ending with .bcnt
#okaydomains: prevents calling the script from other sites,
#             without restricting e-mail addresses.
#             replaces $SECURE_NAME from earlier versions.
#             use only lower case letters.
#SMTP_SERVER: the full host name of the server providing e-mail
#             gateway service
##################################################################
# MAIN 
# uncomment the line below, and change bignosebird to your domain
# name if you wish to make is so the script can only be called
# from your site.
#@okaydomains=("http://mydomain.com", "http://www.mydomain.com");     
#SMTP_SERVER: indicates the name of the host acting as the e-mail
#             gateway. "localhost" should work on most systems.

$SMTP_SERVER="localhost";

#OR IF SMTP IS UNAVAILABLE TO YOU, USE SEND_MAIL-
# BUT NOT BOTH!

#$SEND_MAIL="/usr/lib/sendmail -t";

$lockfile="/tmp/bnbform.lck";

   $SD=&sys_date;
   $ST=&sys_time;

   &decode_vars;

   &valid_page;

   if ($fields{'countfile'} ne "") { &get_number; }

   &valid_data;

   &write_data;

   if ($fields{'automessage'} ne "") { &answer_back; }

   if ($fields{'ok_url'} ne ""){
     print "Location: $fields{'ok_url'}\n\n"; exit;
   }
     else { &thank_you; }

##################################################################
sub write_data
{

   if ($fields{'submit_by'} ne "") {
       if (&valid_address == 0) {
          &bad_email;
          exit;
       }
   }
   
   if ($fields{'submit_by'} ne "" && $fields{'emailfile'} ne "") {
      open (EMF,">>$fields{'emailfile'}");
      print EMF "$fields{'submit_by'}\n";
      close (EMF);
   }

   if ($fields{'submit_to'} ne "") {
     $msgtext="";
     $msgtext .= "On $SD at $ST,\n";
     $msgtext .=  "The following information was submitted:\n";
     $msgtext .=  "From Host: $ENV{'REMOTE_ADDR'}\n";
   }

   if ($fields{'outputfile'} ne "") { 
      &get_the_lock; 
      open(OUT_FILE,">>$fields{'outputfile'}"); 
   }

   foreach $to_print (@sortlist) {
      if ($fields{'outputfile'} ne "")
       { print OUT_FILE "$fields{$to_print}\|"; }
      if ($fields{'submit_to'} ne "")
       { $msgtext .= "$to_print = $fields{$to_print}\n"; }
   }
   if ($fields{'outputfile'} ne "") {
     print OUT_FILE "$SD\|$ST\|\n";
     close(OUT_FILE);
     &drop_the_lock;
   }

   foreach $to_get (@recipients) {
      $mailresult=&sendmail($fields{submit_by}, $fields{submit_by}, $to_get, $SMTP_SERVER, $fields{form_id}, $msgtext);
      if ($mailresult ne "1") {
       print "Content-type: text/html\n\n";
       print "MAIL NOT SENT. SMTP ERROR: $mailcodes{'$mailresult'}\n";
       exit
      }
    }
   foreach $to_cc (@cc_tos) {
      $mailresult=&sendmail($fields{submit_by}, $fields{submit_by}, $to_cc, $SMTP_SERVER, $fields{form_id}, $msgtext);
      if ($mailresult ne "1") {
       print "Content-type: text/html\n\n";
       print "MAIL NOT SENT. SMTP ERROR: $mailcodes{'$mailresult'}\n";
       exit
      }
    }

}

##################################################################
sub decode_vars
 {
  $i=0;
  read(STDIN,$temp,$ENV{'CONTENT_LENGTH'});
  @pairs=split(/&/,$temp);
  foreach $item(@pairs) {
    ($key,$content)=split(/=/,$item,2);
    $content=~tr/+/ /;
    $content=~s/%(..)/pack("c",hex($1))/ge;
    $content=~s/\t/ /g;
    $fields{$key}=$content;
    if ($key eq "data_order") {
       $content=~s/\012//g;
       $content=~s/\015//g;
       $content=~s/ //g;
       $content=~s/ //g;
       @sortlist=split(/,/,$content);
    }
    if ($key eq "required") {
       $content=~s/\012//g;
       $content=~s/\015//g;
       $content=~s/ //g;
       @mandatory=split(/,/,$content);
    }
    if ($key eq "submit_to") {
       $content=~s/\012//g;
       $content=~s/\015//g;
       $content=~s/ //g;
       @recipients=split(/,/,$content);
    }
    if ($key eq "cc_to") {
       $content=~s/\012//g;
       $content=~s/\015//g;
       $content=~s/ //g;
       @cc_tos=split(/,/,$content);
    }

   }
    if  (
     ( ($fields{automessage}=~ /^([-\/\w.]+)$/ || $fields{automessage} eq "") &&
      ($fields{countfile}=~ /^([-\/\w.]+)$/ || $fields{countfile} eq "") &&
      ($fields{emailfile}=~ /^([-\/\w.]+)$/ || $fields{emailfile} eq "") &&
      ($fields{outputfile}=~ /^([-\/\w.]+)$/ || $fields{outputfile} eq "") )
    ) {$donothing=0;}
    else {
       print "Content-type: text/html\n\n sorry, invalid characters...\n";
       exit;
    }
   if ($fields{automessage} ne "") {$fields{automessage} .= ".baut";}
   if ($fields{countfile} ne "") {$fields{countfile} .= ".bcnt";}
   if ($fields{emailfile} ne "") {$fields{emailfile} .= ".bemf";}
   if ($fields{outputfile} ne "") {$fields{outputfile} .= ".bout";}
}

##################################################################
sub valid_data
  {
   if ($fields{'data_order'} eq "")    #make sure we have work to do!
    {
      print "Content-type: text/html\n\n"; 
      print <<__W1__;

      <H1>NO data_order list SPECIFIED!</H1>

__W1__
      exit;
    }

   foreach $to_check (@mandatory) #test all required fields, bail on 1st bad
    {                             
      if ($fields{$to_check} eq "") {
          if ($fields{'not_ok_url'} ne "") { 
              print "Location: $fields{'not_ok_url'}\n\n";
              exit;
          }
             else { &try_again; }
      }
   }

  }

##################################################################
sub thank_you
  {
 print "Content-type: text/html\n\n"; 
 print <<__W2__;
   <BODY BGCOLOR="#FFFFFF">
   <CENTER>
   <TABLE WIDTH=550 BORDER=1>
    <TR>
     <TD>
      <H1>Thank you!</H1>
      Your information has been sent and I will be in touch
      with you as soon as I can
      <P>
      Here is the information you provided:
      <P>
__W2__

  foreach $itm (@sortlist) {
   print <<__W2A__;
   $itm: $fields{$itm}
   <BR>
__W2A__
  }

 print <<__W2B__;
  </TD>
  </TR>
 </TABLE>

__W2B__

      exit;
  }

##################################################################
sub try_again
  {
      print "Content-type: text/html\n\n"; 
      print <<__W3__;

      <H1>Missing Data!</H1>
      <B>Please press the back button and fill in
      all required fields!<P></B>

__W3__
      exit;
  }

##################################################################
sub answer_back
 {

   $subject = "Thank you";
   $msgtext="";
  if ($fields{'automessage'} ne "") {
    open (AM,"< $fields{'automessage'}");
    while (<AM>) {
      chop $_;
      $msgtext .= "$_\n";
    } 
    close(AM);
  }
    else {
      $msgtext =<<__W4__;

Thank you for your submission. I will be
getting in touch with you soon.

__W4__
    }
  $replyaddr=$recipients[0];
  $mailresult=&sendmail($replyaddr, $replyaddr, $fields{submit_by}, $SMTP_SERVER, $subject, $msgtext);
 }

##################################################################

sub get_number
 {
   $newnum=0;
   open(COUNTER,"<$fields{'countfile'}");
   while($thisnum=<COUNTER>) {
      if ($thisnum eq "") { $thisnum = 0;}
      $newnum = $thisnum + 1;
   }
   close(COUNTER);
   open(COUNTER,">$fields{'countfile'}");
   print COUNTER "$newnum";
   close (COUNTER);
   $fields{'counter'}=$newnum
 }

##################################################################
sub valid_address 
 {
  $testmail = $fields{'submit_by'};
  if ($testmail =~/ /)
   { return 0; }
  if ($testmail =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)/ ||
  $testmail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/)
   { return 0; }
   else { return 1; }
}

##################################################################
sub bad_email
{
print <<__STOP_OF_BADMAIL__;
Content-type: text/html

<FONT SIZE="+1">
<B>
SORRY! Your request could not be processed because of an
improperly formatted e-mail address. Please use your browser's 
back button to return to the form entry page.
</B>
</FONT>
__STOP_OF_BADMAIL__
}

sub get_the_lock
{
  local ($endtime);                                   
  $endtime = 60;                                      
  $endtime = time + $endtime;                         
  while (-e $lockfile && time < $endtime) 
   {
    # Do Nothing                                    
   }                                                   
   open(LOCK_FILE, ">$lockfile");                     
}

sub drop_the_lock
{
  close($lockfile);
  unlink($lockfile);
}


##################################################################
sub valid_page
 {
  if (@okaydomains == 0)
     {return;}
  $DOMAIN_OK=0;
  $RF=$ENV{'HTTP_REFERER'};
  $RF=~tr/A-Z/a-z/;
  foreach $ts (@okaydomains) {
     if ($RF =~ /$ts/)
      { $DOMAIN_OK=1; }
  }
  if ( $DOMAIN_OK == 0) {
      print "Content-type: text/html\n\n Sorry....Cant run from here!";    
      exit;
  }
 }


###################################################################
#Sendmail.pm routine below by Milivoj Ivkovic (modified by bnb)
###################################################################
sub sendmail  {

# error codes below for those who bother to check result codes <gr>

# 1 success
# -1 $smtphost unknown
# -2 socket() failed
# -3 connect() failed
# -4 service not available
# -5 unspecified communication error
# -6 local user $to unknown on host $smtp
# -7 transmission of message failed
# -8 argument $to empty
#
#  Sample call:
#
# &sendmail($from, $reply, $to, $smtp, $subject, $message );
#
#  Note that there are several commands for cleaning up possible bad inputs - if you
#  are hard coding things from a library file, so of those are unnecesssary
#

    my ($fromaddr, $replyaddr, $to, $smtp, $subject, $message) = @_;

    $to =~ s/[ \t]+/, /g; # pack spaces and add comma
    $fromaddr =~ s/.*<([^\s]*?)>/$1/; # get from email address
    $replyaddr =~ s/.*<([^\s]*?)>/$1/; # get reply email address
    $replyaddr =~ s/^([^\s]+).*/$1/; # use first address
    $message =~ s/^\./\.\./gm; # handle . as first character
    $message =~ s/\r\n/\n/g; # handle line ending
    $message =~ s/\n/\r\n/g;
    $smtp =~ s/^\s+//g; # remove spaces around $smtp
    $smtp =~ s/\s+$//g;

    if (!$to)
    {
	return(-8);
    }

 if ($SMTP_SERVER ne "")
  {
    my($proto) = (getprotobyname('tcp'))[2];
    my($port) = (getservbyname('smtp', 'tcp'))[2];

    my($smtpaddr) = ($smtp =~
		     /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/)
	? pack('C4',$1,$2,$3,$4)
	    : (gethostbyname($smtp))[4];

    if (!defined($smtpaddr))
    {
	return(-1);
    }

    if (!socket(MAIL, AF_INET, SOCK_STREAM, $proto))
    {
	return(-2);
    }

    if (!connect(MAIL, pack('Sna4x8', AF_INET, $port, $smtpaddr)))
    {
	return(-3);
    }

    my($oldfh) = select(MAIL);
    $| = 1;
    select($oldfh);

    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-4);
    }

    print MAIL "helo $SMTP_SERVER\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-5);
    }

    print MAIL "mail from: <$fromaddr>\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-5);
    }

    foreach (split(/, /, $to))
    {
	print MAIL "rcpt to: <$_>\r\n";
	$_ = <MAIL>;
	if (/^[45]/)
	{
	    close(MAIL);
	    return(-6);
	}
    }

    print MAIL "data\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close MAIL;
	return(-5);
    }

   }

  if ($SEND_MAIL ne "")
   {
     open (MAIL,"| $SEND_MAIL");
   }

    print MAIL "To: $to\n";
    print MAIL "From: $fromaddr\n";
    print MAIL "Reply-to: $replyaddr\n" if $replyaddr;
    print MAIL "X-Mailer: Perl Powered Socket Mailer\n";
    print MAIL "Subject: $subject\n\n";
    print MAIL "$message";
    print MAIL "\n.\n";

 if ($SMTP_SERVER ne "")
  {
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-7);
    }

    print MAIL "quit\r\n";
    $_ = <MAIL>;
  }

    close(MAIL);
    return(1);
}

sub sys_date
{
 %mn = ('Jan','01', 'Feb','02', 'Mar','03', 'Apr','04',
        'May','05', 'Jun','06', 'Jul','07', 'Aug','08',
        'Sep','09', 'Oct','10', 'Nov','11', 'Dec','12' );
 $sydate=localtime(time);
 ($day, $month, $num, $time, $year) = split(/\s+/,$sydate);
    $zl=length($num);
    if ($zl == 1)
      { $num = "0$num";}
 $yyyymmdd="$year\-$mn{$month}\-$num";
 return $yyyymmdd;
}


sub sys_time
{
 $sydate=localtime(time);
 ($day, $month, $num, $time, $year) = split(/\s+/,$sydate);
 return $time;
}
#--------DISCLAIMER-AND-COPYRIGHT-INFORMATION---------------------------#
# ANY SOFTWARE PROVIDED BY BIGNOSEBIRD.COM, INC. IS ``AS IS'' AND ANY
# EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BIGNOSEBIRD.COM, INC. OR
# ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# THIS SCRIPT IS PROVIDED WITHOUT SUPPORT
#
# THIS SCRIPT IS FREEWARE AND CAN BE USED FOR BOTH COMMERCIAL AND
# NON-COMMERCIAL USE. REPUBLICATION OF THE SCRIPT REQUIRES OUR PERMISSION.
# webmaster\@bignosebird.com
#-----------------------------------------------------------------------#

