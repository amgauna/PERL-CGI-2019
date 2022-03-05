#! /usr/local/bin/tclsh
/* Diz ao servidor para correr o interpretador tcl localizado no directório /usr/local/bin/ para executar o programa cgi/*

puts "Content-type: text/plain", "\n\n"
set query_string $ENV{'QUERY_STRING'}
set par [split $query_string = ] 
set field_name [lindex $par 0]
set command [lindex $par 1] 
if {$command == "guest"} {
puts "usr/local/bin/guest"
} elsif {$command == "mgi"} {
puts "usr/ucb/mgi"
} else {
puts "usr/local/bin/outro";
}
exit(0);
