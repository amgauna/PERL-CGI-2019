#!/usr/local/bin/perl

require config;

# HTML 
#
########################

sub willkommen { 
    print << "[END]";
<HTML>
<HEAD><TITLE>$html_title - Login</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>$html_title</I></H1>
<H3>Entrada</H3>
<FORM METHOD=POST ACTION="$script2_name">
<INPUT TYPE=hidden NAME="action" VALUE="login">
<TABLE><TR><TD>
<B>Apelido:</B> </TD><TD><INPUT NAME="name"><BR></TD></TR>
<TR><TD><B>Senha:</B> </TD><TD><INPUT TYPE=PASSWORD NAME="password"><BR>
</TD></TR></TABLE>
<INPUT TYPE=SUBMIT VALUE="entrar">
</FORM>
<P>
<B><A HREF="$script2_name?action=register">registrar novo apelido</A></B>
</P>
</CENTER>
</BODY>
</HTML>
[END]
}


#CHATINPUT.HTML
sub chatinput_html {
    print <<"[END]";
<HTML>$html_bodytag
<FORM METHOD=POST ACTION="$script_name">
<TABLE WIDTH=\"100%\"><TR><TD>
<INPUT TYPE=HIDDEN NAME=\"action\" VALUE=\"postmsg\">
<INPUT TYPE=HIDDEN NAME=\"name\" VALUE=\"$query{'name'}\">
<INPUT TYPE=HIDDEN NAME=\"password\" VALUE=\"$query{'password'}\">
<INPUT TYPE=HIDDEN NAME=\"color\" VALUE=\"$query{'color'}\">
<INPUT TYPE=HIDDEN NAME=\"new_msg_on_top\" VALUE=\"$query{'new_msg_on_top'}\">
<INPUT TYPE=HIDDEN NAME=\"updatefrequency\" VALUE=\"$query{'updatefrequency'}\">
<INPUT SIZE=\"$input_field_size\" NAME=\"msg\" MAXLENGTH=400>
<INPUT TYPE=SUBMIT VALUE=\"enviar\">
[END]
    &select_user;
    print <<"[END]";
<A HREF=\"$script2_name?action=options_html\&name=$query{'name'}\&password=$query{'password'}\&updatefrequency=$query{'updatefrequency'}\&color=$query{'color'}\&new_msg_on_top=$query{'new_msg_on_top'}\" TARGET=\"_top\">op��es</A>
&nbsp;<A HREF=\"$script2_name?action=changeuserinfo\&name=$query{'name'}\&password=$query{'password'}\&updatefrequency=$query{'updatefrequency'}\&color=$query{'color'}\&new_msg_on_top=$query{'new_msg_on_top'}\" TARGET=\"_top\">inf.usu�rio</A></B>
&nbsp;<A HREF=\"$script2_name?action=gotourl&url=$logout_url\" TARGET=\"_top\"><B> SAIR ! </B></A></B>
</TD><TD ALIGN=\"right\">
<SMALL><A HREF=\"http://www.bigfoot.com/~ralfg\" TARGET=\"_top\">&copy; ralf 99</A></SMALL>
</TD></TR></TABLE>
</FORM>
<SCRIPT LANGUAGE=\"javascript\">
document.forms[0].msg.focus()
</SCRIPT>
</BODY>
</HTML>
[END]
}


