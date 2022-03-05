#!/bin/sh
#A próxima linha reinicia usando o wish \
    exec wish "$0" "$@"
proc soma { N } {
    set A 0
    set B 0
    while {$A < $N} {
	incr A
	set B [expr $B + $A]
    }
    puts "A soma dos $N primeiros números inteiros é $B"
}

button .b1 -text "Executar o programa soma" -command {soma 5}
pack .b1