#STILLALIVE.HTML - the users online frame
sub stillalive_html_header {
    print <<"[END]";
<HTML><HEAD>
<SCRIPT LANGUAGE=\"JavaScript\"><!--
    window.setTimeout(\"location.reload()\",20000)
//--></SCRIPT><NOSCRIPT>
<meta http-equiv=\"refresh\" content=\"20\">
</NOSCRIPT>
</HEAD>$html_bodytag
[END]
}
sub stillalive_html_footer {
    print <<"[END]";
</BODY></HTML>
[END]
}

#CHAT.HTML
sub chat_html_header {
    print <<"[END]";
<HTML><HEAD>
<SCRIPT LANGUAGE=\"JavaScript\"><!--
    window.setTimeout(\"location.reload()\",$query{'updatefrequency'}000)
//--></SCRIPT><NOSCRIPT>
<meta http-equiv=\"refresh\" content=\"$query{'updatefrequency'}\">
</NOSCRIPT>
</HEAD>$html_bodytag
[END]
}
sub chat_html_footer {
    print <<"[END]";
</BODY></HTML>
[END]
}


# END HTML PART.
#
#######################


# Main Part - DON'T CHANGE ANYTHING HERE!
#
#######################

&action;    # Fuehrt je nach action variable gegebene sub aus
	    # action im FORM definieren!

exit;

sub action {
    if ($qs eq "") { # Wenn query_string leer sprung zum
    	&welcome;	       # welcome-teil, 1st visit seite
    } 
    elsif ($query{'action'} eq "chatinput_html") {
    	&header;
    	&chatinput_html;
    }
    elsif ($query{'action'} eq "stillalive") {
        &stillalive;
    }
    elsif ($query{'action'} eq "chat") {
        &chat;
    }
    elsif ($query{'action'} eq "postmsg") {
        &postmsg;
    }
    else {
    	&error;
    } 
}


sub welcome { # Aufruf beim ersten Programmstart
    &header;
    &willkommen_html;
}

sub stillalive { # stillalive/who prozedur
    &checkpass;
    if (-e "$data_dir/$data_stillalive_file") { # SAfile oeffnen/erstellen
    } else {
        &create_file("$data_dir/$data_stillalive_file");        
    }

    open (SAFILE, "<$data_dir/$data_stillalive_file") || &error("opening safile failed");
    flock(SAFILE,2); 
    my $safile = <SAFILE>; # Daten aus safile an $safile uebergeben
#    flock(SAFILE,8);
    close SAFILE;

    @sa = split (/;;/, $safile);

    @sa = &repair_safile(@sa) if (($#sa+1) % 2 == 1); # wenn safile fehlerhaft -> repair

    $ownsaexists=0;
    for ($i=0; $i<=$#sa; $i+=2) { # eigenen Eintrag erneuern
        if ($sa[$i] eq $query{'name'}) {
            $sa[$i+1] = time;
            $ownsaexists=1;
        }  
    }

    # Eintraege nach ueberfaelligen (aelter als 50s) durchsuchen und diese entfernen    
    for ($i=1; $i<=$#sa; $i+=2) { 
        if ($sa[$i] < (time - 50)) { # ist zeitstempel schon aelter als 50s?
            #print logout msg
            open (CHATFILE, ">>$data_dir/$data_msg_file");
            flock(CHATFILE,2);
            print CHATFILE "<B>".$sa[$i-1]." ".$logout_msg."</B>\n";
            close CHATFILE;

            $sa[$i] = "//2delete";
            $sa[$i-1] = "//2delete";  # zu loeschende eintraege mit //2delete ersetzten
        }  
    }
    # alle Felder mit //2delete entfernen
    $templsa = $#sa; # Laenge von @sa wird in templsa gespeichert;
    for ($i=0; $i<=$templsa; $i++) {
        $temp = shift(@sa);
        if ($temp ne "//2delete") {
            push(@sa,$temp);
        }
    }

    # if no own sa entry exists -> add
    if ($ownsaexists != 1) { 
        $sa[++$#sa] = $query{'name'};
        $sa[++$#sa] = time;
    }

    $safile = join(';;', @sa);
    
    open (SAFILE, ">$data_dir/$data_stillalive_file") || &error("opening safile failed");
    flock(SAFILE,2);

    print SAFILE $safile;

#    flock(SAFILE,8);
    close SAFILE;
    
    &header;
    &stillalive_html_header;

    $nrusers = ($#sa+1) / 2;
    $s = $nrusers > 1 ? "s" : "";

    print "<H1><I>$nrusers usu�rio$s no chat!</I></H2>";
    for ($i=0; $i<=$#sa; $i+=2) {
        print "<B><A HREF=\"$script2_name?action=userinfo\&infoabout=$sa[$i]\" TARGET=\"RC_INFO\">$sa[$i]</A></B><BR>";
    }
    &stillalive_html_footer;
}

sub chat { # Chatprocedure: show Messages    
    if (-e "$data_dir/$data_msg_file") { # CHATFILE oeffnen/erstellen
    } else {
        &create_file("$data_dir/$data_msg_file");        
    }

    &checkpass;

    &header;
    &chat_html_header;

    open (CHATFILE, "<$data_dir/$data_msg_file") || &error("opening chatfile failed");
    flock(CHATFILE,2);

    my @chatfile = <CHATFILE>;

#    flock(CHATFILE,8);
    close CHATFILE;

    # Ausgabe Messages    
    foreach(@chatfile) {
        while ($_ =~ /<!--PrivateMsgHere;;/) { # private msg?
            my @this_msg = split (/;;/, $_); 
            if ($this_msg[1] eq $query{'name'}) { # private msg fuer user?
                open (PRIVATEFILE, "<$data_dir/$data_private_file.$query{'name'}") || &error("opening privatefile failed");
                my @privatefile = <PRIVATEFILE>;
                close PRIVATEFILE;
                for (@privatefile) {
                    my @priv_file_line = split (/;;/, $_); 
                    if ($priv_file_line[0] == $this_msg[2])  {
                        if ($query{'new_msg_on_top'} == 1) {
                            unshift @chatmsgs, $priv_file_line[1];
                        } else {
                            print "\n<BR>$priv_file_line[1]";
                        }
                    }
                }
            }
            $_ =~ s/<!--PrivateMsgHere;;/<!--/;
            $_ =~ s/;;//;
            $_ =~ s/;;//;
        }

        $query{'new_msg_on_top'} == 1 ? unshift @chatmsgs, $_ : print "\n<BR>$_";
    }

    print "<A NAME=\"end\">";
    if ($query{'new_msg_on_top'} == 1) {
        for (@chatmsgs) {
            print "\n<BR>$_";
        }
    }
    &chat_html_footer;
}

sub postmsg {
    open (CHATFILE, "<$data_dir/$data_msg_file") || &error("opening chatfile failed");
    flock(CHATFILE,2);

    my @chatfile = <CHATFILE>;

#    flock(CHATFILE,8);
    close CHATFILE;

    # alte Eintraege >$message_limit loeschen
    for ($i=0; $i <= ($#chatfile - $message_limit); $i++) {
        shift(@chatfile);
    }
    open (CHATFILE, ">$data_dir/$data_msg_file") || &error("opening chatfile failed");
    flock(CHATFILE,2);

    print CHATFILE @chatfile;

#    flock(CHATFILE,8);
    close CHATFILE;

    # check name+password
    &checkpass;
    
    $query{'msg'} = &wash_msg($query{'msg'});

    if (substr($query{'msg'},0,1) eq "/" ) { # msg = command?
        &command("$query{'msg'}");    
    } elsif ($query{'msg_to'} ne "") {
        &command("/msg $query{'msg_to'} $query{'msg'}");    
    } elsif ($query{'msg'} ne "") {
    # poste msg nach $data_dir/message
        open (CHATFILE, ">>$data_dir/$data_msg_file");
        flock(CHATFILE,2);

        # set userspecified font color if not standard
        if ($query{'color'} eq "standard") {
            print CHATFILE "<B>$query{'name'}</B>: $query{'msg'}\n";
        } else {
            print CHATFILE "<FONT COLOR=\"$query{'color'}\"><B>$query{'name'}</B>: $query{'msg'}</FONT>\n";

        }        

#        flock(CHATFILE,8); # UNLOCK Chatfile
        close CHATFILE;
        # LOG ACTION
        if ($logtype >= 3) {
            open (LOGFILE, ">>$log_dir/$log_file") || &error("::open $log_dir/$log_file failed::");
            flock(LOGFILE,2);
            print LOGFILE localtime(time)." $ENV{'REMOTE_ADDR'} [MSG] $query{'name'}: $query{'msg'}\n";
            close LOGFILE;
        }
    }
    &header;
    &chatinput_html;
}

sub command { # Kommandoprozedur fuer /cmd ; parameter 0: commandstring
    $_[0] = $_[0]." ";
    $_[0] =~ s/</\&lt\;/g; # 'entschaerfe' html-tags
    $_[0] = substr($_[0], 1, length($_[0])-1);
    @cmdargs = split(/ /, $_[0]);
    $thecommand = substr($_[0],0 , index($_[0], " "));
    if ($thecommand eq "msg") {
        my $msg_to = $cmdargs[1];
        $_[0]=substr($_[0], index($_[0], " ")+1, length($_[0]));
        $_[0]=substr($_[0], index($_[0], " ")+1, length($_[0]));
        if ($_[0] ne "" && $_[0] ne " ") {
            &postprivatemsg($query{'name'}, "->".$msg_to, $_[0]); 
            &postprivatemsg($msg_to, $query{'name'}, $_[0]);
        }
    } elsif ($thecommand eq "help") {
        &help;
    } elsif ($thecommand eq "about") {
        &about;
    } elsif ($thecommand eq "me") {
        $_[0]=substr($_[0], index($_[0], " ")+1, length($_[0]));
        &me_action($query{'name'}, $_[0]);
    } elsif ($thecommand eq "list_nicks") {
        my $usermpass = $cmdargs[1];
        if ($usermpass eq $masterpassword) {
            &list_nicks;
        } else {
            &postprivatemsg($query{'name'}, "LIST_NICKS", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "clean_old_nicks") {
        my $usermpass = $cmdargs[1];
        my $cleandate = $cmdargs[2];
        if ($usermpass eq $masterpassword) {
            if ($cleandate ne "") {
                &clean_old_nicks($cleandate);
            } else {
                &postprivatemsg($query{'name'}, "CLEAN_OLD_NICKS", $nocleantime_msg);
            }
        } else {
            &postprivatemsg($query{'name'}, "CLEAN_OLD_NICKS", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "remove_nick") {
        my $usermpass = $cmdargs[1];
        my $nick2rm = $cmdargs[2];
        if ($usermpass eq $masterpassword) {
            &remove_nick($nick2rm);
        } else {
            &postprivatemsg($query{'name'}, "REMOVE_NICK", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "userinfo") {
        $query{'infoabout'} = $cmdargs[1];
        $userinfo_as_private_msg = 1;
        &userinfo;
    } elsif ($thecommand eq "ban") {
        if ($cmdargs[1] eq $masterpassword) {
            &kick_or_ban_nick($cmdargs[2], 2);
        } else {
            &postprivatemsg($query{'name'}, "BAN", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "kick") {
        if ($cmdargs[1] eq $masterpassword) {
            &kick_or_ban_nick($cmdargs[2], 1);
        } else {
            &postprivatemsg($query{'name'}, "KICK", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "banned_list") {
        if ($cmdargs[1] eq $masterpassword) {
            &banned_list;
        } else {
            &postprivatemsg($query{'name'}, "BANNED_LIST", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "unban") {
        if ($cmdargs[1] eq $masterpassword) {
            &unban($cmdargs[2], 2);
        } else {
            &postprivatemsg($query{'name'}, "UNBAN", $wrongmasterpass_msg);
        }
    } elsif ($thecommand eq "memo") {
        $_[0]=substr($_[0], index($_[0], " ")+1, length($_[0]));
        $_[0]=substr($_[0], index($_[0], " ")+1, length($_[0]));
        &memo($cmdargs[1],$query{'name'}, $_[0]);
    } else {
        &postprivatemsg($query{'name'}, "HELP", "$unknowncmd_msg: $_[0]");
    }
}

sub help {
    &postprivatemsg($query{'name'}, "HELP", $help_msg);
}


sub me_action {  # parameter 0: wer 1: was
    open (CHATFILE, ">>$data_dir/$data_msg_file");
    flock(CHATFILE,2);

    print CHATFILE "<B>* $_[0] $_[1]</B>\n";

#    flock(CHATFILE,8);
    close CHATFILE;
}

sub about {
    &postprivatemsg($query{'name'}, "ABOUT", $about_msg);
}

sub list_nicks {
    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open Nickfile failed::");
    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen

    $nicklist = "<TABLE><TR><TD><B>Nickname</B></TD><TD><B>eMail</B></TD><TD><B>Created on</B></TD><TD><B>last visited</B></TD><TD><B>current/last ip</B></TD><TD><B>status</B></TD><TD><B>#memos</B></TD></TR>";

    for (@nickfile) {
        $_ =~ s/\n//g;
        my @nickfileentry = split(/;;/, $_);
        $status = ($nickfileentry[10] == 0) ? "normal" : "kicked";
        $status = ($nickfileentry[10] == 2) ? "banned" : $status;
		$nicklist = $nicklist."<TR><TD>".$nickfileentry[0]."</TD><TD>".$nickfileentry[2]."</TD><TD>".$nickfileentry[3]."</TD><TD>".localtime($nickfileentry[4])."</TD><TD>".$nickfileentry[11]."</TD><TD>".$status."</TD><TD>".$nickfileentry[12]."</TD></TR>";
    }
    $nicklist = $nicklist."</TABLE>";
    &postprivatemsg($query{'name'}, "LIST_NICKS", $nicklist);
}

sub clean_old_nicks { # clear all old nicks older than $_[0]
    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; 
    close NICKFILE;

    &make_matrix(@nickfile);
    
    $removed_users=0;
    $removed_users_names = "";
    $nr_of_days=$_[0];
    @nickfile_matrix = @matrix;
    for ($con_i=0; $con_i<=$#nickfile_matrix; $con_i++) {
        if ($nickfile_matrix[$con_i][4] < (time - $nr_of_days*60*60*24) && $nickfile_matrix[$con_i][0] ne $query{'name'}) { # ist zeitstempel schon aelter als $_[0] tage
            $removed_users_names = $removed_users_names." $nickfile_matrix[$con_i][0]";
            system 'rm', "$data_dir/$data_private_file.$nickfile_matrix[$con_i][0]"; # deletes private file

            $removed_users++;
            
            $nickfile_matrix[$con_i] = "//2delete";

        }  
    }
    @matrix = @nickfile_matrix;
    # alle Felder mit //2delete entfernen
    $templmatrix = $#matrix; # Laenge von @sa wird in templsa gespeichert;
    for ($i=0; $i<=$templmatrix; $i++) {
        $temp = shift(@matrix);
        if ($temp ne "//2delete") {
            push(@matrix,$temp);
        }
    }

    open (NICKFILE, ">$data_dir/$data_nicks_file");
    flock(NICKFILE,2);

    for ($i2=0; $i2<=$#matrix/2; $i2++) {
        print NICKFILE &join_matrix."\n";
    }

#    flock(NICKFILE,8); 
    close NICKFILE;

    @remove_from_uifile = split (/ /, $removed_users_names);
    for (@remove_from_uifile) {
        &rm_uientry($_); # delete user from uifile
        &rm_memoentry($_); # delete memos for user from memofile
    }    

    &postprivatemsg("$query{'name'}","CLEAN_OLD_NICKS","removed users: $removed_users_names<BR>total: $removed_users");

     # LOG ACTION
     if ($logtype >= 1) {
        open (LOGFILE, ">>$log_dir/$log_file") || &error("::open $log_dir/$log_file failed::");
        flock(LOGFILE,2);
        print LOGFILE localtime(time)." $ENV{'REMOTE_ADDR'} [CLEAN_OLD_NICKS] removed users: $removed_users_names\n";
        close LOGFILE;
    }
}

sub remove_nick { # $_[0] = nick to remove
    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; 
    close NICKFILE;

    &make_matrix(@nickfile);
    
    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $_[0]) { # ist nick = nick to remove
            $matrix[$i] = "//2delete";
            $userfound=1;
        }  
    }
    # alle Felder mit //2delete entfernen
    $templmatrix = $#matrix; # Laenge von @sa wird in templsa gespeichert;
    for ($i=0; $i<=$templmatrix; $i++) {
        $temp = shift(@matrix);
        if ($temp ne "//2delete") {
            push(@matrix,$temp);
        }
    }

    open (NICKFILE, ">$data_dir/$data_nicks_file");
    flock(NICKFILE,2);

    for ($i2=0; $i2<=$#matrix/2; $i2++) {
        print NICKFILE &join_matrix."\n";
    }

    if ($userfound == 1) {
        system 'rm', "$data_dir/$data_private_file.$_[0]"; # deletes private file
        &rm_uientry($_[0]);
        &rm_memoentry($_[0]);
        &postprivatemsg("$query{'name'}","REMOVE_NICK","User $_[0] removed");
         # LOG ACTION
         if ($logtype >= 1) {
            open (LOGFILE, ">>$log_dir/$log_file") || &error("::open $log_dir/$log_file failed::");
            flock(LOGFILE,2);
            print LOGFILE localtime(time)." $ENV{'REMOTE_ADDR'} [REMOVE_NICK] $_[0] removed\n";
            close LOGFILE;
        }
    } else {
        &postprivatemsg("$query{'name'}","REMOVE_NICK","User $_[0] doesnot exist");
    }
}

sub select_user {
    if (-e "$data_dir/$data_stillalive_file") { # SAfile oeffnen/erstellen
    } else {
        &create_file("$data_dir/$data_stillalive_file");        
    }

    open (SAFILE, "<$data_dir/$data_stillalive_file") || &error("opening safile failed");
    flock(SAFILE,2); 
    my $safile = <SAFILE>; # Daten aus safile an $safile uebergeben
#    flock(SAFILE,8);
    close SAFILE;

    @sa = split (/;;/, $safile);

    print "<SELECT MAXLENGTH=2 NAME=\"msg_to\">";
    $selected = ($query{'msg_to'} eq "") ? "SELECTED" : "";
    print "<OPTION $selected VALUE=\"\">todos</A>";
    for ($i=0; $i<=$#sa; $i+=2) {
        $points = (length($sa[$i]) > 9) ? ".." : "";
        $shortnick = substr($sa[$i],0,9).$points;
        $selected = ($query{'msg_to'} eq $sa[$i]) ? "SELECTED" : "";
        print "<OPTION $selected VALUE=\"$sa[$i]\">$shortnick</A>";
    }
    print "</SELECT>";
}

# remove user from userinfo database
sub rm_uientry { # $_[0] = nick to remove from userinfo database
    open (UIFILE, "<$data_dir/$data_userinfo_file") || &error("::open $data_dir/$data_userinfo_file failed::");
    my @uifile = <UIFILE>; 
    close UIFILE;

    &make_matrix(@uifile);    

    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $_[0]) { # ist nick = nick to remove
            $matrix[$i] = "//2delete";
        }  
    }
    # alle Felder mit //2delete entfernen
    $templmatrix = $#matrix;
    for ($i=0; $i<=$templmatrix; $i++) {
        $temp = shift(@matrix);
        if ($temp ne "//2delete") {
            push(@matrix,$temp);
        }
    }

    open (UIFILE, ">$data_dir/$data_userinfo_file");
    flock(UIFILE,2);

    for ($i2=0; $i2<=$#matrix/2; $i2++) {
        print UIFILE &join_matrix."\n";
    }
    close UIFILE;
}

# remove memos for user from memo database
sub rm_memoentry { # $_[0] = nick to remove
    open (MEMOFILE, "<$data_dir/$data_memo_file") || &error("::open $data_dir/$data_memo_file failed::");
    my @memofile = <MEMOFILE>; 
    close UIFILE;

    &make_matrix(@memofile);    

    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $_[0]) { # ist nick = nick to remove
            $matrix[$i] = "//2delete";
        }  
    }
    # alle Felder mit //2delete entfernen
    $templmatrix = $#matrix;
    for ($i=0; $i<=$templmatrix; $i++) {
        $temp = shift(@matrix);
        if ($temp ne "//2delete") {
            push(@matrix,$temp);
        }
    }

    open (MEMOFILE, ">$data_dir/$data_memo_file");
    flock(MEMOFILE,2);

    for ($i2=0; $i2<=$#matrix/2; $i2++) {
        print MEMOFILE &join_matrix."\n";
    }
    close MEMOFILE;
}

sub kick_or_ban_nick { # $_[0] nick to kick/ban, $_[1] banlevel (1=kick, 2=ban)
    if ($_[0] =~ /^ip:/i) {
        open (BANFILE, ">>$data_dir/$data_banned_file");
        flock(BANFILE,2); 
        print BANFILE "$_[0];;";
        close BANFILE;
        &postprivatemsg("$query{'name'}","BAN","IP ".substr($_[0],3)." banned");
        return;
    }
    
    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen
    
    &make_matrix(@nickfile);

    for ($bani=0; $bani<=$#matrix; $bani++) {
        if (uc($matrix[$bani][0]) eq uc($_[0])) {
            $matrix[$bani][10] = $_[1];
            open (NICKFILE, ">$data_dir/$data_nicks_file");
            flock(NICKFILE,2); 

            for ($i2=0; $i2<=$#matrix; $i2++) {
                print NICKFILE &join_matrix."\n";
            }
#            flock(NICKFILE,8);
            close NICKFILE;

            # post ban msg
            if ($_[1] == 1) {
                &postprivatemsg("$query{'name'}","KICK","User $_[0] kicked");
            } elsif ($_[1] == 2) {
                &postprivatemsg("$query{'name'}","BAN","User $_[0] banned");
                open (BANFILE, ">>$data_dir/$data_banned_file");
                flock(BANFILE,2); 
                print BANFILE "$_[0];;";
                close BANFILE;
            }

        }
    }
}    

sub banned_list {
    open (BANFILE, "<$data_dir/$data_banned_file");
    my $banfile = <BANFILE>;
    $banfile =~ s/;;/<BR>/g;
    close BANFILE;
    &postprivatemsg("$query{'name'}","BANNED_LIST","<B>Banned:</B><BR>$banfile");
}

sub unban {
    open (BANFILE, "<$data_dir/$data_banned_file");
    my $banfile = <BANFILE>;
    my @temp = split(/;;/, $banfile);

    for ($i=0; $i<=@temp; $i++) {
        if ($temp[$i] eq $_[0]) { # ist nick/ip = nick/ip to unban
            $temp[$i] = "//2delete";
            &postprivatemsg("$query{'name'}","UNBAN","User $_[0] unbanned");
        }  
    }
    # alle Felder mit //2delete entfernen
    $templ = $#temp;
    for ($i=0; $i<=$templ; $i++) {
        $temp2 = shift(@temp);
        if ($temp2 ne "//2delete") {
            push(@temp,$temp2);
        }
    }

    open (BANFILE, ">$data_dir/$data_banned_file");
    flock(BANFILE,2); 
    print BANFILE join(';;', @temp);
    close BANFILE;

    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen
    
    &make_matrix(@nickfile);

    for ($bani=0; $bani<=$#matrix; $bani++) {
        if (uc($matrix[$bani][0]) eq uc($_[0])) {
            $matrix[$bani][10] = 0;
            open (NICKFILE, ">$data_dir/$data_nicks_file");
            flock(NICKFILE,2); 

            for ($i2=0; $i2<=$#matrix; $i2++) {
                print NICKFILE &join_matrix."\n";
            }
#            flock(NICKFILE,8);
            close NICKFILE;
        }
    }
}

sub memo {
    # check if recipient is valid
    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; 
    close NICKFILE;

    &make_matrix(@nickfile);
    
    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $_[0]) {
            $userfound=1;
			$matrix[$i][12]++; # increase number of memos
        }  
    }

	open (NICKFILE, ">$data_dir/$data_nicks_file");
	flock(NICKFILE,2); 
	for ($i2=0; $i2<=$#matrix; $i2++) {
		print NICKFILE &join_matrix."\n";
	}
	close NICKFILE;

    $memo_msg_to = $_[0];
    $memo_msg_from = $_[1];
    $memo_msg = $_[2];
    $memo_time = time;

    if ($userfound != 1) {
        &postprivatemsg("$query{'name'}","MEMO","User $_[0] doesnot exist");
        return;
    }

    &create_file("$data_dir/$data_memo_file") if (!-e "$data_dir/$data_memo_file");
    open (MEMOFILE, ">>$data_dir/$data_memo_file") || &error("opening memofile failed");
    flock(MEMOFILE,2); 
    print MEMOFILE "$memo_msg_to;;$memo_msg_from;;$memo_msg;;$memo_time\n";
    close MEMOFILE;
    &postprivatemsg("$query{'name'}","MEMO","Memo for $_[0] was posted successfully");
}

sub wash_msg { # $_[0] string to 'wash'
    # kill html-tags
    $_[0] =~ s/</\&lt\;/g;
    # kill linebreaks
    $_[0] =~ s/\n/<BR>/g;
    # kill ;
    $_[0] =~ s/;/&#59;/g;

    # link urls
    # http://*
    $_[0] =~ s/(\bhttp:\/\/.[^\ ]+)/<A HREF=\"$script2_name?action=gotourl\&url=$1\" TARGET=\"linkwindow\">$1<\/A>/g;
    # ftp://*
    $_[0] =~ s/(\bftp:\/\/.*\b)/<A HREF=\"$script2_name?action=gotourl\&url=$1\" TARGET=\"linkwindow\">$1<\/A>/g;
    # mailto:*
    $_[0] =~ s/(\bmailto:.*\b)/<A HREF=\"$1\">$1<\/A>/g;

    return $_[0];
}


# END Main Part
#
##############################
